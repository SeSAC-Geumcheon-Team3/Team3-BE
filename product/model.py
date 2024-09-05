from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class Product(SQLModel, table=True):
    idx: int = Field(default=None, primary_key=True)
    member_idx: Optional[int] = Field(default=None)  # 외래키 설정 추가 필요
    icon: str = ''
    product_name: str
    stock: int
    limit: int
    category: str
    update_date: date

class ProductLog(SQLModel, table=True):
    log_idx: int = Field(default=None, primary_key=True)
    product: str
    category: str
    used_number: int
    update_date: date
