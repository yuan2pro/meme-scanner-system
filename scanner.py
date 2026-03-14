#!/usr/bin/env python3
"""
Meme Scanner - 简化版（集成原始脚本逻辑）
数据源：Ave.ai API
"""

import json
import asyncio
import aiohttp
import time
import os
from datetime import datetime

# Ave.ai API 配置
AVE_API_KEY = os.getenv("AVE_API_KEY", "uHxe2IxOYEx3vHNpUpPtVDJVd2UTPycHLimZkAIpyMxkGS9GE84tf05VU96Uwgdm")
AVE_API_BASE = os.getenv("AVE_API_BASE", "https://prod.ave-api.com")

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULTS_FILE = os.path.join(DATA_DIR, "latest_results.json")
SCANNED_FILE = os.path.join(DATA_DIR, "scanned_tokens.json")

# 筛选条件
MIN_MCAP = 10000        # $10K
MAX_MCAP = 5000000      # $5M
MIN_LIQUIDITY = 4000    # $4K
MIN_HOLDERS = 50
MIN_CHANGE_24H = 100    # 100%

os.makedirs(DATA_DIR, exist_ok=True)

def fmt_num(n):
    if n is None: return "N/A"
    n = float(n)
    if n >= 1e9: return f"${n/1e9:.2f}B"
    if n >= 1e6: return f"${n/1e6:.2f}M"
    if n >= 1e3: return f"${n/1e3:.1f}K"
    return f"${n:.2f}"

def fmt_pct(p):
    if p is None: return "N/A"
    return f"{'+' if float(p)>=0 else ''}{float(p):.2f}%"

def load_scanned():
    if os.path.exists(SCANNED_FILE):
        with open(SCANNED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_scanned(data):
    with open(SCANNED_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def save_results(data):
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

async def scan_ave(session, chain: str) -> list:
    """从 Ave.ai 扫描"""
    tokens = []
    # 使用正确的 API 端点
    url = f"https://api.ave.ai/v1/market/trending?chain={chain}"
    headers = {
        "Authorization": f"Bearer {AVE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with session.get(url, headers=headers, timeout=30) as resp:
            text = await resp.text()
            if resp.status == 200:
                try:
                    data = json.loads(text)
                    if data.get('success') and data.get('data'):
                        for item in data['data']:
                            mcap = item.get('marketCap', 0)
                            liquidity = item.get('liquidity', 0)
                            holders = item.get('holders', 0)
                            change_24h = item.get('priceChange24h', 0)
                            
                            # 筛选
                            if (MIN_MCAP <= mcap <= MAX_MCAP and
                                liquidity >= MIN_LIQUIDITY and
                                holders >= MIN_HOLDERS and
                                change_24h >= MIN_CHANGE_24H):
                                
                                tokens.append({
                                    "symbol": item.get('symbol', 'UNKNOWN'),
                                    "name": item.get('name', 'Unknown'),
                                    "address": item.get('address'),
                                    "chain": chain,
                                    "price": item.get('price', 0),
                                    "market_cap": mcap,
                                    "liquidity": liquidity,
                                    "holders": holders,
                                    "price_change_24h": change_24h,
                                    "volume_24h": item.get('volume24h', 0),
                                    "created_at": datetime.now().isoformat()
                                })
                except json.JSONDecodeError:
                    print(f"⚠️  {chain} API 返回非 JSON: {text[:100]}")
            else:
                print(f"⚠️  {chain} API 状态码：{resp.status}")
    except Exception as e:
        print(f"❌ Ave {chain} 扫描失败：{e}")
    
    return tokens

async def run_scan():
    """执行扫描"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Meme Scanner 启动...")
    
    all_tokens = []
    scanned = load_scanned()
    
    async with aiohttp.ClientSession() as session:
        # 扫描 SOL 和 BSC
        for chain in ['sol', 'bsc']:
            tokens = await scan_ave(session, chain)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Ave {chain}: 获取 {len(tokens)} 个代币")
            all_tokens.extend(tokens)
    
    # 去重
    seen = set()
    unique_tokens = []
    for token in all_tokens:
        key = f"{token['chain']}_{token['address']}"
        if key not in seen:
            seen.add(key)
            unique_tokens.append(token)
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
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 去重后共 {len(unique_tokens)} 个代币")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 扫描完成！")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_scan())
