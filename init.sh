#!/bin/bash
# 初始化并推送到 GitHub

set -e

echo "🔧 初始化项目到 GitHub..."

# 1. 检查 GitHub Token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 请设置 GITHUB_TOKEN 环境变量"
    echo "   export GITHUB_TOKEN=your_token_here"
    exit 1
fi

# 2. 克隆本地仓库 (先假设 repo 不存在)
REPO_NAME="content-pipeline"
USER_NAME=$(git config user.name || whoami)

# 3. 通过 API 创建远程仓库
echo "📦 创建 GitHub 仓库: $USER_NAME/$REPO_NAME"
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"private\":false,\"auto_init\":true}"

# 4. 初始化 Git
git init
git branch -M main
git remote add origin https://github.com/$USER_NAME/$REPO_NAME.git
git add .
git commit -m "feat: AI 内容生产流水线 v0.1.0"
git push -u origin main --force

echo ""
echo "✅ 项目已初始化！"
echo "📍 Repository: https://github.com/$USER_NAME/$REPO_NAME"
echo ""
echo "👉 下一步:"
echo "   1. 编辑 .env 配置你的 API Keys"
echo "   2. pip install -r requirements.txt"
echo "   3. python src/main.py --help"
