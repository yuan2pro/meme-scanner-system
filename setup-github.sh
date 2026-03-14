#!/bin/bash
# GitHub 一键上传脚本

set -e

echo "📤 Meme Scanner - GitHub 上传助手"
echo "=================================="
echo ""

cd /home/n100/.openclaw/workspace/meme-scanner-system

# 检查 Git
if ! git --version > /dev/null 2>&1; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

echo "✅ Git 已安装: $(git --version)"
echo ""

# 检查是否已安装 GitHub CLI
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI 已安装"
    echo ""
    
    # 检查是否已登录
    if gh auth status &> /dev/null; then
        echo "✅ 已登录 GitHub"
        
        # 创建并推送
        echo ""
        echo "🚀 创建仓库并推送..."
        gh repo create meme-scanner-system --public --source=. --push
        
        echo ""
        echo "✅ 上传成功！"
        echo "🌐 访问：https://github.com/yuan2pro/meme-scanner-system"
        exit 0
    else
        echo "⚠️  未登录 GitHub"
        echo ""
        echo "开始登录..."
        gh auth login
        
        # 重试创建
        gh repo create meme-scanner-system --public --source=. --push
        
        echo ""
        echo "✅ 上传成功！"
        echo "🌐 访问：https://github.com/yuan2pro/meme-scanner-system"
        exit 0
    fi
else
    echo "❌ GitHub CLI 未安装"
    echo ""
    echo "请选择上传方式:"
    echo ""
    echo "1️⃣  安装 GitHub CLI（推荐）"
    echo "2️⃣  使用 Personal Access Token"
    echo "3️⃣  使用 SSH"
    echo "4️⃣  查看手动上传指南"
    echo ""
    read -p "请选择 (1-4): " choice
    
    case $choice in
        1)
            echo ""
            echo "🔧 安装 GitHub CLI..."
            
            # 检测系统
            if [ -f /etc/debian_version ]; then
                echo "检测到 Debian/Ubuntu 系统"
                curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
                echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
                sudo apt update
                sudo apt install gh -y
                
                echo ""
                echo "✅ GitHub CLI 安装完成"
                echo ""
                echo "现在重新运行此脚本："
                echo "./setup-github.sh"
            else
                echo "请手动安装 GitHub CLI："
                echo "https://github.com/cli/cli#installation"
            fi
            ;;
        2)
            echo ""
            echo "📝 使用 Personal Access Token 上传："
            echo ""
            echo "1. 访问：https://github.com/settings/tokens"
            echo "2. 生成新 Token（勾选 repo 权限）"
            echo "3. 复制 Token"
            echo ""
            read -p "输入你的 GitHub Token: " -s token
            echo ""
            
            # 移除已存在的 remote
            git remote remove origin 2>/dev/null || true
            
            # 添加 remote
            git remote add origin https://github.com/yuan2pro/meme-scanner-system.git
            
            # 推送
            echo ""
            echo "🚀 推送中..."
            git branch -M main
            GIT_ASKPASS=echo git push -u origin main
            
            echo ""
            echo "✅ 上传成功！"
            echo "🌐 访问：https://github.com/yuan2pro/meme-scanner-system"
            ;;
        3)
            echo ""
            echo "🔑 使用 SSH 上传："
            echo ""
            
            # 检查 SSH key
            if [ ! -f ~/.ssh/id_ed25519.pub ]; then
                echo "生成 SSH Key..."
                ssh-keygen -t ed25519 -C "yuan2pro@users.noreply.github.com"
            fi
            
            echo ""
            echo "公钥内容："
            cat ~/.ssh/id_ed25519.pub
            echo ""
            echo "请复制以上内容，添加到："
            echo "https://github.com/settings/keys"
            echo ""
            read -p "添加完成后按 Enter 继续..."
            
            # 移除已存在的 remote
            git remote remove origin 2>/dev/null || true
            
            # 添加 SSH remote
            git remote add origin git@github.com:yuan2pro/meme-scanner-system.git
            
            # 测试 SSH
            echo ""
            echo "测试 SSH 连接..."
            ssh -T git@github.com || true
            
            # 推送
            echo ""
            echo "🚀 推送中..."
            git branch -M main
            git push -u origin main
            
            echo ""
            echo "✅ 上传成功！"
            echo "🌐 访问：https://github.com/yuan2pro/meme-scanner-system"
            ;;
        4)
            echo ""
            echo "📖 查看上传指南："
            echo "cat UPLOAD_TO_GITHUB.md"
            echo ""
            cat UPLOAD_TO_GITHUB.md
            ;;
        *)
            echo "无效选择"
            exit 1
            ;;
    esac
fi
