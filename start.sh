#!/bin/bash
# Meme Scanner System 启动脚本

echo "🚀 启动 Meme Scanner 系统..."

# 检查 Python 依赖
echo "📦 检查 Python 依赖..."
cd /home/n100/.openclaw/workspace/meme-scanner-system/backend
pip3 install -r requirements.txt -q

# 启动后端
echo "🔧 启动后端服务..."
cd /home/n100/.openclaw/workspace/meme-scanner-system/backend
python3 main.py &
BACKEND_PID=$!

echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
echo "🌐 访问前端：http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待中断
wait $BACKEND_PID
