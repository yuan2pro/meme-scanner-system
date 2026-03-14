# 📤 上传到 GitHub 指南

## 方式一：使用 GitHub CLI（推荐）⭐

### 1. 安装 GitHub CLI

```bash
# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# 验证安装
gh --version
```

### 2. 登录 GitHub

```bash
gh auth login
```

按提示操作：
- GitHub.com: 按 Enter
- SSH: 选择 HTTPS
- Login: 选择 "Paste an authentication token"
- 输入 Token（见下方获取方法）

### 3. 创建并推送仓库

```bash
cd /home/n100/.openclaw/workspace/meme-scanner-system

# 创建仓库
gh repo create meme-scanner-system --public --source=. --push

# 完成！
```

---

## 方式二：使用 Personal Access Token

### 1. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写说明（如：meme-scanner-upload）
4. 勾选权限：`repo`（全选）
5. 点击 "Generate token"
6. **复制 Token（只显示一次！）**

### 2. 使用 Token 推送

```bash
cd /home/n100/.openclaw/workspace/meme-scanner-system

# 在 GitHub 上手动创建仓库（命名为 meme-scanner-system）
# 访问：https://github.com/new

# 关联远程仓库
git remote add origin https://github.com/yuan2pro/meme-scanner-system.git

# 推送（替换 YOUR_TOKEN 为你的 Token）
git branch -M main
git push -u origin main
```

或者使用带凭证的 URL：
```bash
git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/yuan2pro/meme-scanner-system.git
git push -u origin main
```

---

## 方式三：使用 SSH

### 1. 生成 SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加 SSH Key 到 GitHub

```bash
# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制输出内容
```

1. 访问 https://github.com/settings/keys
2. 点击 "New SSH key"
3. 粘贴公钥内容
4. 保存

### 3. 使用 SSH 推送

```bash
cd /home/n100/.openclaw/workspace/meme-scanner-system

# 关联 SSH 远程仓库
git remote add origin git@github.com:yuan2pro/meme-scanner-system.git

# 推送
git branch -M main
git push -u origin main
```

---

## ✅ 验证上传

上传成功后访问：
**https://github.com/yuan2pro/meme-scanner-system**

---

## 🔒 安全提示

- ⚠️ **不要分享你的 Token**
- ⚠️ **不要将 Token 提交到 Git**
- ✅ Token 已保存在本地，不会上传
- ✅ 项目使用 MIT 许可证，可安全开源

---

## 📋 上传检查清单

- [ ] 已安装 GitHub CLI 或配置 Git
- [ ] 已获取 GitHub Token 或配置 SSH
- [ ] 已在 GitHub 创建仓库（如使用 HTTPS）
- [ ] 已执行推送命令
- [ ] 验证仓库页面显示代码

---

**需要帮助？** 执行以下命令自动检查：

```bash
cd /home/n100/.openclaw/workspace/meme-scanner-system
git status
git log --oneline -5
```
