from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class AdminBoardResponse(BaseModel):
    board_idx: int
    member_idx: int
    nickname: Optional[str]
    content: str
    like: int
    created_at: datetime
    image_paths: List[Optional[str]]
    notice: bool

class AdminBoardListResponse(BaseModel):
    page: int
    size: int
    total_pages: int
    total_size: int
    items: List[AdminBoardResponse]

# 회원 정보 응답 스키마
class MemberResponse(BaseModel):
    member_idx: int
    name: str
    email: EmailStr
    nickname: Optional[str] = None
    phone: str
    authority: str
    reported: Optional[int] = None
    profile_image: Optional[str] = None
    notice: bool
    birth: Optional[str] = None
    sex: Optional[str] = None
    household: Optional[int] = None

# 회원 목록 조회 응답 스키마
class MemberListResponse(BaseModel):
    page: int
    size: int
    total_pages: int
    total_size: int
    items: List[MemberResponse]

# 게시글 생성 요청 스키마
class BoardCreateRequest(BaseModel):
    content: str
    imgs: Optional[List[str]] = []

# 신고 횟수 추가 요청 스키마
class ReportMemberRequest(BaseModel):
    member_idx: int
    reported: int