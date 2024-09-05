# auth.py
from fastapi import Depends, HTTPException, Header, status
from member.utils import JWTHandler

jwt_handler = JWTHandler()


# 의존성을 사용하여 헤더에서 accessToken을 가져오는 함수
async def get_access_token(Authorization: str = Header(...)):
    if not Authorization:# or not accessToken.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    token_payload = jwt_handler.verify_token(Authorization.split(" ")[1])

    if token_payload["authority"]=="권한 없음":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용 권한이 없습니다")

    return token_payload


# 의존성을 사용하여 헤더에서 accessToken을 가져오는 함수 : 관리자용
async def get_admin_access_token(Authorization: str = Header(...)):
    if not Authorization:# or not accessToken.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    token_payload = jwt_handler.verify_token(Authorization.split(" ")[1])

    if token_payload["authority"]!="관리자":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용 권한이 없습니다")

    return token_payload


# 비밀번호 수정 시 의존성을 사용하여 헤더에서 accessToken을 가져오는 함수
async def get_reset_pw_token(Authorization: str = Header(...)):
    if not Authorization:# or not accessToken.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing"
        )
    token_payload = jwt_handler.verify_token(Authorization.split(" ")[1])

    return token_payload