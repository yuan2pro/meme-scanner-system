# 🔍 Meme Scanner System

智能 Meme 币扫描与分析系统 - 自动发现链上机会，实时追踪热门代币

![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

## ✨ 功能特性

- 🚀 **实时扫描**: 从 Ave.ai 自动扫描热门代币
- ⛓️ **多链支持**: SOL (Solana)、BSC (Binance Smart Chain)
- 📊 **智能筛选**: 市值、流动性、持有者、涨幅等多维度筛选
- 🎨 **现代前端**: Vue.js 3 驱动的响应式仪表盘
- ⚙️ **灵活配置**: 可自定义筛选条件
- 📈 **历史记录**: 追踪所有扫描过的代币
- 🐳 **Docker 部署**: 一键启动，开箱即用

## 🏗️ 项目结构

```
meme-scanner-system/
├── backend/
│   ├── main.py              # FastAPI 后端服务
│   └── requirements.txt     # Python 依赖
├── frontend/
│   └── index.html           # Vue.js 3 前端界面
├── data/                     # 数据目录（运行时生成）
├── scanner.py               # 扫描脚本
├── Dockerfile               # Docker 镜像配置
├── docker-compose.yml       # Docker 编排配置
├── deploy-full.sh          # 一键部署脚本
├── API_CONFIG.md           # API 配置指南
└── README.md               # 本文档
```

## 🚀 快速开始

### 方式一：Docker 部署（推荐）⭐

```bash
# 1. 克隆项目
git clone https://github.com/YOUR_USERNAME/meme-scanner-system.git
cd meme-scanner-system

# 2. 一键部署
chmod +x deploy-full.sh
./deploy-full.sh

# 3. 访问前端
# 打开浏览器访问：http://localhost:8000
```

### 方式二：手动部署

```bash
# 1. 安装依赖
cd backend
pip3 install -r requirements.txt

# 2. 启动后端服务
python3 main.py

# 3. 运行扫描
cd ..
python3 scanner.py

# 4. 访问前端
# 打开浏览器访问：http://localhost:8000
```

## 🌐 访问地址

- **前端界面**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **API 状态**: http://localhost:8000/api/status

## ⚙️ 配置说明

### 筛选条件（默认值）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| min_mcap | $10,000 | 最小市值 |
| max_mcap | $5,000,000 | 最大市值 |
| min_liquidity | $4,000 | 最小流动性 |
| min_holders | 50 | 最小持有者数 |
| min_change_24h | 50% | 最小 24h 涨幅 |
| scan_interval_minutes | 5 | 扫描间隔 |

### API 配置

编辑 `docker-compose.yml` 添加环境变量：

```yaml
environment:
  - AVE_API_KEY=你的_API_Key
  - AVE_API_BASE=https://prod.ave-api.com
```

**获取 API Key：**
1. 访问 [Ave.ai](https://ave.ai)
2. 注册账号
3. 进入开发者中心获取 API Key

## 🛠️ API 接口

### GET /api/status
获取系统状态

```bash
curl http://localhost:8000/api/status
```

### GET /api/results
获取最新扫描结果

```bash
curl http://localhost:8000/api/results
```

### GET /api/tokens
获取代币列表

```bash
curl http://localhost:8000/api/tokens
```

### POST /api/scan
触发手动扫描

```bash
curl -X POST http://localhost:8000/api/scan
```

### GET /api/config
获取当前配置

```bash
curl http://localhost:8000/api/config
```

### POST /api/config
更新配置

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"min_mcap": 50000}' \
  http://localhost:8000/api/config
```

## 📊 数据示例

```json
{
  "tokens": [
    {
      "symbol": "R.S UGOR",
      "name": "UGOR",
      "address": "8M5LMCLUAAMDsy4xq6xaxVs2UcMNe1XKBtKTZZKuvvCW",
      "chain": "sol",
      "price": 0.033509,
      "market_cap": 3350899973.89,
      "liquidity": 23810.48,
      "holders": 204,
      "price_change_24h": 525.96,
      "volume_24h": 55907477.49
    }
  ],
  "last_scan": "2026-03-14T09:09:13",
  "total_found": 100
}
```

## 🔧 常用命令

### Docker 管理

```bash
# 查看状态
docker compose ps

# 查看日志
docker compose logs -f

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 重新构建
docker compose build --no-cache
```

### 手动扫描

```bash
# 运行一次扫描
docker compose exec meme-scanner python3 scanner.py

# 或在宿主机运行
python3 scanner.py
```

## 📝 技术栈

- **后端**: FastAPI + Python 3.11
- **前端**: Vue.js 3 + Axios
- **数据源**: Ave.ai API
- **部署**: Docker + Docker Compose
- **UI**: 自定义 CSS（深色主题）

## ⚠️ 风险提示

1. **本系统仅供学习研究使用**
2. **Meme 币风险极高，请谨慎投资**
3. **不构成任何投资建议**
4. **请自行做好研究（DYOR）**

## 🔒 注意事项

1. 确保网络环境可以访问 Ave.ai API
2. Docker 部署需确保 8000 端口未被占用
3. 建议定期更新 API Key
4. 数据文件自动保存在 `data/` 目录

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 项目地址：https://github.com/YOUR_USERNAME/meme-scanner-system
- 问题反馈：https://github.com/YOUR_USERNAME/meme-scanner-system/issues

## 🙏 致谢

感谢以下项目和服务：

- [Ave.ai](https://ave.ai) - 提供代币数据 API
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架

---

**⚠️ 免责声明**: 本项目仅供学习和研究使用。使用本系统进行交易所产生的任何风险由用户自行承担。作者不对任何损失负责。

**📅 最后更新**: 2026-03-14
