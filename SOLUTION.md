# 🔍 Meme Scanner 数据源解决方案

## ⚠️ 当前问题

**gmgn.ai 和 Ave.ai 都有防护：**
- gmgn.ai: Cloudflare 防护，需要浏览器访问
- Ave.ai: API 端点失效/需要正式 Key

## ✅ 解决方案

### 方案一：添加本地浏览器支持（推荐）

在宿主机上运行扫描脚本，使用已有的 Chrome 浏览器：

```bash
# 1. 确保 Chrome/Chromium 已安装
google-chrome --version

# 2. 运行原始扫描脚本
cd /home/n100/.openclaw/workspace/skills/temp-skills/skills/hanguang254/meme-scanner/scripts
python3 meme_scanner.py
```

### 方案二：使用其他免费 API

可以考虑集成以下数据源：
- **DexScreener**: https://api.dexscreener.com/latest/dex/tokens/{chain}
- **Birdeye**: https://public-api.birdeye.so/defi/token_list
- **GeckoTerminal**: https://api.coingecko.com/api/v3/simple/token_price

### 方案三：前端直接调用（CORS 允许的话）

修改前端直接调用 gmgn.ai API（需要测试 CORS）

## 🚀 快速开始（使用现有脚本）

原始的 meme_scanner.py 已经支持：
- ✅ Chrome DevTools Protocol
- ✅ gmgn.ai + Ave.ai 双数据源
- ✅ Telegram 推送

**运行方式：**
```bash
cd /home/n100/.openclaw/workspace/skills/temp-skills/skills/hanguang254/meme-scanner/scripts
python3 meme_scanner.py
```

## 📊 当前系统状态

- ✅ Docker 容器运行正常
- ✅ 前端页面可访问
- ⚠️ API 数据源需要浏览器支持

---

**建议：** 使用原始 meme_scanner.py 脚本进行扫描，新系统作为展示界面。
