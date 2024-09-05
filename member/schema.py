"""
DTO와 같이 데이터 전송에 사용되는 모델
"""
from pydantic import EmailStr
from sqlmodel import SQLModel


# 회원가입 시 전달되는 데이터 모델
class MemberSignUp(SQLModel):
    name: str
    email: EmailStr
    password: str
    nickname: str
    phone: str
    notice: bool
    birth: str = ""
    sex: str = ""
    household: int = 0


# 로그인 시 전달되는 데이터 모델
class MemberSignIn(SQLModel):
    email: EmailStr
    password: str


# 회원 정보 수정 시 전달되는 데이터 모델
class MemberUpdate(SQLModel):
    name: str
    email: EmailStr
    nickname: str
    phone: str
    notice: bool
    birth: str
    sex: str
    household: int


# ID 찾을 때 전달되는 데이터 모델
class FindMemberId(SQLModel):
    name:str
    phone:str

# PW 찾을 때 전달되는 데이터 모델
class FindMemberPw(SQLModel):
    email:str
    name:str
    phone:str


# 회원 정보 조회 요청에 대한 응답 데이터 모델
class MemberInfo(SQLModel):
    name: str
    email: str
    nickname: str
    phone: str
    profile_img: str
    birth: str
    sex: str
    household: int
    notice: bool


# 회원정보 수정 위한 비밀번호 데이터 모델
class editMemberPW(SQLModel):
    password:str