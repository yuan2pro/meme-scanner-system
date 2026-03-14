#!/usr/bin/env python3
"""
Ave.ai API 测试工具
用于验证 API Key 是否有效
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

AVE_API_KEY = os.getenv("AVE_API_KEY")
AVE_API_BASE = os.getenv("AVE_API_BASE", "https://prod.ave-api.com")

def test_api():
    """测试 Ave.ai API"""
    print("🔍 测试 Ave.ai API 连接...")
    print(f"API Base: {AVE_API_BASE}")
    print(f"API Key: {AVE_API_KEY[:10]}...{AVE_API_KEY[-10:] if len(AVE_API_KEY) > 20 else '***'}")
    print("")
    
    # 测试 trending 接口
    chains = ["sol", "bsc", "eth"]
    
    for chain in chains:
        print(f"📊 测试 {chain.upper()} 链...")
        url = f"{AVE_API_BASE}/v1/market/trending?chain={chain}"
        headers = {"Authorization": f"Bearer {AVE_API_KEY}"}
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"  状态码：{resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    tokens = data.get('data', [])
                    print(f"  ✅ 成功！获取到 {len(tokens)} 个热门代币")
                    if tokens:
                        print(f"  示例：{tokens[0].get('symbol', 'N/A')} - {tokens[0].get('name', 'N/A')}")
                else:
                    print(f"  ❌ API 返回错误：{data}")
            elif resp.status_code == 401:
                print(f"  ❌ 认证失败：API Key 无效")
            elif resp.status_code == 429:
                print(f"  ⚠️  请求频率超限")
            else:
                print(f"  ❌ 未知错误：{resp.text[:200]}")
        except Exception as e:
            print(f"  ❌ 请求失败：{e}")
        print("")

if __name__ == "__main__":
    test_api()
