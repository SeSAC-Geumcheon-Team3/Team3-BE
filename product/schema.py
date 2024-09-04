from pydantic import BaseModel
from typing import List
from datetime import date

class ProductItem(BaseModel):
    index: int
    memberIdx: int
    icon: str
    product: str
    category: str
    stock: int
    limit: int
    update_date: date

class ProductResponse(BaseModel):
    page: int
    size: int
    totalPages: int
    totalItems: int
    items: List[ProductItem]

class ProductCreateRequest(BaseModel):
    product_name: str
    icon: str
    stock: int
    limit: int
    category: str
    update_date: date

class ProductUpdate(BaseModel):
    idx: int
    category: str
    stock: int
    limit: int

class ProductUpdateRequest(BaseModel):
    data: List[ProductUpdate]

class LinearData(BaseModel):
    category: str
    spend: float
    date: str

class PieData(BaseModel):
    category: str
    spend: float

class ProductLogResponse(BaseModel):
    year: int
    linear: List[LinearData]
    pie: List[PieData]
    total: float
