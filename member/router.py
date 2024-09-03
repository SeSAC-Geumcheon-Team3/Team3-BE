"""
사용자 관리 기능(ex.로그인,회원가입)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from member.model import Member 
from member.schema import MemberSignUp, MemberSignIn, MemberUpdate, FindMemberId, FindMemberPw
from connection import get_session
from sqlmodel import select
from member.utils import HashPassword
# from auth.hash_password import HashPassword
# from auth.jwt_handler import create_jwt_token

member_router = APIRouter( tags=["member"] )

hash_password = HashPassword()

@member_router.post("/signup")
async def sign_new_user(data: MemberSignUp, session=Depends(get_session)) -> dict:
    """
    회원가입
    """
    new_member = Member ( 
        name=data.name,
        email = data.email,
        password=hash_password.hash_password(data.password),
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
    if not hash_password.verify_password(data.password, member.password):
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

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    member.name = data.name
    member.email = data.email
    member.password = hash_password.hash_password(data.password)
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


@member_router.delete("/delete_account")
async def delete_member(session=Depends(get_session))->dict:
    """
    회원 탈퇴
    """
    member_idx = 1
    # 1. 회원 조회
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 3. 회원 정보 삭제
    session.delete(member)
    session.commit()

    return {"message":"회원 삭제가 완료되었습니다."}


@member_router.post("/findid")
async def find_id(data:FindMemberId, session=Depends(get_session))->dict:
    """
    사용자 ID 찾기
    """
    # 1. 회원 조회
    statement = select(Member).where((Member.name==data.name) & (Member.phone==data.phone))
    member = session.exec(statement).first()

     # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 3. 마스킹
    user, domain = member.email.split('@')

    if len(user) <= 2:
        # 사용자 이름이 2자 이하일 경우, 모든 문자 마스킹
        masked_user = user[0] + '*' * (len(user) - 1)
    else:
        # 사용자 이름이 3자 이상인 경우, 중간 부분을 마스킹
        masked_user = user[:2] + '*' * (len(user) - 2) 

    return { "email": f"{masked_user}@{domain}" }


@member_router.post("/findpw")
async def find_pw(data:FindMemberPw, session=Depends(get_session)) -> dict:
    """
    비밀번호 찾기
    """
    # 1. 회원 조회
    statement = select(Member).where((Member.email==data.email) & (Member.name==data.name) & (Member.phone==data.phone))
    member = session.exec(statement).first()
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 2. pw 재설정 링크 생성 및 이메일 발송 링크 생성

    return {"link":"거시기입니다"}