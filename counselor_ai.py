"""
AIカウンセラーのコア機能
"""
import google.generativeai as genai
from typing import List, Dict, Optional
import config
import time


class CounselorAI:
    """カール・ロジャースの理論に基づくAIカウンセラー"""
    
    def __init__(self):
        """AIカウンセラーの初期化"""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=config.MODEL_NAME,
            generation_config={
                'temperature': config.TEMPERATURE,
                'max_output_tokens': config.MAX_TOKENS,
            }
        )
        self.conversation_history = []
        
    def get_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """ユーザーの入力に対してカウンセリング応答を生成"""
        try:
            # 会話履歴を整形
            history_text = self._format_conversation_history(conversation_history)
            
            # プロンプトを構築
            prompt = f"""{config.SYSTEM_PROMPT}

これまでの会話:
{history_text}

ユーザーの最新の発言: {user_input}

上記の基本的態度と技法に基づいて、共感的で支持的な応答をしてください。
ユーザーが自己探索を深められるような質問や反映を含めてください。"""
            
            # Gemini APIを呼び出し
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"応答生成中にエラーが発生しました: {e}")
            return "申し訳ございません。少し考える時間をいただけますか..."
    
    def _format_conversation_history(self, history: List[Dict]) -> str:
        """会話履歴を文字列に整形"""
        if not history:
            return "（会話開始）"
        
        formatted = []
        # 最新の10ターンのみを使用（コンテキストの制限）
        recent_history = history[-20:] if len(history) > 20 else history
        
        for msg in recent_history:
            role = "ユーザー" if msg["role"] == "user" else "カウンセラー"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def analyze_emotional_state(self, user_input: str) -> Dict[str, any]:
        """ユーザーの感情状態を分析（内部使用）"""
        try:
            prompt = f"""以下のユーザーの発言から、感情状態を分析してください。
判断や評価ではなく、観察された感情を客観的に記述してください。

ユーザーの発言: {user_input}

以下の形式で回答してください：
- 主な感情:
- 感情の強度（1-10）:
- 潜在的なニーズ:"""
            
            response = self.model.generate_content(prompt)
            # この分析は内部的に使用し、直接ユーザーには見せない
            return {"analysis": response.text}
            
        except Exception as e:
            return {"analysis": "分析できませんでした"}
    
    def get_session_summary(self, conversation_history: List[Dict]) -> str:
        """セッションの要約を生成"""
        try:
            history_text = self._format_conversation_history(conversation_history)
            
            prompt = f"""以下の会話を要約してください。
ユーザーが話した主なテーマ、表現された感情、得られた気づきを含めてください。
判断や評価は避け、客観的な要約にしてください。

会話内容:
{history_text}

要約:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return "セッションの要約を作成できませんでした。"
    
    def suggest_reflection_questions(self, conversation_history: List[Dict]) -> List[str]:
        """セッション後の振り返り質問を提案"""
        questions = [
            "今日の会話で、何か新しい気づきはありましたか？",
            "話してみて、どんな気持ちになりましたか？",
            "これから、どんなことを大切にしていきたいですか？",
            "自分自身について、何か発見はありましたか？"
        ]
        return questions