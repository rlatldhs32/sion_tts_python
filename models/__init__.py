from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

def init_db(app, config):
    """
    Flask 앱에 데이터베이스 초기화
    
    Args:
        app: Flask 애플리케이션 인스턴스
        config: 설정 객체
    """
    # MariaDB 연결 문자열 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@'
        f'{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = config.DEBUG  # SQL 쿼리 로깅 (디버그 모드에서만)
    
    # 앱에 DB 연결
    db.init_app(app)
    
    # 앱 컨텍스트 내에서 모든 테이블 생성
    with app.app_context():
        db.create_all()