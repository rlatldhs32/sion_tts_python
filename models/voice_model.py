from datetime import datetime
from models import db

class VoiceModel(db.Model):
    """음성 모델 클래스"""
    
    __tablename__ = 'voice_models'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    model_name = db.Column(db.String(128), nullable=False)
    reference_id = db.Column(db.String(128), nullable=False, unique=True)  # Fish TTS API에서 제공하는 ID
    file_path = db.Column(db.String(255))  # 로컬에 저장된 원본 오디오 파일 경로 (선택사항)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')  # active, deleted, processing 등
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, model_name, reference_id, file_path=None, description=None):
        self.user_id = user_id
        self.model_name = model_name
        self.reference_id = reference_id
        self.file_path = file_path
        self.description = description
    
    def to_dict(self):
        """음성 모델 정보를 딕셔너리로 변환 (API 응답용)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'model_name': self.model_name,
            'reference_id': self.reference_id,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<VoiceModel {self.model_name}>'