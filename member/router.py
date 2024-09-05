"""
사용자 관리 기능(ex.로그인,회원가입)
"""
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from member.model import Member 
from member.schema import MemberSignUp, MemberSignIn, MemberUpdate, FindMemberId, FindMemberPw, editMemberPW, MemberInfo
from connection import get_session, Settings
from sqlmodel import select
from member.utils import HashPassword, JWTHandler, JWTtoFindPW
from member.auth import get_access_token
import os
from fastapi.responses import FileResponse

member_router = APIRouter( tags=["member"] )

hash_password = HashPassword()
jwt_handler = JWTHandler()
jwt_to_find_pw = JWTtoFindPW()

settings = Settings()

@member_router.post("/signup")
async def signUp(data: MemberSignUp, session=Depends(get_session)) -> dict:
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
async def signIn(data: MemberSignIn, session=Depends(get_session)) -> dict:
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

    # 4. 토큰 생성 및 반환
    return {"access_token": jwt_handler.create_token(member.member_idx, member.authority)}


@member_router.get("/logout")
async def update_member(session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    """
    로그아웃
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    return {"message":"로그아웃 되었습니다"}


@member_router.post("/mypage/get_edit_auth")
async def auth_edit_member(data:editMemberPW, session=Depends(get_session), token=Depends(get_access_token)) -> dict :
    """
    회원정보 수정을 위해 비밀번호를 입력
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: 
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 3. 비밀번호 암호화 후 비교
    if not hash_password.verify_password(data.password, member.password):
        raise HTTPException(status_code=401, detail="권한이 없습니다.")

    # 4. 비밀번호 재설정용 토큰 반환
    return {"token2pw":jwt_to_find_pw.create_token(member.member_idx)}


@member_router.get("/mypage")
async def get_member(session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    """
    회원정보 조회
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 3. 회원 정보 응답 스키마 생성
    member_info = MemberInfo(
        name=member.name,
        email=member.email,
        nickname=member.nickname,
        phone=member.phone,
        birth=member.birth,
        sex=member.sex,
        household=member.household,
        notice = member.notice
    )
    
    return member_info.model_dump()

@member_router.get("/mypage/profile")
async def get_member_profile(session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    """
    파일 전송
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    if member.profile_img=='':
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, 'main.png')
        return FileResponse(path=file_path, media_type='application/octet-stream', filename='main.png')
    else:
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, member.profile_img)
        return FileResponse(path=file_path, media_type='application/octet-stream', filename=member.profile_img)


@member_router.put("/mypage/edit")
async def update_member(data:MemberUpdate, session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    """
    회원정보 수정
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    member.name = data.name
    member.email = data.email
    member.nickname = data.nickname
    member.phone = data.phone
    member.notice = data.notice
    member.sex = data.sex
    member.household = data.household

    # 3. 데이터베이스에 변경 사항 저장
    session.add(member)
    session.commit()
    session.refresh(member)

    return {"message":"회원정보가 성공적으로 수정되었습니다."}


@member_router.post("/mypage/editprofile")
async def update_profile(profile_image: UploadFile = File(...), session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    """
    파일 업로드(프로필 설정)
    """
    # 1. 헤더에서 accessToken 가져와 회원 인덱스로 DB에서 회원 정보를 조회
    member_idx = token["member_idx"]
    statement = select(Member).where(Member.member_idx == member_idx)
    member = session.exec(statement).first()

    # 2. 회원 없을 시 404 오류
    if not member: raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # 3. 전송받은 파일 저장소에 저장
    file_location = os.path.join(settings.UPLOAD_DIRECTORY, profile_image.filename)
    with open(file_location, "wb") as file:
        contents = await profile_image.read()
        file.write(contents)

    member.profile_img = profile_image.filename

    # 4. 데이터베이스에 변경 사항 저장
    session.add(member)
    session.commit()
    session.refresh(member)

    return {"message":"프로필 업데이트 완료"}


@member_router.delete("/delete_account")
async def delete_member(session=Depends(get_session), token=Depends(get_access_token))->dict:
    """
    회원 탈퇴
    """
    member_idx = token["member_idx"]
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