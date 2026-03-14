#!/usr/bin/env python3
"""
Meme Scanner System - Backend API
基于 FastAPI 的 Meme 币扫描系统后端
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import asyncio
import aiohttp
import time
import os
from datetime import datetime
import uvicorn

app = FastAPI(title="Meme Scanner API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（前端）
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# 数据文件路径
DATA_DIR = "/home/n100/.openclaw/workspace/meme-scanner-system/data"
SCANNED_FILE = os.path.join(DATA_DIR, "scanned_tokens.json")
RESULTS_FILE = os.path.join(DATA_DIR, "latest_results.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# Ave.ai API Key
AVE_API_KEY = "uHxe2IxOYEx3vHNpUpPtVDJVd2UTPycHLimZkAIpyMxkGS9GE84tf05VU96Uwgdm"

# 默认配置
DEFAULT_CONFIG = {
    "min_mcap": 10000,
    "max_mcap": 5000000,
    "min_liquidity": 4000,
    "min_holders": 50,
    "min_change_24h": 100,
    "min_vol_mcap_ratio": 0.3,
    "max_bundler_rate": 0.5,
    "chains": ["sol", "bsc"],
    "scan_interval_minutes": 5
}

# --- 辅助函数 ---
def fmt_num(n):
    if n is None: return "N/A"
    n = float(n)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    if n >= 1: return f"${n:.2f}"
    return f"${n:.4f}"

def fmt_pct(p):
    if p is None: return "N/A"
    return f"{'+' if float(p)>=0 else ''}{float(p):.2f}%"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_scanned():
    if os.path.exists(SCANNED_FILE):
        with open(SCANNED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_scanned(data):
    with open(SCANNED_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return {"tokens": [], "last_scan": None}

def save_results(data):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- API 接口 ---

@app.get("/", response_class=HTMLResponse)
async def root():
    """返回前端页面"""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Meme Scanner</h1><p>Frontend not found</p>", status_code=404)

@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    results = load_results()
    scanned = load_scanned()
    config = load_config()
    return {
        "status": "online",
        "last_scan": results.get("last_scan"),
        "total_scanned": len(scanned),
        "latest_tokens_count": len(results.get("tokens", [])),
        "config": config
    }

@app.get("/api/config")
async def get_config():
    """获取当前配置"""
    return load_config()

@app.post("/api/config")
async def update_config(config: Dict[str, Any]):
    """更新配置"""
    current = load_config()
    current.update(config)
    save_config(current)
    return {"message": "配置已更新", "config": current}

@app.get("/api/results")
async def get_results():
    """获取最新扫描结果"""
    return load_results()

@app.post("/api/scan")
async def trigger_scan():
    """触发手动扫描"""
    try:
        results = await run_scan()
        return {"message": "扫描完成", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tokens")
async def get_tokens():
    """获取代币列表"""
    results = load_results()
    return {"tokens": results.get("tokens", []), "count": len(results.get("tokens", []))}

@app.get("/api/history")
async def get_history(limit: int = 50):
    """获取扫描历史"""
    scanned = load_scanned()
    items = sorted(scanned.items(), key=lambda x: x[1].get("timestamp", 0), reverse=True)
    return {"history": items[:limit], "total": len(scanned)}

# --- 扫描逻辑 ---

async def fetch_json(session, url, headers=None):
    """通用 JSON 获取"""
    try:
        async with session.get(url, headers=headers, timeout=30) as resp:
            return await resp.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

async def scan_gmgn(session, chain: str, config: dict) -> List[dict]:
    """从 gmgn.ai 扫描"""
    tokens = []
    url = f"https://gmgn.ai/defi/quotation/v1/rank/{chain}/swaps/1h?limit=50"
    
    try:
        data = await fetch_json(session, url)
        if data and data.get('code') == 0 and data.get('data', {}).get('rank'):
            for item in data['data']['rank']:
                token = item.get('token', {})
                if not token: continue
                
                address = token.get('address')
                symbol = token.get('symbol', 'UNKNOWN')
                name = token.get('name', 'Unknown')
                
                # 获取代币详情
                detail_url = f"https://gmgn.ai/defi/quotation/v1/tokens/{chain}/{address}"
                detail = await fetch_json(session, detail_url)
                
                if detail and detail.get('code') == 0:
                    token_data = detail.get('data', {})
                    
                    # 筛选条件
                    mcap = token_data.get('market_cap', 0)
                    liquidity = token_data.get('liquidity', 0)
                    holders = token_data.get('holders_count', 0)
                    price_change_24h = token_data.get('price_change_24h', 0)
                    
                    if (config['min_mcap'] <= mcap <= config['max_mcap'] and
                        liquidity >= config['min_liquidity'] and
                        holders >= config['min_holders'] and
                        price_change_24h >= config['min_change_24h']):
                        
                        tokens.append({
                            "symbol": symbol,
                            "name": name,
                            "address": address,
                            "chain": chain,
                            "price": token_data.get('price', 0),
                            "market_cap": mcap,
                            "liquidity": liquidity,
                            "holders": holders,
                            "price_change_24h": price_change_24h,
                            "volume_24h": token_data.get('volume_24h', 0),
                            "created_at": datetime.now().isoformat()
                        })
    except Exception as e:
        print(f"gmgn scan error: {e}")
    
    return tokens

async def scan_ave(session, chain: str, config: dict) -> List[dict]:
    """从 Ave.ai 扫描"""
    tokens = []
    url = f"{AVE_API_BASE}/v1/market/trending?chain={chain}"
    headers = {"Authorization": f"Bearer {AVE_API_KEY}"}
    
    try:
        data = await fetch_json(session, url, headers)
        if data and data.get('success') and data.get('data'):
            for item in data['data']:
                mcap = item.get('marketCap', 0)
                liquidity = item.get('liquidity', 0)
                holders = item.get('holders', 0)
                price_change_24h = item.get('priceChange24h', 0)
                
                if (config['min_mcap'] <= mcap <= config['max_mcap'] and
                    liquidity >= config['min_liquidity'] and
                    holders >= config['min_holders'] and
                    price_change_24h >= config['min_change_24h']):
                    
                    tokens.append({
                        "symbol": item.get('symbol', 'UNKNOWN'),
                        "name": item.get('name', 'Unknown'),
                        "address": item.get('address'),
                        "chain": chain,
                        "price": item.get('price', 0),
                        "market_cap": mcap,
                        "liquidity": liquidity,
                        "holders": holders,
                        "price_change_24h": price_change_24h,
                        "volume_24h": item.get('volume24h', 0),
                        "created_at": datetime.now().isoformat()
                    })
    except Exception as e:
        print(f"ave scan error: {e}")
    
    return tokens

async def run_scan():
    """执行完整扫描"""
    config = load_config()
    all_tokens = []
    scanned = load_scanned()
    
    async with aiohttp.ClientSession() as session:
        for chain in config.get('chains', ['sol', 'bsc']):
            # 扫描两个数据源
            gmgn_tokens = await scan_gmgn(session, chain, config)
            ave_tokens = await scan_ave(session, chain, config)
            all_tokens.extend(gmgn_tokens)
            all_tokens.extend(ave_tokens)
    
    # 去重
    seen = set()
    unique_tokens = []
    for token in all_tokens:
        key = f"{token['chain']}_{token['address']}"
        if key not in seen:
            seen.add(key)
            unique_tokens.append(token)
            # 记录已扫描
            scanned[key] = {
                "timestamp": time.time(),
                "symbol": token['symbol'],
                "chain": token['chain']
            }
    
    # 保存结果
    results = {
        "tokens": unique_tokens,
        "last_scan": datetime.now().isoformat(),
        "total_found": len(unique_tokens)
    }
    save_results(results)
    save_scanned(scanned)
    
    return results

# --- 启动 ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
