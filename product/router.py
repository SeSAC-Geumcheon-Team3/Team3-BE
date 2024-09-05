from fastapi import APIRouter, HTTPException, Query, Depends, Body, status
from typing import List, Dict
from product.model import Product, ProductLog
from product.schema import ProductCreateRequest, ProductItem, ProductResponse, ProductUpdateRequest, ProductLogResponse, LinearData, PieData
from connection import get_session
from sqlmodel import select, func
from member.auth import get_access_token

product_router = APIRouter(
    tags=["Products"]
)

# 데이터 목록
product_list = []
product_logs = []


# 생필품 조회
@product_router.get("/product", response_model=ProductResponse)
async def get_products(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(25, ge=1, le=100, description="페이지당 항목 수"),
    session=Depends(get_session),
    token = Depends(get_access_token)
) -> ProductResponse:

    member_idx = token["member_idx"]

    total_items_query = select(func.count()).select_from(Product).where(Product.member_idx==member_idx)
    total_items = session.exec(total_items_query).one()  # 총 생필품 수

    if total_items == 0:
        return ProductResponse(
            totalItems=0,
            items=[]
        )

    products_query = select(Product).where(Product.member_idx==member_idx)
    products = session.exec(products_query).all()

    items_pydantic = [
        ProductItem(
            idx=product.idx,
            icon=product.icon,
            product=product.product_name,
            category=product.category,
            stock=product.stock,
            limit=product.limit,
            update_date=product.update_date
        ) for product in products
    ]

    return ProductResponse(
        totalItems=total_items,
        items=items_pydantic
    )


# 생필품 목록 입력
@product_router.post("/product", status_code=201)
async def add_product(product_data: ProductCreateRequest = Body(...), session=Depends(get_session), token=Depends(get_access_token)) -> dict:
    member_idx = token["member_idx"]

    new_product = Product(
        member_idx=member_idx,
        icon=product_data.icon,
        product_name=product_data.product_name,
        stock=product_data.stock,
        limit=product_data.limit,
        category=product_data.category,
        update_date=product_data.update_date
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    
    return {"message": "생필품 목록이 성공적으로 생성되었습니다"}

# 생필품 삭제
@product_router.delete("/product")
async def delete_product(idx: int = Query(..., description="삭제할 생필품의 idx"), session = Depends(get_session), token=Depends(get_access_token)) -> dict:
    member_idx = token["member_idx"]
    product = session.get(Product, idx)
    
    if not product:
        raise HTTPException(status_code=404, detail="생필품을 찾을 수 없습니다.")
    
    if product.member_idx != member_idx:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="삭제 권한이 없습니다")
    
    session.delete(product)
    session.commit()    
    
    deleted_product = session.get(Product, idx)
    if deleted_product:
        raise HTTPException(status_code=500, detail="생필품 삭제에 실패했습니다.")
    
    return {"message": "선택하신 생필품이 삭제되었습니다."}


# 생필품 수정
@product_router.put("/product", response_model=dict)
async def update_products(request: ProductUpdateRequest, session = Depends(get_session), token=Depends(get_access_token)) -> dict:
    member_idx = token["member_idx"]
    updated_idxs = set()

    for update in request.data:
        product = session.get(Product, update.idx)

        if product.member_idx != member_idx:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="삭제 권한이 없습니다.")


        if product:
            product_data = update.dict(exclude_unset=True)
            for key, value in product_data.items():
                setattr(product, key, value)

            session.add(product)
            session.commit()
            session.refresh(product)
            updated_idxs.add(update.idx)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"생필품 ID {update.idx}을(를) 찾을 수 없습니다.")

    if len(updated_idxs) == len(request.data):
        return {"message": "생필품 정보가 수정되었습니다."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="생필품을 찾을 수 없습니다.")


# 생필품 집계 보고서 조회
@product_router.get("/product/logs", response_model=ProductLogResponse)
async def get_product_logs(year: int = Query(..., description="조회할 연도"), session = Depends(get_session), token=Depends(get_access_token)) -> ProductLogResponse:
    
    member_idx = token["member_idx"]

    statement = select(ProductLog).where((func.YEAR(ProductLog.update_date) == year) & (ProductLog.member_idx)==member_idx)
    filtered_logs = session.exec(statement).all()

    if not filtered_logs:
        raise HTTPException(status_code=404, detail="해당 연도에 대한 데이터가 없습니다.")
    
    # LinearData
    linear_data = [LinearData(category=log.category, spend=log.used_number, date=log.update_date.strftime('%Y-%m-%d')) for log in filtered_logs]

    # PieData
    pie_data_dict: Dict[str, float] = {}
    for log in filtered_logs:
        if log.category in pie_data_dict:
            pie_data_dict[log.category] += log.used_number
        else:
            pie_data_dict[log.category] = log.used_number
    
    pie_data = [PieData(category=cat, spend=spend) for cat, spend in pie_data_dict.items()]
    total_spend = sum(log.used_number for log in filtered_logs)
    
    response = ProductLogResponse(
        year=year,
        linear=linear_data,
        pie=pie_data,
        total=total_spend
    )
    
    return response
