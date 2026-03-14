#!/bin/bash
# Meme Scanner Docker 部署脚本

set -e

echo "🐳 Meme Scanner Docker 部署"
echo "=============================="
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装"
    exit 1
fi

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p data

# 构建镜像
echo "🔨 构建 Docker 镜像..."
if docker compose version &> /dev/null; then
    docker compose build
else
    docker-compose build
fi

# 启动容器
echo "🚀 启动容器..."
if docker compose version &> /dev/null; then
    docker compose up -d
else
    docker-compose up -d
fi

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查状态
echo "📊 检查服务状态..."
if curl -s http://localhost:8000/api/status > /dev/null; then
    echo ""
    echo "✅ 部署成功！"
    echo ""
    echo "🌐 访问地址：http://localhost:8000"
    echo "📋 API 文档：http://localhost:8000/docs"
    echo ""
    echo "🔧 常用命令:"
    echo "  查看日志：docker logs -f meme-scanner"
    echo "  停止服务：docker compose down"
    echo "  重启服务：docker compose restart"
    echo "  查看状态：docker compose ps"
else
    echo "⚠️  服务可能还未完全启动，请稍后访问 http://localhost:8000"
fi
