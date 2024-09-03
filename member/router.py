"""
사용자 관리 기능(ex.로그인,회원가입)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from member.model import Member 
from member.schema import MemberSignUp, MemberSignIn, MemberUpdate
from connection import get_session
from sqlmodel import select
# from auth.hash_password import HashPassword
# from auth.jwt_handler import create_jwt_token

member_router = APIRouter( tags=["member"] )

@member_router.post("/signup")
async def sign_new_user(data: MemberSignUp, session=Depends(get_session)) -> dict:
    """
    회원가입
    """

    new_member = Member ( 
        name=data.name,
        email = data.email,
        password = data.password,
        # password=hash_password.hash_password(data.password),
        nickname = data.nickname,
        phone  = data.phone,
        notice = data.notice,
        birth = data.birth,
        sex = data.sex,
        household = data.household
    )

    session.add(new_member)
    session.commit()
    
    return {"message":"정상적으로 등록되었습니다"}

@member_router.post("/signin")
async def sign_new_user(data: MemberSignIn, session=Depends(get_session)) -> dict:
    """
    로그인
    """
    # 1. 요청 환경 설정
    statement = select(Member).where(Member.email==data.email)
    member = session.exec(statement).first()

    # 2. 사용자가 일치 여부 확인 
    if not member:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, detail="일치하는 사용자가 존재하지 않습니다" )
    
    # 3. 패스워드 일치여부 확인
    # if not hash_password.verify_password(data.password, user.password):
    if data.password != member.password:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="패스워드가 일치하지 않습니다" )
    
    # 4. 로그인 성공 확인
    return {"message":"로그인에 성공하였습니다"}

    # 4. 토큰 생성 및 반환
    # return {"message":"로그인에 성공하였습니다", "access_token":create_jwt_token(user.email, user.id)}

@member_router.put("/mypage/edit")
async def update_member(data:MemberUpdate, session=Depends(get_session)) -> dict:
    """
    회원정보 수정
    """
    # 1. DB에서 회원 정보를 조회
    statement = select(Member).where(Member.member_idx == data.member_idx)
    member = session.exec(statement).first()

    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    member.name = data.name
    member.email = data.email
    member.password = data.password
    member.nickname = data.nickname
    member.phone = data.phone
    member.notice = data.notice
    member.sex = data.sex
    member.household = data.household
    member.profile_img = data.profile_img

    # 3. 데이터베이스에 변경 사항 저장
    session.add(member)
    session.commit()
    session.refresh(member)

    # 4. 수정된 member를 MemberUpdate 객체로 변환하여 반환
    updated_member = MemberUpdate.model_validate(member)

    return updated_member.model_dump()
