#!/bin/bash
# Meme Scanner 完整部署脚本

set -e

echo "🚀 Meme Scanner 完整部署"
echo "=========================="
echo ""

cd /home/n100/.openclaw/workspace/meme-scanner-system

# 停止旧容器
echo "🛑 停止旧服务..."
sudo docker compose down 2>/dev/null || true

# 构建镜像
echo "🔨 构建 Docker 镜像..."
sudo docker compose build

# 启动服务
echo "🚀 启动服务..."
sudo docker compose up -d

# 等待启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查状态
echo "📊 检查服务状态..."
sudo docker compose ps

echo ""
if curl -s http://localhost:8000/api/status > /dev/null; then
    echo "✅ 部署成功！"
    echo ""
    echo "🌐 访问地址：http://localhost:8000"
    echo "📋 API 文档：http://localhost:8000/docs"
    echo ""
    echo "🔧 手动扫描:"
    echo "  sudo docker compose run --rm scanner"
    echo ""
    echo "📋 常用命令:"
    echo "  查看日志：sudo docker compose logs -f"
    echo "  停止服务：sudo docker compose down"
    echo "  重启服务：sudo docker compose restart"
else
    echo "⚠️ 服务可能还未完全启动，请稍后访问 http://localhost:8000"
fi
