from pydantic import BaseModel
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
    notice: int

class AdminBoardListResponse(BaseModel):
    page: int
    size: int
    total_pages: int
    total_size: int
    items: List[AdminBoardResponse]