import anthropic
from config import Config

class ClaudeService:
    """Claude API와 통신하는 서비스 클래스"""
    
    def __init__(self):
        """Claude API 클라이언트 초기화"""
        self.client = anthropic.Anthropic(api_key=Config.CLAUDE_API_KEY)
        self.model = Config.CLAUDE_MODEL
        self.system_prompt = """
        당신은 친절하고 유용한 AI 비서입니다. 사용자의 질문에 명확하고 간결하게 대답해주세요.
        가능한 한 정확한 정보를 제공하되, 확실하지 않은 내용은 솔직하게 모른다고 말해야 합니다.
        """
    
    def get_response(self, user_message, conversation_history=None):
        """
        Claude API에 메시지를 보내고 응답을 받음
        
        Args:
            user_message (str): 사용자 메시지
            conversation_history (list, optional): 이전 대화 기록
            
        Returns:
            str: Claude의 응답
        """
        try:
            # 대화 기록이 없으면 빈 리스트로 초기화
            if conversation_history is None:
                conversation_history = []
            
            # 메시지 구성
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]
            
            # 대화 기록 추가
            for message in conversation_history:
                messages.append(message)
            
            # 사용자 메시지 추가
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # API 호출
            response = self.client.messages.create(
                model=self.model,
                messages=messages,
                max_tokens=2000
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API 오류: {str(e)}")
            return "죄송합니다. 응답을 생성하는 중에 오류가 발생했습니다."