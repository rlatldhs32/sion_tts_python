from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from models import init_db

# 앱 인스턴스 생성
app = Flask(__name__)
Config.init_app(app)

# CORS 설정 (Flutter 앱에서 접근 허용)
CORS(app)

# SocketIO 설정 (실시간 음성 스트리밍)
socketio = SocketIO(app, cors_allowed_origins="*")

# 데이터베이스 초기화
init_db(app, Config)

# 라우트 등록
from api.routes import register_routes
register_routes(app, socketio)

if __name__ == '__main__':
    print(f"서버 시작! 포트: {Config.PORT}")
    socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)