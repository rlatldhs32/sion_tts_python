from models import db
from models.user import User

class UserService:
    """사용자 관련 비즈니스 로직 처리 서비스"""
    
    def create_user(self, username, email, password):
        """
        새 사용자 생성
        
        Args:
            username (str): 사용자명
            email (str): 이메일
            password (str): 비밀번호
            
        Returns:
            User: 생성된 사용자 객체
        """
        try:
            # 이미 존재하는 사용자 확인
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    return {'error': '이미 사용 중인 사용자명입니다.'}
                else:
                    return {'error': '이미 사용 중인 이메일입니다.'}
            
            # 새 사용자 생성 및 저장
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            
            return new_user
            
        except Exception as e:
            db.session.rollback()
            print(f"사용자 생성 오류: {str(e)}")
            return {'error': '사용자 생성 중 오류가 발생했습니다.'}
    
    def get_user_by_id(self, user_id):
        """
        ID로 사용자 조회
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            User: 사용자 객체 또는 None
        """
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        """
        사용자명으로 사용자 조회
        
        Args:
            username (str): 사용자명
            
        Returns:
            User: 사용자 객체 또는 None
        """
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        """
        이메일로 사용자 조회
        
        Args:
            email (str): 이메일
            
        Returns:
            User: 사용자 객체 또는 None
        """
        return User.query.filter_by(email=email).first()
    
    def authenticate_user(self, username_or_email, password):
        """
        사용자 인증
        
        Args:
            username_or_email (str): 사용자명 또는 이메일
            password (str): 비밀번호
            
        Returns:
            User: 인증 성공 시 사용자 객체, 실패 시 None
        """
        # 이메일 또는 사용자명으로 사용자 조회
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        # 사용자가 존재하고 비밀번호가 일치하는지 확인
        if user and user.check_password(password):
            return user
        return None
    
    def update_user(self, user_id, data):
        """
        사용자 정보 업데이트
        
        Args:
            user_id (int): 사용자 ID
            data (dict): 업데이트할 필드와 값
            
        Returns:
            User: 업데이트된 사용자 객체 또는 오류
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {'error': '사용자를 찾을 수 없습니다.'}
            
            # 허용된 필드만 업데이트
            allowed_fields = ['username', 'email']
            for field in allowed_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            # 비밀번호 변경이 포함된 경우
            if 'password' in data:
                user.set_password(data['password'])
            
            db.session.commit()
            return user
            
        except Exception as e:
            db.session.rollback()
            print(f"사용자 업데이트 오류: {str(e)}")
            return {'error': '사용자 정보 업데이트 중 오류가 발생했습니다.'}
    
    def delete_user(self, user_id):
        """
        사용자 삭제
        
        Args:
            user_id (int): 사용자 ID
            
        Returns:
            bool: 성공 여부
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False
            
            db.session.delete(user)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"사용자 삭제 오류: {str(e)}")
            return False