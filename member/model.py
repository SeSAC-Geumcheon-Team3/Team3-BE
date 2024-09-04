"""
사용자 모델
"""
from pydantic import EmailStr #,BaseModel
from typing import List, Optional
from sqlmodel import Field, Integer, SQLModel, Column,String, Boolean      # mysql


# 사용자 정보를 저장하는 데이터 모델(entity?)
class Member(SQLModel, table=True):
    member_idx: int = Field(
        sa_column=Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)  # primary_key와 기타 설정은 sa_column에서 지정)
    )
    name: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str = Field( nullable=False)
    nickname: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    authority: str = "기본 사용자"
    reported: int = 0
    profile_img: str = ""
    notice: bool = Field(nullable=False)
    birth: str
    sex: str = Field(nullable=False)
    household: int = 1 
