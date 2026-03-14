#!/bin/bash
# 快速推送到 GitHub

echo "📤 Meme Scanner - 快速推送到 GitHub"
echo "===================================="
echo ""

cd /home/n100/.openclaw/workspace/meme-scanner-system

# 检查 Git 状态
echo "📊 Git 状态:"
git status -s
echo ""

# 显示最近的提交
echo "📝 最近提交:"
git log --oneline -5
echo ""

# 检查远程仓库
echo "🔗 远程仓库:"
git remote -v
echo ""

echo "✅ 准备推送!"
echo ""
echo "请按以下步骤操作:"
echo ""
echo "1️⃣  在 GitHub 创建仓库"
echo "   访问：https://github.com/new"
echo "   仓库名：meme-scanner-system"
echo "   选择：Public"
echo "   不要初始化 README"
echo ""
echo "2️⃣  运行推送命令:"
echo "   git push -u origin main"
echo ""
echo "3️⃣  输入 GitHub 用户名和密码（或 Token）"
echo ""
echo "4️⃣  完成！访问："
echo "   https://github.com/yuan2pro/meme-scanner-system"
echo ""

# 询问是否现在推送
read -p "是否现在推送？(y/n): " choice

if [ "$choice" = "y" ]; then
    echo ""
    echo "🚀 推送中..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 推送成功！"
        echo "🌐 访问：https://github.com/yuan2pro/meme-scanner-system"
    else
        echo ""
        echo "❌ 推送失败"
        echo ""
        echo "可能的原因:"
        echo "1. 仓库不存在 - 请先到 GitHub 创建仓库"
        echo "2. 认证失败 - 请使用 Token 代替密码"
        echo ""
        echo "获取 Token: https://github.com/settings/tokens"
    fi
else
    echo "好的，你可以稍后手动执行:"
    echo "git push -u origin main"
fi
