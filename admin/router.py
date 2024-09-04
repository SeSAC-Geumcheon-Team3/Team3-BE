from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlmodel import select, func
from typing import List

from board.model import Board
from board.schema import BoardResponse, BoardListResponse
from admin.schema import AdminBoardResponse, AdminBoardListResponse
from connection import get_session

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# 전체 게시글 조회
@admin_router.get("/boards", response_model=AdminBoardListResponse)
async def get_boards(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    session=Depends(get_session)
) -> AdminBoardListResponse:

    total_items_query = select(func.count()).select_from(Board)
    total_items = session.exec(total_items_query).one()

    offset = (page - 1) * size
    limit = size

    boards_query = select(Board).offset(offset).limit(limit)
    boards = session.exec(boards_query).all()

    items = []
    for board in boards:
        image_paths = [board.image_path1, board.image_path2, board.image_path3, board.image_path4]
        items.append(AdminBoardResponse(
            board_idx=board.board_idx,
            member_idx=board.member_idx,
            nickname=board.nickname,
            content=board.content,
            like=board.like,
            created_at=board.created_at,
            image_paths=image_paths,
            notice=board.notice
        ))

    total_pages = (total_items + size - 1) // size

    return AdminBoardListResponse(
        page=page,
        size=size,
        total_pages=total_pages,
        total_size=total_items,
        items=items
    )

# 특정 게시글 조회
@admin_router.get("/board/detail", response_model=AdminBoardResponse)
async def get_board_detail(
    board_idx: int = Query(..., description="조회할 게시글의 idx"),
    session=Depends(get_session)
) -> AdminBoardResponse:
    
    board = session.get(Board, board_idx)
    
    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    image_paths = [board.image_path1, board.image_path2, board.image_path3, board.image_path4]
    
    return AdminBoardResponse(
        board_idx=board.board_idx,
        member_idx=board.member_idx,
        nickname=board.nickname,
        content=board.content,
        like=board.like,
        created_at=board.created_at,
        image_paths=image_paths,
        notice=board.notice
    )

# 신고당한 게시글만 조회
@admin_router.get("/board/reported", response_model=AdminBoardListResponse)
async def get_reported_boards(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    session=Depends(get_session)
) -> AdminBoardListResponse:

    total_items_query = select(func.count()).select_from(Board).where(Board.notice > 0)
    total_items = session.exec(total_items_query).one()

    offset = (page - 1) * size
    limit = size

    boards_query = select(Board).where(Board.notice > 0).offset(offset).limit(limit)
    boards = session.exec(boards_query).all()

    items = []
    for board in boards:
        image_paths = [board.image_path1, board.image_path2, board.image_path3, board.image_path4]
        items.append(AdminBoardResponse(
            board_idx=board.board_idx,
            member_idx=board.member_idx,
            nickname=board.member_idx,
            content=board.content,
            like=board.like,
            created_at=board.created_at,
            image_paths=image_paths,
            notice=board.notice
        ))

    total_pages = (total_items + size - 1) // size

    return AdminBoardListResponse(
        page=page,
        size=size,
        total_pages=total_pages,
        total_size=total_items,
        items=items
    )

# 게시글 삭제
@admin_router.delete("/board")
async def delete_board(board_idx: int = Query(..., description="삭제할 게시글의 idx"),session=Depends(get_session)) -> dict:
    board = session.get(Board, board_idx)
    
    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    session.delete(board)
    session.commit()

    return {"message": "게시글이 성공적으로 삭제되었습니다!"}
