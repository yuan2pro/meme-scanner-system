# 🔍 Meme Scanner System

智能 Meme 币扫描与分析系统 - 自动发现链上机会

## ✨ 功能特性

- 🚀 **实时扫描**: 从 gmgn.ai 和 Ave.ai 自动扫描热门代币
- ⛓️ **多链支持**: SOL、BSC 链
- 📊 **智能筛选**: 市值、流动性、持有者、涨幅等多维度筛选
- 🎨 **现代前端**: Vue.js 驱动的响应式仪表盘
- ⚙️ **灵活配置**: 可自定义筛选条件
- 📈 **历史记录**: 追踪所有扫描过的代币

## 🏗️ 项目结构

```
meme-scanner-system/
├── backend/
│   ├── main.py              # FastAPI 后端
│   └── requirements.txt     # Python 依赖
├── frontend/
│   └── index.html           # Vue.js 前端
├── data/                     # 数据文件 (运行时生成)
├── Dockerfile               # Docker 镜像配置
├── docker-compose.yml       # Docker Compose 配置
├── deploy.sh                # Docker 部署脚本
├── start.sh                 # 本地启动脚本
├── .dockerignore           # Docker 忽略文件
├── .gitignore              # Git 忽略文件
└── README.md               # 本文档
```

## 🚀 快速开始

### 方式一：Docker 部署（推荐）⭐

```bash
# 一键部署
./deploy.sh

# 或手动执行
docker-compose up -d
```

### 方式二：本地运行

```bash
# 1. 安装依赖
cd backend
pip3 install -r requirements.txt

# 2. 启动服务
python3 main.py
```

### 3. 访问前端

打开浏览器访问：**http://localhost:8000**

**📋 API 文档：** http://localhost:8000/docs

## ⚙️ 配置说明

### 筛选条件

| 参数 | 默认值 | 说明 |
|------|--------|------|
| min_mcap | $10,000 | 最小市值 |
| max_mcap | $5,000,000 | 最大市值 |
| min_liquidity | $4,000 | 最小流动性 |
| min_holders | 50 | 最小持有者数 |
| min_change_24h | 100% | 最小 24h 涨幅 |
| scan_interval_minutes | 5 | 扫描间隔 |

### 数据文件

- `data/scanned_tokens.json` - 已扫描代币记录
- `data/latest_results.json` - 最新扫描结果
- `data/config.json` - 用户配置

## 🛠️ API 接口

### GET /api/status
获取系统状态

### GET /api/config
获取当前配置

### POST /api/config
更新配置

### GET /api/results
获取最新扫描结果

### POST /api/scan
触发手动扫描

### GET /api/tokens
获取代币列表

## 🐳 Docker 部署

### 一键部署

```bash
./deploy.sh
```

### 手动部署

```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d

# 查看日志
docker logs -f meme-scanner

# 停止服务
docker-compose down
```

### 数据持久化

数据自动挂载到 `./data` 目录，容器删除后数据不丢失。

### 常用命令

```bash
# 查看状态
docker-compose ps

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build

# 查看资源使用
docker stats meme-scanner
```

## 🔒 注意事项

1. 本系统仅供学习研究使用
2. Meme 币风险极高，请谨慎投资
3. 确保网络环境可以访问 gmgn.ai 和 Ave.ai
4. Docker 部署需确保 8000 端口未被占用

## 📝 技术栈

- **后端**: FastAPI + Python 3
- **前端**: Vue.js 3 + Axios
- **数据源**: gmgn.ai, Ave.ai
- **UI**: 自定义 CSS
- **部署**: Docker + Docker Compose

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License
