"""
DTO와 같이 데이터 전송에 사용되는 모델
"""
from pydantic import EmailStr
from sqlmodel import SQLModel


# 사용자 등록 시 전달되는 데이터 모델
class MemberSignUp(SQLModel):
    name: str
    email: EmailStr
    password: str
    nickname: str
    phone: str
    notice: bool
    sex: str
    household: int