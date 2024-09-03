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
    member_idx:int
    profile_img: str
    name: str
    email: EmailStr
    password: str
    nickname: str
    phone: str
    notice: bool
    birth: str
    sex: str
    household: int

    class Config:
        orm_mode = True


# ID 찾을 때 전달되는 데이터 모델
class FindMemberId(SQLModel):
    name:str
    phone:str