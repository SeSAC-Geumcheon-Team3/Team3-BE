# auth.py
from fastapi import Depends, HTTPException, Header, status
from member.utils import JWTHandler

jwt_handler = JWTHandler()


# 의존성을 사용하여 헤더에서 accessToken을 가져오는 함수
async def get_access_token(token: str = Header(...)):
    if not token:# or not accessToken.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    
    token_payload = jwt_handler.verify_token(token)
    print(token_payload)
    return token_payload
