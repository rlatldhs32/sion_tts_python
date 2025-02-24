import speech_recognition as sr
import io
import os
import tempfile
from pydub import AudioSegment

class SpeechService:
    """음성 인식 관련 기능을 제공하는 서비스 클래스"""
    
    def __init__(self):
        """음성 인식기 초기화"""
        self.recognizer = sr.Recognizer()
        
        # 인식 옵션 설정
        self.recognizer.energy_threshold = 300  # 음성 감지 임계값
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # 말 사이 최대 멈춤 시간 (초)
    
    def speech_to_text(self, audio_data, language="ko-KR"):
        """
        음성 데이터를 텍스트로 변환
        
        Args:
            audio_data (bytes): 오디오 파일 데이터
            language (str): 인식할 언어 코드
            
        Returns:
            str: 인식된 텍스트
        """
        try:
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # 오디오 파일 로드 및 인식
            with sr.AudioFile(temp_path) as source:
                audio = self.recognizer.record(source)
            
            # 임시 파일 삭제
            os.unlink(temp_path)
            
            # Google 음성 인식 API 사용하여 텍스트 변환
            text = self.recognizer.recognize_google(audio, language=language)
            return text
            
        except sr.UnknownValueError:
            return "음성을 인식할 수 없었습니다."
        except sr.RequestError as e:
            return f"음성 인식 서비스 오류: {e}"
        except Exception as e:
            print(f"음성 인식 오류: {str(e)}")
            return "음성 처리 중 오류가 발생했습니다."
    
    def process_stream_chunk(self, audio_chunk, language="ko-KR"):
        """
        실시간 스트리밍 오디오 청크 처리
        
        Args:
            audio_chunk (bytes): 오디오 데이터 청크
            language (str): 인식할 언어 코드
            
        Returns:
            str: 인식된 텍스트 (있는 경우)
        """
        try:
            # 오디오 데이터를 AudioData 객체로 변환
            audio_data = sr.AudioData(audio_chunk, 16000, 2)  # 샘플링 레이트와 채널 수를 적절히 조정
            
            # 음성 인식 (음성이 확실한 경우에만)
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
            
        except sr.UnknownValueError:
            # 음성이 없거나 인식할 수 없는 경우 무시
            return None
        except Exception as e:
            print(f"스트리밍 오디오 처리 오류: {str(e)}")
            return None
    
    def convert_audio_format(self, audio_data, input_format="webm", output_format="wav"):
        """
        오디오 형식 변환
        
        Args:
            audio_data (bytes): 입력 오디오 데이터
            input_format (str): 입력 형식
            output_format (str): 출력 형식
            
        Returns:
            bytes: 변환된 오디오 데이터
        """
        try:
            # BytesIO 객체로 변환
            audio_io = io.BytesIO(audio_data)
            
            # pydub을 사용하여 오디오 형식 변환
            audio = AudioSegment.from_file(audio_io, format=input_format)
            
            # 출력 형식으로 변환
            output_io = io.BytesIO()
            audio.export(output_io, format=output_format)
            
            return output_io.getvalue()
            
        except Exception as e:
            print(f"오디오 변환 오류: {str(e)}")
            return None