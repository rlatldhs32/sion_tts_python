from flask import request, jsonify
from flask_socketio import emit
from services.speech_service import SpeechService
from services.claude_service import ClaudeService

class VoiceController:
    """음성 관련 요청을 처리하는 컨트롤러 클래스"""
    
    def __init__(self):
        """컨트롤러 초기화"""
        self.speech_service = SpeechService()
        self.claude_service = ClaudeService()
        # 실시간 스트리밍을 위한 버퍼
        self.audio_buffer = {}  # 사용자 ID를 키로 사용
    
    def speech_to_text(self):
        """
        음성 파일을 텍스트로 변환
        
        Returns:
            Response: JSON 응답
        """
        try:
            # 오디오 파일 확인
            if 'audio' not in request.files:
                return jsonify({"error": "오디오 파일이 없습니다."}), 400
            
            audio_file = request.files['audio']
            
            # 언어 파라미터 (기본값: 한국어)
            language = request.form.get('language', 'ko-KR')
            
            # 오디오 데이터 읽기
            audio_data = audio_file.read()
            
            # 필요한 경우 오디오 형식 변환
            input_format = request.form.get('format', 'webm')
            if input_format != 'wav':
                audio_data = self.speech_service.convert_audio_format(
                    audio_data, input_format, 'wav')
            
            # 음성 인식 수행
            text = self.speech_service.speech_to_text(audio_data, language)
            
            # 응답 반환
            return jsonify({
                "text": text,
                "status": "success"
            })
            
        except Exception as e:
            print(f"음성 인식 오류: {str(e)}")