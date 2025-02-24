import os
import requests
import json
import uuid
from config import Config

class FishTTSService:
    """Fish TTS API와 통신하는 서비스 클래스"""
    
    def __init__(self):
        """Fish TTS API 초기화"""
        self.api_key = Config.FISH_TTS_API_KEY
        self.api_url = "https://api.fish-tts.com/v1"  # Fish TTS API URL (예시)
        self.voice_models_dir = Config.VOICE_MODELS_DIR
    
    def create_voice_model(self, user_id, audio_file):
        """
        사용자 음성 파일로부터 새로운 TTS 음성 모델 생성
        
        Args:
            user_id (str): 사용자 ID
            audio_file (file): 사용자의 음성 샘플 파일
            
        Returns:
            dict: 생성된 음성 모델 정보
        """
        try:
            # 음성 파일 저장 (선택 사항)
            filename = f"{user_id}_{uuid.uuid4()}.wav"
            file_path = os.path.join(self.voice_models_dir, filename)
            audio_file.save(file_path)
            
            # Fish TTS API 호출하여 음성 모델 생성
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "multipart/form-data"
            }
            
            data = {
                "user_id": user_id,
                "model_name": f"{user_id}_voice_model"
            }
            
            files = {
                'audio_file': (filename, open(file_path, 'rb'), 'audio/wav')
            }
            
            response = requests.post(
                f"{self.api_url}/voice-models",
                headers=headers,
                data=data,
                files=files
            )
            
            if response.status_code == 200:
                model_info = response.json()
                # 모델 정보를 로컬에 저장
                self._save_model_info(user_id, model_info)
                return model_info
            else:
                print(f"Fish TTS API 오류: {response.text}")
                return {"error": "음성 모델 생성에 실패했습니다."}
                
        except Exception as e:
            print(f"음성 모델 생성 오류: {str(e)}")
            return {"error": str(e)}
    
    def text_to_speech(self, text, reference_id=None):
        """
        텍스트를 음성으로 변환
        
        Args:
            text (str): 음성으로 변환할 텍스트
            reference_id (str, optional): 사용할 음성 모델의 ID
            
        Returns:
            bytes: 생성된 음성 파일 데이터
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "output_format": "mp3"
            }
            
            # 음성 모델 ID가 제공된 경우
            if reference_id:
                data["reference_id"] = reference_id
            
            response = requests.post(
                f"{self.api_url}/text-to-speech", 
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"Fish TTS API 오류: {response.text}")
                return None
                
        except Exception as e:
            print(f"TTS 변환 오류: {str(e)}")
            return None
    
    def list_voice_models(self, user_id=None):
        """
        사용자의 음성 모델 목록 조회
        
        Args:
            user_id (str, optional): 특정 사용자의 모델만 조회
            
        Returns:
            list: 음성 모델 목록
        """
        try:
            if user_id:
                # 특정 사용자의 모델만 조회
                model_path = os.path.join(self.voice_models_dir, f"{user_id}_models.json")
                if os.path.exists(model_path):
                    with open(model_path, 'r') as f:
                        return json.load(f)
                return []
            else:
                # 모든 모델 조회 (Fish TTS API 사용)
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                response = requests.get(
                    f"{self.api_url}/voice-models",
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Fish TTS API 오류: {response.text}")
                    return []
                
        except Exception as e:
            print(f"모델 목록 조회 오류: {str(e)}")
            return []
    
    def _save_model_info(self, user_id, model_info):
        """사용자의 음성 모델 정보를 로컬에 저장"""
        try:
            model_path = os.path.join(self.voice_models_dir, f"{user_id}_models.json")
            
            # 기존 모델 정보 로드 또는 새로 생성
            if os.path.exists(model_path):
                with open(model_path, 'r') as f:
                    models = json.load(f)
            else:
                models = []
            
            # 새 모델 정보 추가
            models.append(model_info)
            
            # 저장
            with open(model_path, 'w') as f:
                json.dump(models, f, indent=2)
                
        except Exception as e:
            print(f"모델 정보 저장 오류: {str(e)}")