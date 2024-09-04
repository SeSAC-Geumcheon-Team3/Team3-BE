from fastapi import APIRouter, HTTPException, Query, Depends, Body, status
from sqlmodel import select, func
from typing import List, Optional

from board.model import Board
from board.schema import BoardCreateRequest, BoardResponse, BoardListResponse
from connection import get_session

board_router = APIRouter(
    tags=["Board"]
)

# 게시글 등록
@board_router.post("/board", status_code=201)
async def create_board(board_data: BoardCreateRequest = Body(...), session=Depends(get_session)) -> dict:
    member_idx = 1  # 임시 idx; JWT 수정 필요
    notice = 0  # default

    # 이미지 경로
    img_paths = board_data.imgs + [None] * (4 - len(board_data.imgs))

    new_board = Board(
        member_idx=member_idx,
        content=board_data.content,
        image_path1=img_paths[0],
        image_path2=img_paths[1],
        image_path3=img_paths[2],
        image_path4=img_paths[3],
        notice=notice
    )
    
    session.add(new_board)
    session.commit()
    session.refresh(new_board)

    return {"message": "게시글이 성공적으로 등록되었습니다"}

# 특정 게시글 조회
@board_router.get("/board", response_model=BoardResponse)
async def get_board(
    board_idx: int = Query(..., description="조회할 게시글의 idx"), 
    session=Depends(get_session)
) -> BoardResponse:

    board = session.get(Board, board_idx)
    
    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    image_paths = [board.image_path1, board.image_path2, board.image_path3, board.image_path4]
    
    return BoardResponse(
        board_idx=board.board_idx,
        member_idx=board.member_idx,
        nickname=board.nickname,
        content=board.content,
        like=board.like,
        created_at=board.created_at,
        image_paths=image_paths,
    )

# 게시글 조회
@board_router.get("/boards", response_model=BoardListResponse)
async def get_boards(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(25, ge=1, le=100, description="페이지당 항목 수"),
    session = Depends(get_session)
) -> BoardListResponse:

    total_items_query = select(func.count()).select_from(Board)
    total_items = session.exec(total_items_query).one()

    if total_items == 0:
        return BoardListResponse(
            size=size,
            page=page,
            total_pages=0,
            total_size=0,
            items=[]
        )

    offset = (page - 1) * size
    limit = size

    boards_query = select(Board).offset(offset).limit(limit)
    boards = session.exec(boards_query).all()

    items = []
    for board in boards:
        image_paths = [board.image_path1, board.image_path2, board.image_path3, board.image_path4]
        image_paths = [path for path in image_paths if path]

        items.append(BoardResponse(
            board_idx=board.board_idx,
            member_idx=board.member_idx,
            nickname=board.nickname,
            content=board.content,
            like=board.like,
            created_at=board.created_at,
            image_paths=image_paths
        ))

    total_pages = (total_items + size - 1) // size

    return BoardListResponse(
        size=size,
        page=page,
        total_pages=total_pages,
        total_size=total_items,
        items=items
    )

# 게시글 삭제
@board_router.delete("/board")
async def delete_board(board_idx: int = Query(..., description="삭제할 게시글의 idx"), session=Depends(get_session)) -> dict:
    board = session.get(Board, board_idx)
    
    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    session.delete(board)
    session.commit()

    return {"message": "게시글이 성공적으로 삭제되었습니다!"}