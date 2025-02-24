from flask import jsonify
from api.controllers.chat_controller import ChatController
from api.controllers.voice_controller import VoiceController
from api.controllers.tts_controller import TTSController
from api.controllers.user_controller import UserController

def register_routes(app, socketio):
    """앱에 모든 API 라우트 등록"""
    
    # 컨트롤러 인스턴스 생성
    chat_controller = ChatController()
    voice_controller = VoiceController()
    tts_controller = TTSController()
    user_controller = UserController()
    
    # REST API 엔드포인트 정의
    
    # 1. 건강 체크 엔드포인트
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok", "message": "서버가 정상적으로 작동 중입니다."})
    
    # 2. 텍스트 채팅 엔드포인트
    @app.route('/api/chat', methods=['POST'])
    def chat():
        return chat_controller.process_message()
    
    # 3. 음성 -> 텍스트 변환 엔드포인트
    @app.route('/api/speech-to-text', methods=['POST'])
    def speech_to_text():
        return voice_controller.speech_to_text()
    
    # 4. 음성 모델 생성 엔드포인트
    @app.route('/api/voice-model', methods=['POST'])
    def create_voice_model():
        return tts_controller.create_voice_model()
    
    # 5. 텍스트 -> 음성 변환 엔드포인트 (with custom voice)
    @app.route('/api/text-to-speech', methods=['POST'])
    def text_to_speech():
        return tts_controller.text_to_speech()
    
    # 6. 음성 모델 목록 조회
    @app.route('/api/voice-models', methods=['GET'])
    def list_voice_models():
        return tts_controller.list_voice_models()
    
    # 7. 사용자 인증 관련 엔드포인트
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        return user_controller.register()
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return user_controller.login()
    
    @app.route('/api/users/<int:user_id>', methods=['GET'])
    def get_user_profile(user_id):
        return user_controller.get_profile(user_id)
    
    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user_profile(user_id):
        return user_controller.update_profile(user_id)
    
    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        return user_controller.delete_account(user_id)
    
    # 8. 오류 핸들러
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "요청한 리소스를 찾을 수 없습니다."}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), 500
    
    # SocketIO 이벤트 핸들러 등록 (실시간 음성 스트리밍)
    @socketio.on('connect')
    def handle_connect():
        print('클라이언트 연결됨')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('클라이언트 연결 해제됨')
    
    @socketio.on('stream_audio')
    def handle_stream_audio(audio_data):
        voice_controller.process_stream(audio_data)