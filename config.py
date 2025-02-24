import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """애플리케이션 설정 관리 클래스"""
    
    # Flask 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # API 키
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    FISH_TTS_API_KEY = os.getenv('FISH_TTS_API_KEY')
    
    # 경로 설정
    VOICE_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'voice_models')
    
    # 서버 설정
    PORT = int(os.getenv('PORT', 5000))
    
    # Claude API 설정
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # 사용할 모델 버전
    
    # 데이터베이스 설정
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'voice_assistant')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # 기타 설정
    MAX_AUDIO_LENGTH = 60  # 최대 오디오 길이 (초)
    
    @classmethod
    def init_app(cls, app):
        """Flask 앱에 설정 적용"""
        app.config.from_object(cls)
        
        # 필요한 디렉토리 생성
        os.makedirs(cls.VOICE_MODELS_DIR, exist_ok=True)