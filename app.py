"""
AIカウンセラーBOT - Streamlitアプリケーション
"""
import streamlit as st
import time
from datetime import datetime
from counselor_ai import CounselorAI
import config


def init_session_state():
    """セッション状態の初期化"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'counselor' not in st.session_state:
        st.session_state.counselor = CounselorAI()
    
    if 'session_start' not in st.session_state:
        st.session_state.session_start = datetime.now()
    
    if 'show_summary' not in st.session_state:
        st.session_state.show_summary = False


def display_message(message):
    """メッセージの表示"""
    with st.chat_message(message["role"], avatar="🧘" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])


def main():
    """メインアプリケーション"""
    # ページ設定
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # カスタムCSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    h1 {
        color: #5B8C5A;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # タイトル
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    
    # セッション状態の初期化
    init_session_state()
    
    # サイドバー
    with st.sidebar:
        st.markdown("### セッション情報")
        duration = datetime.now() - st.session_state.session_start
        st.write(f"開始時刻: {st.session_state.session_start.strftime('%H:%M')}")
        st.write(f"経過時間: {int(duration.total_seconds() / 60)}分")
        
        st.markdown("---")
        
        if st.button("セッションを終了", type="secondary"):
            st.session_state.show_summary = True
        
        if st.button("新しいセッション", type="primary"):
            st.session_state.messages = []
            st.session_state.session_start = datetime.now()
            st.session_state.show_summary = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### このアプリについて
        
        カール・ロジャースの来談者中心療法に基づいたAIカウンセラーです。
        
        あなたのお話を聞き、共感的理解を通じて自己探索のお手伝いをします。
        """)
    
    # セッション要約の表示
    if st.session_state.show_summary and len(st.session_state.messages) > 0:
        st.markdown("## セッションの振り返り")
        
        with st.spinner("要約を作成中..."):
            summary = st.session_state.counselor.get_session_summary(st.session_state.messages)
            st.info(summary)
        
        st.markdown("### 振り返りの質問")
        questions = st.session_state.counselor.suggest_reflection_questions(st.session_state.messages)
        for q in questions:
            st.write(f"- {q}")
        
        return
    
    # 初回メッセージ
    if len(st.session_state.messages) == 0:
        welcome_msg = {"role": "assistant", "content": config.WELCOME_MESSAGE}
        st.session_state.messages.append(welcome_msg)
    
    # 会話履歴の表示
    for message in st.session_state.messages:
        display_message(message)
    
    # 会話数の制限チェック
    if len(st.session_state.messages) >= config.MAX_CONVERSATION_LENGTH * 2:
        st.warning("長い時間お話しいただき、ありがとうございました。そろそろ一度休憩を取られてはいかがでしょうか。")
        return
    
    # ユーザー入力
    if prompt := st.chat_input("お話をお聞かせください..."):
        # ユーザーメッセージを追加
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        display_message(user_message)
        
        # AIの応答を生成
        with st.chat_message("assistant", avatar="🧘"):
            with st.spinner(""):
                response = st.session_state.counselor.get_response(
                    prompt, 
                    st.session_state.messages[:-1]  # 最新のユーザーメッセージを除く
                )
                
                # タイピング効果
                placeholder = st.empty()
                full_response = ""
                for chunk in response.split():
                    full_response += chunk + " "
                    placeholder.markdown(full_response + "▌")
                    time.sleep(0.05)
                placeholder.markdown(full_response)
        
        # アシスタントメッセージを追加
        assistant_message = {"role": "assistant", "content": response}
        st.session_state.messages.append(assistant_message)


if __name__ == "__main__":
    # APIキーの確認
    if not config.GEMINI_API_KEY:
        st.error("Gemini APIキーが設定されていません。")
        st.info("ローカル環境の場合は .env ファイルに、Streamlit Cloudにデプロイした場合はSecretsにAPIキーを設定してください。")
        st.stop()
    
    main()