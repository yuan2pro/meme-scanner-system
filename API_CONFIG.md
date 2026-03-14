# Ave.ai API 配置指南

## 📋 获取 API Key

1. 访问 [Ave.ai](https://ave.ai)
2. 注册/登录账号
3. 进入开发者中心获取 API Key

## ⚙️ 配置方式

### 方式一：环境变量（推荐）

编辑 `data/config.env` 文件：

```bash
AVE_API_KEY=你的 API_Key
AVE_API_BASE=https://prod.ave-api.com
```

### 方式二：Docker 环境变量

在 `docker-compose.yml` 中添加：

```yaml
environment:
  - AVE_API_KEY=你的 API_Key
  - AVE_API_BASE=https://prod.ave-api.com
```

### 方式三：直接修改代码（不推荐）

编辑 `backend/main.py`，修改 `AVE_API_KEY` 变量。

## 🧪 测试 API

### 使用测试脚本

```bash
cd backend
pip install requests python-dotenv
python api_test.py
```

### 使用 curl 测试

```bash
# SOL 链热门代币
curl -X GET "https://prod.ave-api.com/v1/market/trending?chain=sol" \
  -H "Authorization: Bearer 你的_API_Key"

# BSC 链热门代币
curl -X GET "https://prod.ave-api.com/v1/market/trending?chain=bsc" \
  -H "Authorization: Bearer 你的_API_Key"
```

## 📊 API 接口

### 热门代币列表

**端点：** `GET /v1/market/trending`

**参数：**
- `chain` (必填): 链名称 (sol, bsc, eth, 等)

**响应示例：**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "TOKEN",
      "name": "Token Name",
      "address": "0x...",
      "price": 0.001,
      "marketCap": 100000,
      "liquidity": 50000,
      "holders": 1000,
      "priceChange24h": 150.5,
      "volume24h": 200000
    }
  ]
}
```

## 🔧 重新部署

修改配置后重新构建：

```bash
cd /home/n100/.openclaw/workspace/meme-scanner-system

# 停止容器
sudo docker compose down

# 重新构建
sudo docker compose build --no-cache

# 启动
sudo docker compose up -d

# 查看日志
sudo docker logs -f meme-scanner
```

## ⚠️ 常见问题

### 1. 401 Unauthorized
- API Key 无效或过期
- 检查是否正确配置环境变量

### 2. 429 Too Many Requests
- 请求频率超限
- 增加扫描间隔时间

### 3. 连接超时
- 检查网络连接
- 确认 API Base URL 正确

## 📝 当前配置

- **API Key:** 已配置 (默认值)
- **API Base:** https://prod.ave-api.com
- **支持链:** SOL, BSC

---

**提示:** 如果默认 API Key 无法使用，请获取自己的 API Key 并更新配置。
