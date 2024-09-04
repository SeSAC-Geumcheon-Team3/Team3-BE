from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Board(SQLModel, table=True):
    board_idx: int = Field(default=None, primary_key=True)
    member_idx: int = Field(nullable=False)
    nickname: Optional[str] = Field(default=None)
    content: str = Field(nullable=False, max_length=255)
    like: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    image_path1: Optional[str] = Field(default=None)
    image_path2: Optional[str] = Field(default=None)
    image_path3: Optional[str] = Field(default=None)
    image_path4: Optional[str] = Field(default=None)
    notice: int = Field(default=0)