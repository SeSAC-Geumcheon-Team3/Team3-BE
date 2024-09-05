from passlib.context import CryptContext
from jose import jwt
from time import time
from connection import Settings

# .env 파일 로드
settings = Settings()

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
    def __init__(self, secret_key: str=settings.SECRET_KEY, algorithm: str=settings.ALGORITHM, expires_in: int=settings.EXP):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_token(self, member_idx: int, authority:str) -> str:
        """
        JWT 생성 함수  
        return: 생성된 JWT 토큰 문자열
        """
        payload = {"member_idx":member_idx, "authority":authority, "iat":time(), "exp": time()+self.expires_in}
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
        
class JWTtoFindPW:
    """
    암호 재설정 위한 JWT 토큰 형식 추가
    """
    def __init__(self, secret_key: str=settings.SECRET_KEY, algorithm: str=settings.ALGORITHM, expires_in: int=settings.EXP):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_token(self, member_idx: int) -> str:
        """
        JWT 생성 함수  
        return: 생성된 JWT 토큰 문자열
        """
        payload = {"member_idx":member_idx, "iat":time(), "exp": time()+self.expires_in}
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