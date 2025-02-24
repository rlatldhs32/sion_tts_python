from models import db
from models.voice_model import VoiceModel
import os
import uuid
from config import Config

class VoiceModelService:
    """음성 모델 관련 비즈니스 로직 처리 서비스"""
    
    def __init__(self, fish_tts_service=None):
        """
        서비스 초기화
        
        Args:
            fish_tts_service: Fish TTS 서비스 인스턴스 (선택사항)
        """
        self.fish_tts_service = fish_tts_service
        self.voice_models_dir = Config.VOICE_MODELS_DIR
    
    def create_voice_model(self, user_id, model_name, audio_file, description=None):
        """
        새 음성 모델 생성
        
        Args:
            user_id (int): 사용자 ID
            model_name (str): 모델 이름
            audio_file (file): 음성 샘플 파일
            description (str, optional): 모델 설명
            
        Returns:
            VoiceModel: 생성된 음성 모델 객체 또는 오류
        """
        try:
            # 파일 저장 경로 생성
            filename = f"{user_id}_{uuid.uuid4()}.wav"
            user_dir = os.path.join(self.voice_models_dir, str(user_id))
            os.makedirs(user_dir, exist_ok=True)
            file_path = os.path.join(user_dir, filename)
            
            # 오디오 파일 저장
            audio_file.save(file_path)
            
            # Fish TTS API를 통해 모델 생성
            if self.fish_tts_service:
                model_info = self.fish_tts_service.create_voice_model(user_id, audio_file)
                if 'error' in model_info:
                    return model_info
                
                reference_id = model_info.get('reference_id')
            else:
                # 테스트용 임시 ID (실제로는 Fish TTS API에서 받아야 함)
                reference_id = f"fish_tts_{uuid.uuid4()}"
            
            # DB에 모델 정보 저장
            voice_model = VoiceModel(
                user_id=user_id,
                model_name=model_name,
                reference_id=reference_id,
                file_path=file_path,
                description=description
            )
            
            db.session.add(voice_model)
            db.session.commit()
            
            return voice_model
            
        except Exception as e:
            db.session.rollback()
            print(f"음성 모델 생성 오류: {str(e)}")
            return {'error': '음성 모델 생성 중 오류가 발생했습니다.'}
    
    def get_model_by_id(self, model_id):
        """
        ID로 음성 모델 조회
        
        Args:
            model_id (int): 모델 ID
            
        Returns:
            VoiceModel: 음성 모델 객체 또는 None
        """
        return VoiceModel.query.get(model_id)
    
    def get_models_by_user(self, user_id):
        """
        사용자의 모든 음성 모델 조회
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            list: 음성 모델 객체 리스트
        """
        return VoiceModel.query.filter_by(user_id=user_id, status='active').all()
    
    def update_model(self, model_id, data):
        """
        음성 모델 정보 업데이트
        
        Args:
            model_id (int): 모델 ID
            data (dict): 업데이트할 필드와 값
            
        Returns:
            VoiceModel: 업데이트된 모델 객체 또는 오류
        """
        try:
            model = VoiceModel.query.get(model_id)
            if not model:
                return {'error': '모델을 찾을 수 없습니다.'}
            
            # 허용된 필드만 업데이트
            allowed_fields = ['model_name', 'description', 'status']
            for field in allowed_fields:
                if field in data:
                    setattr(model, field, data[field])
            
            db.session.commit()
            return model
            
        except Exception as e:
            db.session.rollback()
            print(f"모델 업데이트 오류: {str(e)}")
            return {'error': '모델 정보 업데이트 중 오류가 발생했습니다.'}
    
    def delete_model(self, model_id):
        """
        음성 모델 삭제 (소프트 삭제)
        
        Args:
            model_id (int): 모델 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            model = VoiceModel.query.get(model_id)
            if not model:
                return False
            
            # 소프트 삭제 (상태만 변경)
            model.status = 'deleted'
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"모델 삭제 오류: {str(e)}")
            return False
    
    def hard_delete_model(self, model_id):
        """
        음성 모델 완전 삭제 (DB에서 제거 및 파일 삭제)
        
        Args:
            model_id (int): 모델 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            model = VoiceModel.query.get(model_id)
            if not model:
                return False
            
            # 파일 삭제
            if model.file_path and os.path.exists(model.file_path):
                os.remove(model.file_path)
            
            # DB에서 레코드 삭제
            db.session.delete(model)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"모델 완전 삭제 오류: {str(e)}")
            return False