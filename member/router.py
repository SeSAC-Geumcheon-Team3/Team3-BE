"""
사용자 관리 기능(ex.로그인,회원가입)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from member.model import Member 
from member.schema import MemberSignUp
from connection import get_session
from sqlmodel import select
# from auth.hash_password import HashPassword
# from auth.jwt_handler import create_jwt_token

member_router = APIRouter( tags=["member"] )

@member_router.post("/signup")
async def sign_new_user(data: MemberSignUp, session=Depends(get_session)) -> dict:
    """
    사용자 등록
    """
    statement = select(Member).where(Member.email==data.email)
    member = session.exec(statement).first()

    # case1. 사용자 존재 시 409 오류 코드 반환
    if member:
        raise HTTPException(status_code=status.HTTP_409_CONFILCT, detail="이미 존재하는 사용자입니다")
    
    # case2. 사용자가 없다면 사용자 등록
    new_member = Member ( 
        name=data.username,
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