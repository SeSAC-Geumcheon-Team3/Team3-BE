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
    name: str = Field(sa_column=Column(String, nullable=False))
    email: EmailStr = Field(sa_column=Column(String, unique=True, nullable=False))
    password: str = Field(sa_column=Column(String, nullable=False))
    nickname: str = Field(sa_column=Column(String, unique=True, nullable=False))
    phone: str = Field(sa_column=Column(String, nullable=False))
    authority: str = "기본 사용자"
    reported: int = 0
    profile_img: str = ""
    notice: bool = Field(sa_column=Column(String, nullable=False))
    sex: str = Field(sa_column=Column(String, nullable=False))
    household: int = 1 
