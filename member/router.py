"""
사용자 관리 기능(ex.로그인,회원가입)
"""
from fastapi import APIRouter, Depends
from member.model import Member 
from member.schema import MemberSignUp
from connection import get_session
# from auth.hash_password import HashPassword
# from auth.jwt_handler import create_jwt_token

member_router = APIRouter( tags=["member"] )

@member_router.post("/signup")
async def sign_new_user(data: MemberSignUp, session=Depends(get_session)) -> dict:
    """
    사용자 등록
    """

    new_member = Member ( 
        name=data.name,
        email = data.email,
        password = data.password,
        # password=hash_password.hash_password(data.password),
        nickname = data.nickname,
        phone  = data.phone,
        notice = data.notice,
        sex = data.sex,
        household = data.household
    )

    session.add(new_member)
    session.commit()
    
    return {"message":"정상적으로 등록되었습니다"}