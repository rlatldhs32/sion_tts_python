from flask import request, jsonify, send_file
import os
import tempfile
from services.tts_service import FishTTSService
from services.voice_model_service import VoiceModelService
from models.voice_model import VoiceModel

class TTSController:
    """TTS 관련 요청을 처리하는 컨트롤러 클래스"""
    
    def __init__(self):
        """컨트롤러 초기화"""
        self.tts_service = FishTTSService()
        self.voice_model_service = VoiceModelService(self.tts_service)
    
    def create_voice_model(self):
        """
        사용자 음성 파일로 새 음성 모델 생성
        
        Returns:
            Response: JSON 응답
        """
        try:
            # 오디오 파일 검증
            if 'audio_file' not in request.files:
                return jsonify({"error": "오디오 파일이 필요합니다."}), 400
            
            audio_file = request.files['audio_file']
            if not audio_file.filename:
                return jsonify({"error": "빈 파일명입니다."}), 400
            
            # 사용자 ID와 모델명 가져오기
            user_id = request.form.get('user_id')
            model_name = request.form.get('model_name')
            description = request.form.get('description')
            
            if not user_id or not model_name:
                return jsonify({"error": "사용자 ID와 모델명이 필요합니다."}), 400
            
            # 음성 모델 생성
            # 임시 구현: 실제로는 voice_model_service의 create_voice_model 호출
            # result = self.voice_model_service.create_voice_model(
            #     user_id=int(user_id),
            #     model_name=model_name,
            #     audio_file=audio_file,
            #     description=description
            # )
            
            # 임시 구현 (DB 연동 없이 Fish TTS API만 호출)
            result = self.tts_service.create_voice_model(user_id, audio_file)
            
            # 오류 확인
            if isinstance(result, dict) and 'error' in result:
                return jsonify(result), 400
            
            # 성공 응답
            return jsonify({
                "message": "음성 모델이 성공적으로 생성되었습니다.",
                "model": result
            }), 201
            
        except Exception as e:
            print(f"음성 모델 생성 오류: {str(e)}")
            return jsonify({"error": "음성 모델 생성 중 오류가 발생했습니다."}), 500
    
    def text_to_speech(self):
        """
        텍스트를 음성으로 변환 (커스텀 음성 모델 사용 가능)
        
        Returns:
            Response: 오디오 파일 또는 JSON 오류
        """
        try:
            data = request.get_json()
            
            # 필수 필드 검증
            if 'text' not in data:
                return jsonify({"error": "변환할 텍스트가 필요합니다."}), 400
            
            text = data['text']
            reference_id = data.get('reference_id')  # 선택 사항
            
            # TTS 변환 수행
            audio_data = self.tts_service.text_to_speech(text, reference_id)
            
            if not audio_data:
                return jsonify({"error": "음성 생성에 실패했습니다."}), 500
            
            # 임시 파일에 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # 오디오 파일 응답
            return send_file(
                temp_path,
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name='speech.mp3',
                # 파일 전송 후 삭제
                attachment_filename='speech.mp3'  # 구 버전 Flask 호환용
            )
            
        except Exception as e:
            print(f"TTS 변환 오류: {str(e)}")
            return jsonify({"error": "텍스트 음성 변환 중 오류가 발생했습니다."}), 500
    
    def list_voice_models(self):
        """
        사용자의 음성 모델 목록 조회
        
        Returns:
            Response: JSON 응답
        """
        try:
            # 사용자 ID 가져오기 (선택 사항)
            user_id = request.args.get('user_id')
            
            # 음성 모델 목록 조회
            # 임시 구현: 직접 서비스 호출
            models = self.tts_service.list_voice_models(user_id)
            
            # 성공 응답
            return jsonify({
                "models": models
            })
            
        except Exception as e:
            print(f"모델 목록 조회 오류: {str(e)}")
            return jsonify({"error": "음성 모델 목록 조회 중 오류가 발생했습니다."}), 500