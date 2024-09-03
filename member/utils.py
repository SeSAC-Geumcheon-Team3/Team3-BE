from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from time import time


# .env 파일 로드
load_dotenv()
# .env에 정의된 SECRET_KEY 가져오기
SECRET_KEY = os.getenv("SECRET_KEY")

class HashPassword:
    """
    패스워드 암호화(해싱) 및 검증
    """
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password:str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password:str, hashed_password:str):
        return self.pwd_context.verify(plain_password, hashed_password)

class JWTHandler:
    """
    jwt 토큰 핸들링
    """
    def __init__(self, secret_key: str=SECRET_KEY, algorithm: str="HS256", expires_in: int=3600):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_token(self, email: str, user_id: int) -> str:
        """
        JWT 생성 함수  
        return: 생성된 JWT 토큰 문자열
        """
        payload = {"email":email, "user_id":user_id, "iat":time(), "exp": time()+self.expires_in}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        """
        JWT 검증 함수  
        return: JWT의 payload
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        
        # exp 오류 - 토큰만료
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        
        # 토큰 형식 불일치
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")