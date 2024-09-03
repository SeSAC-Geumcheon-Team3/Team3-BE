"""
사용자 모델
"""
from pydantic import EmailStr #,BaseModel
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel      # mysql


# 사용자 정보를 저장하는 데이터 모델(entity?)
class Member(SQLModel, table=True):
    member_idx: int = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password: str
    nickname: str
    phone: str
    authority: str = "기본 사용자"
    reported: int = 0
    profile_img: str = ""
    notice: bool
    sex: str
    household: int = 1
