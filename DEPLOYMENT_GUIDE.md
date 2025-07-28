# 🚀 AIカウンセラーBOT デプロイメントガイド

このガイドでは、AIカウンセラーBOTをGitHubにアップロードし、Streamlit Cloudでデプロイする手順を説明します。

## 📋 前提条件

- GitHubアカウント
- Streamlit Cloudアカウント（GitHubでログイン可能）
- Gemini API Key（[取得はこちら](https://makersuite.google.com/app/apikey)）

## 🔧 手動デプロイ手順

### Step 1: GitHubリポジトリの作成

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を設定:
   - Repository name: `ai-counselor-bot`
   - Description: `AI Counselor Bot based on Carl Rogers' Person-Centered Therapy`
   - Public/Private: お好みで選択
4. 「Create repository」をクリック

### Step 2: ローカルからGitHubへプッシュ

ターミナルで以下のコマンドを実行:

```bash
# プロジェクトディレクトリに移動
cd /Users/shunm/Downloads/obsidian_knowledge/AI-task-manager/completed/ai-counselor-bot

# Gitの初期化
git init

# すべてのファイルを追加
git add .

# 初回コミット
git commit -m "Initial commit: AI Counselor Bot"

# メインブランチに変更
git branch -M main

# リモートリポジトリを追加（URLは自分のものに置き換え）
git remote add origin https://github.com/YOUR_USERNAME/ai-counselor-bot.git

# GitHubにプッシュ
git push -u origin main
```

### Step 3: Streamlit Cloudでデプロイ

1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. GitHubアカウントでログイン
3. 「New app」ボタンをクリック
4. 以下を設定:
   - **Repository**: `YOUR_USERNAME/ai-counselor-bot`
   - **Branch**: `main`
   - **Main file path**: `app.py`

5. 「Advanced settings」を展開
6. 「Secrets」セクションに以下を入力:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

7. 「Deploy!」をクリック

### Step 4: デプロイの確認

- デプロイには数分かかります
- 完了すると、URLが表示されます（例: `https://your-app-name.streamlit.app`）
- アプリにアクセスして動作を確認

## 🔄 更新方法

アプリを更新する場合:

```bash
# 変更をコミット
git add .
git commit -m "Update: 変更内容の説明"

# GitHubにプッシュ
git push

# Streamlit Cloudが自動的に再デプロイします
```

## 🐛 トラブルシューティング

### エラー: "GEMINI_API_KEY not found"
→ Streamlit CloudのSecretsにAPIキーが正しく設定されているか確認

### エラー: "Module not found"
→ `requirements.txt`にすべての必要なパッケージが含まれているか確認

### デプロイが失敗する
→ Streamlit Cloudのログを確認し、エラーメッセージを確認

## 🔒 セキュリティの注意事項

- APIキーは絶対にコードに直接記述しない
- `.gitignore`ファイルで機密情報を除外
- Streamlit CloudのSecretsを使用してAPIキーを管理

## 📱 モバイル対応

デプロイされたアプリは自動的にモバイル対応になります。スマートフォンやタブレットからもアクセス可能です。

## 🎉 完了！

これでAIカウンセラーBOTがオンラインで利用可能になりました。URLを共有して、他の人にも使ってもらいましょう。

---

**サポートが必要な場合**: GitHubのIssuesまたはDiscussionsでお問い合わせください。