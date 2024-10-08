from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BoardCreateRequest(BaseModel):
    content: str
    imgs: Optional[List[str]] = []

class BoardResponse(BaseModel):
    board_idx: int
    member_idx: int
    nickname: Optional[str]
    content: str
    like: int
    created_at: datetime
    image_paths: List[Optional[str]]

class BoardListResponse(BaseModel):
    page: int
    size: int
    total_pages: int
    total_size: int
    items: List[BoardResponse]