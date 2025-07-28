"""
ローカルテスト用スクリプト
APIキーが正しく設定されているか確認
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルから環境変数を読み込み
load_dotenv()

def test_api_connection():
    """Gemini APIの接続テスト"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ エラー: GEMINI_API_KEYが設定されていません")
        print("解決方法:")
        print("1. .envファイルを作成")
        print("2. GEMINI_API_KEY=your-key-here を記入")
        return False
    
    try:
        # API設定
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # テストプロンプト
        response = model.generate_content("こんにちは。これはテストです。")
        
        print("✅ API接続成功!")
        print(f"応答: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_counselor_response():
    """カウンセラーAIの応答テスト"""
    from counselor_ai import CounselorAI
    
    print("\n🧘 カウンセラーAIのテスト")
    print("-" * 40)
    
    try:
        counselor = CounselorAI()
        
        # テスト入力
        test_input = "最近、仕事でストレスを感じています。"
        
        print(f"ユーザー: {test_input}")
        print("\nカウンセラーの応答:")
        
        response = counselor.get_response(test_input, [])
        print(response)
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


if __name__ == "__main__":
    print("🔧 AIカウンセラーBOT ローカルテスト")
    print("=" * 40)
    
    # API接続テスト
    if test_api_connection():
        # カウンセラー応答テスト
        test_counselor_response()
    
    print("\n✅ テスト完了")
    print("\n次のステップ:")
    print("1. streamlit run app.py でアプリを起動")
    print("2. ./deploy.sh でGitHubにデプロイ")