# Ave API 测试结果

## 📊 测试时间
2026-03-14 08:42 (Asia/Shanghai)

## 🔍 测试过程

### 测试 1: prod.ave-api.com
```bash
curl -s "https://prod.ave-api.com/v1/market/trending?chain=sol" \
  -H "Authorization: Bearer [API_KEY]"
```
**结果:** ❌ 404 Not Found

### 测试 2: api.ave.ai
```bash
curl -s "https://api.ave.ai/v1/market/trending?chain=sol" \
  -H "Authorization: Bearer [API_KEY]"
```
**结果:** ❌ 连接失败 (SSL 握手超时)

## ⚠️ 问题分析

1. **API 端点可能已变更** - Ave.ai 可能更新了 API 地址
2. **API Key 可能无效** - 当前配置的是示例 Key
3. **需要注册获取正式 Key** - 可能需要到 Ave.ai 官网申请

## ✅ 解决方案

### 方案一：获取正式 API Key（推荐）

1. 访问 [Ave.ai](https://ave.ai)
2. 注册账号
3. 进入开发者中心申请 API Key
4. 更新 `data/config.env` 配置

### 方案二：使用 gmgn.ai（当前可用）

系统已经集成了 gmgn.ai 数据源，无需 API Key 即可使用！

gmgn.ai 接口：
- `https://gmgn.ai/defi/quotation/v1/rank/{chain}/swaps/1h`
- 支持 SOL、BSC 链
- 无需认证

### 方案三：双数据源配置

在 `data/config.env` 中配置：

```bash
# Ave API（可选）
AVE_API_KEY=你的正式 Key
AVE_API_BASE=https://new-api.ave.ai

# 启用/禁用数据源
ENABLE_AVE=false
ENABLE_GMGN=true
```

## 📝 当前状态

- ✅ **gmgn.ai**: 正常工作
- ⚠️ **Ave API**: 需要更新配置

## 🚀 下一步

1. 如果只需要扫描功能，可以直接使用（gmgn.ai 已可用）
2. 如果需要 Ave 数据，请获取正式 API Key 后更新配置
3. 重启容器：`sudo docker compose restart`

---

**提示:** 点击前端"立即扫描"按钮即可开始扫描（使用 gmgn.ai 数据源）！
