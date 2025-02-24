from flask import request, jsonify
from services.claude_service import ClaudeService

class ChatController:
    """채팅 관련 요청을 처리하는 컨트롤러 클래스"""
    
    def __init__(self):
        """컨트롤러 초기화"""
        self.claude_service = ClaudeService()
    
    def process_message(self):
        """
        사용자 메시지를 처리하고 Claude API 응답 반환
        
        Returns:
            Response: JSON 응답
        """
        try:
            # 요청에서 데이터 추출
            data = request.get_json()
            
            if not data or 'message' not in data:
                return jsonify({"error": "메시지가 비어있습니다."}), 400
            
            user_message = data['message']
            conversation_history = data.get('conversation_history', [])
            
            # Claude API 호출
            response = self.claude_service.get_response(user_message, conversation_history)
            
            # 응답 반환
            return jsonify({
                "response": response,
                "status": "success"
            })
            
        except Exception as e:
            print(f"메시지 처리 오류: {str(e)}")
            return jsonify({"error": "메시지 처리 중 오류가 발생했습니다."}), 500