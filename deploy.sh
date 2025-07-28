#!/bin/bash

echo "🧘 AIカウンセラーBOTのデプロイスクリプト"
echo "=================================="

# 色の定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Gitの初期化確認
echo -e "${BLUE}1. Gitリポジトリの確認...${NC}"
if [ ! -d .git ]; then
    git init
    echo -e "${GREEN}✓ Gitリポジトリを初期化しました${NC}"
else
    echo -e "${GREEN}✓ Gitリポジトリは既に初期化されています${NC}"
fi

# 2. GitHubリモートの設定
echo -e "\n${BLUE}2. GitHubリモートリポジトリの設定${NC}"
echo -e "${YELLOW}GitHubでリポジトリを作成してください:${NC}"
echo "リポジトリ名の推奨: ai-counselor-bot"
echo ""
read -p "GitHubリポジトリのURLを入力してください (例: https://github.com/username/repo.git): " REPO_URL

if [ ! -z "$REPO_URL" ]; then
    git remote add origin $REPO_URL 2>/dev/null || git remote set-url origin $REPO_URL
    echo -e "${GREEN}✓ リモートリポジトリを設定しました${NC}"
fi

# 3. ファイルの追加とコミット
echo -e "\n${BLUE}3. ファイルのコミット...${NC}"
git add .
git commit -m "Initial commit: AI Counselor Bot with Carl Rogers' approach" 2>/dev/null || echo "既にコミット済みです"

# 4. GitHubへのプッシュ
echo -e "\n${BLUE}4. GitHubへのプッシュ...${NC}"
git branch -M main
git push -u origin main

echo -e "${GREEN}✓ GitHubへのプッシュが完了しました${NC}"

# 5. Streamlit Cloudへのデプロイ手順
echo -e "\n${BLUE}5. Streamlit Cloudへのデプロイ手順${NC}"
echo "=================================="
echo "1. https://share.streamlit.io/ にアクセス"
echo "2. GitHubアカウントでログイン"
echo "3. 'New app'をクリック"
echo "4. 以下の情報を入力:"
echo "   - Repository: $REPO_URL"
echo "   - Branch: main"
echo "   - Main file path: app.py"
echo ""
echo "5. 'Advanced settings'を開き、'Secrets'に以下を追加:"
echo -e "${YELLOW}GEMINI_API_KEY = \"your-api-key-here\"${NC}"
echo ""
echo "6. 'Deploy!'をクリック"

echo -e "\n${GREEN}✅ デプロイの準備が完了しました！${NC}"
echo "上記の手順に従ってStreamlit Cloudでデプロイしてください。"