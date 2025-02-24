from flask import request, jsonify
from services.user_service import UserService

class UserController:
    """사용자 관련 요청을 처리하는 컨트롤러 클래스"""
    
    def __init__(self):
        """컨트롤러 초기화"""
        self.user_service = UserService()
    
    def register(self):
        """
        새 사용자 등록
        
        Returns:
            Response: JSON 응답
        """
        try:
            data = request.get_json()
            
            # 필수 필드 검증
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"{field} 필드가 필요합니다."}), 400
            
            # 사용자 생성
            result = self.user_service.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            
            # 오류 확인
            if isinstance(result, dict) and 'error' in result:
                return jsonify(result), 400
            
            # 성공 응답
            return jsonify({
                "message": "사용자가 성공적으로 등록되었습니다.",
                "user": result.to_dict()
            }), 201
            
        except Exception as e:
            print(f"사용자 등록 오류: {str(e)}")
            return jsonify({"error": "사용자 등록 중 오류가 발생했습니다."}), 500
    
    def login(self):
        """
        사용자 로그인
        
        Returns:
            Response: JSON 응답
        """
        try:
            data = request.get_json()
            
            # 필수 필드 검증
            if 'username_or_email' not in data or 'password' not in data:
                return jsonify({"error": "사용자 이름/이메일과 비밀번호가 필요합니다."}), 400
            
            # 사용자 인증
            user = self.user_service.authenticate_user(
                username_or_email=data['username_or_email'],
                password=data['password']
            )
            
            if not user:
                return jsonify({"error": "인증 실패: 사용자 이름/이메일 또는 비밀번호가 잘못되었습니다."}), 401
            
            # 여기에 JWT 토큰 생성 로직을 추가할 수 있음
            # token = create_jwt_token(user.id)
            
            # 성공 응답
            return jsonify({
                "message": "로그인 성공",
                "user": user.to_dict(),
                # "token": token  # JWT 사용 시 주석 해제
            })
            
        except Exception as e:
            print(f"로그인 오류: {str(e)}")
            return jsonify({"error": "로그인 중 오류가 발생했습니다."}), 500
    
    def get_profile(self, user_id):
        """
        사용자 프로필 조회
        
        Args:
            user_id (int): 사용자 ID
        
        Returns:
            Response: JSON 응답
        """
        try:
            user = self.user_service.get_user_by_id(user_id)
            
            if not user:
                return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404
            
            return jsonify({"user": user.to_dict()})
            
        except Exception as e:
            print(f"프로필 조회 오류: {str(e)}")
            return jsonify({"error": "프로필 조회 중 오류가 발생했습니다."}), 500
    
    def update_profile(self, user_id):
        """
        사용자 프로필 업데이트
        
        Args:
            user_id (int): 사용자 ID
        
        Returns:
            Response: JSON 응답
        """
        try:
            data = request.get_json()
            
            # 업데이트 수행
            result = self.user_service.update_user(user_id, data)
            
            # 오류 확인
            if isinstance(result, dict) and 'error' in result:
                return jsonify(result), 400 if 'not found' in result['error'] else 500
            
            return jsonify({
                "message": "프로필이 성공적으로 업데이트되었습니다.",
                "user": result.to_dict()
            })
            
        except Exception as e:
            print(f"프로필 업데이트 오류: {str(e)}")
            return jsonify({"error": "프로필 업데이트 중 오류가 발생했습니다."}), 500
    
    def delete_account(self, user_id):
        """
        사용자 계정 삭제
        
        Args:
            user_id (int): 사용자 ID
        
        Returns:
            Response: JSON 응답
        """
        try:
            success = self.user_service.delete_user(user_id)
            
            if not success:
                return jsonify({"error": "사용자를 찾을 수 없거나 삭제할 수 없습니다."}), 404
            
            return jsonify({"message": "사용자 계정이 성공적으로 삭제되었습니다."})
            
        except Exception as e:
            print(f"계정 삭제 오류: {str(e)}")
            return jsonify({"error": "계정 삭제 중 오류가 발생했습니다."}), 500