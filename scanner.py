#!/usr/bin/env python3
"""
Meme Scanner - Token scanner for Solana and BSC chains.
Data source: Ave.ai API
"""

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any

import aiohttp

# ============================================================================
# Configuration
# ============================================================================
AVE_API_KEY = os.getenv(
    "AVE_API_KEY",
    "uHxe2IxOYEx3vHNpUpPtVDJVd2UTPycHLimZkAIpyMxkGS9GE84tf05VU96Uwgdm"
)
AVE_API_BASE = os.getenv("AVE_API_BASE", "https://prod.ave-api.com")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULTS_FILE = os.path.join(DATA_DIR, "latest_results.json")
SCANNED_FILE = os.path.join(DATA_DIR, "scanned_tokens.json")

# Screening criteria
MIN_MCAP = 10_000  # $10K
MAX_MCAP = 5_000_000  # $5M
MIN_LIQUIDITY = 4_000  # $4K
MIN_HOLDERS = 50
MIN_CHANGE_24H = 100  # 100%

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================================
# Helper Functions
# ============================================================================

def format_number(n: float | None) -> str:
    """
    Format number with K/M/B suffix.
    
    Args:
        n: Number to format
    
    Returns:
        Formatted string (e.g., "$1.23M", "$456.78K")
    """
    if n is None:
        return "N/A"
    
    n = float(n)
    if n >= 1e9:
        return f"${n / 1e9:.2f}B"
    if n >= 1e6:
        return f"${n / 1e6:.2f}M"
    if n >= 1e3:
        return f"${n / 1e3:.1f}K"
    return f"${n:.2f}"


def format_percentage(p: float | None) -> str:
    """
    Format percentage with sign.
    
    Args:
        p: Percentage value
    
    Returns:
        Formatted string (e.g., "+12.34%", "-5.67%")
    """
    if p is None:
        return "N/A"
    
    sign = '+' if float(p) >= 0 else ''
    return f"{sign}{float(p):.2f}%"


def load_scanned_tokens() -> Dict[str, Any]:
    """Load previously scanned tokens from file."""
    if os.path.exists(SCANNED_FILE):
        with open(SCANNED_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_scanned_tokens(data: Dict[str, Any]) -> None:
    """Save scanned tokens to file."""
    with open(SCANNED_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def save_scan_results(data: Dict[str, Any]) -> None:
    """Save scan results to file."""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def create_token_item(item: Dict[str, Any], chain: str) -> Dict[str, Any]:
    """
    Create standardized token item from API response.
    
    Args:
        item: Raw API response item
        chain: Blockchain identifier
    
    Returns:
        Standardized token dictionary
    """
    return {
        "symbol": item.get('symbol', 'UNKNOWN'),
        "name": item.get('name', 'Unknown'),
        "address": item.get('address'),
        "chain": chain,
        "price": item.get('price', 0),
        "market_cap": item.get('marketCap', 0),
        "liquidity": item.get('liquidity', 0),
        "holders": item.get('holders', 0),
        "price_change_24h": item.get('priceChange24h', 0),
        "volume_24h": item.get('volume24h', 0),
        "created_at": datetime.now().isoformat()
    }


def meets_screening_criteria(item: Dict[str, Any]) -> bool:
    """
    Check if token meets screening criteria.
    
    Args:
        item: Token data from API
    
    Returns:
        True if token meets all criteria
    """
    mcap = item.get('marketCap', 0)
    liquidity = item.get('liquidity', 0)
    holders = item.get('holders', 0)
    change_24h = item.get('priceChange24h', 0)
    
    return (
        MIN_MCAP <= mcap <= MAX_MCAP and
        liquidity >= MIN_LIQUIDITY and
        holders >= MIN_HOLDERS and
        change_24h >= MIN_CHANGE_24H
    )


# ============================================================================
# Scanner Functions
# ============================================================================

async def scan_ave_chain(session: aiohttp.ClientSession, chain: str) -> List[Dict[str, Any]]:
    """
    Scan tokens from Ave.ai API for a specific chain.
    
    Args:
        session: aiohttp client session
        chain: Blockchain identifier (e.g., 'sol', 'bsc')
    
    Returns:
        List of tokens meeting screening criteria
    """
    tokens = []
    url = f"{AVE_API_BASE}/v1/market/trending?chain={chain}"
    headers = {
        "Authorization": f"Bearer {AVE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        async with session.get(url, headers=headers, timeout=30) as resp:
            text = await resp.text()
            
            if resp.status != 200:
                print(f"⚠️  {chain} API status code: {resp.status}")
                return tokens
            
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                print(f"⚠️  {chain} API returned non-JSON: {text[:100]}")
                return tokens
            
            if not data.get('success') or not data.get('data'):
                return tokens
            
            # Process each token
            for item in data['data']:
                if meets_screening_criteria(item):
                    tokens.append(create_token_item(item, chain))
                    
    except asyncio.TimeoutError:
        print(f"❌ Ave {chain} scan timeout")
    except Exception as e:
        print(f"❌ Ave {chain} scan failed: {e}")
    
    return tokens


async def run_scan() -> Dict[str, Any]:
    """
    Execute token scan across all configured chains.
    
    Returns:
        Scan results dictionary
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] 🚀 Meme Scanner starting...")
    
    all_tokens: List[Dict[str, Any]] = []
    scanned_tokens = load_scanned_tokens()
    
    async with aiohttp.ClientSession() as session:
        # Scan SOL and BSC chains
        for chain in ['sol', 'bsc']:
            tokens = await scan_ave_chain(session, chain)
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] ✅ Ave {chain}: Found {len(tokens)} tokens")
            all_tokens.extend(tokens)
    
    # Remove duplicates
    seen: set = set()
    unique_tokens: List[Dict[str, Any]] = []
    
    for token in all_tokens:
        key = f"{token['chain']}_{token['address']}"
        if key not in seen:
            seen.add(key)
            unique_tokens.append(token)
            scanned_tokens[key] = {
                "timestamp": time.time(),
                "symbol": token['symbol'],
                "chain": token['chain']
            }
    
    # Save results
    results = {
        "tokens": unique_tokens,
        "last_scan": datetime.now().isoformat(),
        "total_found": len(unique_tokens)
    }
    
    save_scan_results(results)
    save_scanned_tokens(scanned_tokens)
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] 📊 Total unique tokens: {len(unique_tokens)}")
    print(f"[{timestamp}] ✅ Scan complete!")
    
    return results


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    asyncio.run(run_scan())
