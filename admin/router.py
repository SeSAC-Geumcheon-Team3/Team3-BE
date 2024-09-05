from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlmodel import select, func
from typing import List

from board.model import Board
from member.model import Member
from admin.schema import AdminBoardResponse, AdminBoardListResponse, MemberResponse, MemberListResponse, BoardCreateRequest, ReportMemberRequest
from connection import get_session
from member.auth import get_admin_access_token

admin_router = APIRouter(
    tags=["Admin"]
)

# 전체 게시글 조회
@admin_router.get("/boards", response_model=AdminBoardListResponse)
async def get_boards(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    session=Depends(get_session),
    token=Depends(get_admin_access_token)
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
            #notice=board.notice
            notice=board.notice > 0
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
    session=Depends(get_session),
    token=Depends(get_admin_access_token)
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
    session=Depends(get_session),
    token=Depends(get_admin_access_token)
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
async def delete_board(board_idx: int = Query(..., description="삭제할 게시글의 idx"),session=Depends(get_session),token=Depends(get_admin_access_token)) -> dict:
    board = session.get(Board, board_idx)
    
    if not board:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    session.delete(board)
    session.commit()

    return {"message": "게시글이 성공적으로 삭제되었습니다!"}

# 멤버 강제 탈퇴
@admin_router.delete("/member")
async def force_delete_member(member_idx: int, session=Depends(get_session), token=Depends(get_admin_access_token)) -> dict:
    
    # 요청한 사용자의 idx를 사용하여 사용자 권한을 데이터베이스에서 조회
    requester_idx = token.get("member_idx")

    if not requester_idx:
        raise HTTPException(status_code=401, detail="사용자 정보가 없습니다.")
    
    requester = session.get(Member, requester_idx)
    if not requester:
        raise HTTPException(status_code=404, detail="요청한 사용자를 찾을 수 없습니다.")
    
    if requester.authority != "관리자":
        raise HTTPException(status_code=401, detail="사용 권한이 없습니다.")
    
    # 삭제할 멤버 조회
    member = session.get(Member, member_idx)
    
    if not member:
        raise HTTPException(status_code=404, detail="멤버를 찾을 수 없습니다.")
    
    # 멤버 삭제
    session.delete(member)
    session.commit()

    return {"message": "해당 멤버가 강퇴되었습니다"}

# 회원 정보 조회
@admin_router.get("/member", response_model=MemberListResponse)
async def get_members(
    page: int = Query(1, ge=1),
    size: int = Query(25, ge=1, le=100),
    session=Depends(get_session),
    token=Depends(get_admin_access_token)
) -> MemberListResponse:

    # 요청한 사용자의 idx를 사용하여 사용자 권한을 데이터베이스에서 조회
    requester_idx = token.get("member_idx")

    if not requester_idx:
        raise HTTPException(status_code=401, detail="사용자 정보가 없습니다.")
    
    requester = session.get(Member, requester_idx)
    if not requester:
        raise HTTPException(status_code=404, detail="요청한 사용자를 찾을 수 없습니다.")
    
    if requester.authority != "관리자":
        raise HTTPException(status_code=401, detail="사용 권한이 없습니다.")

    total_items_query = select(func.count()).select_from(Member)
    total_items = session.exec(total_items_query).one()

    offset = (page - 1) * size
    limit = size

    members_query = select(Member).offset(offset).limit(limit)
    members = session.exec(members_query).all()

    items = [MemberResponse(
        member_idx=member.member_idx,
        name=member.name,
        email=member.email,
        nickname=member.nickname,
        phone=member.phone,
        authority=member.authority,
        reported=member.reported,
        profile_image=member.profile_img,
        notice=member.notice,
        birth=member.birth,
        sex=member.sex,
        household=member.household
    ) for member in members]

    total_pages = (total_items + size - 1) // size

    return MemberListResponse(
        page=page,
        size=size,
        total_pages=total_pages,
        total_size=total_items,
        items=items
    )

# 게시글 등록
@admin_router.post("/board", status_code=201)
async def create_board(board_data: BoardCreateRequest = Body(...), session=Depends(get_session), token=Depends(get_admin_access_token)) -> dict:

    # 요청한 사용자의 idx를 사용하여 사용자 권한을 데이터베이스에서 조회
    requester_idx = token.get("member_idx")

    if not requester_idx:
        raise HTTPException(status_code=401, detail="사용자 정보가 없습니다.")
    
    requester = session.get(Member, requester_idx)
    if not requester:
        raise HTTPException(status_code=404, detail="요청한 사용자를 찾을 수 없습니다.")
    
    if requester.authority != "관리자":
        raise HTTPException(status_code=401, detail="사용 권한이 없습니다.")
    
    member_idx = token["member_idx"]
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

# 신고 횟수 추가
@admin_router.post("/member/add_reported")
async def add_reported_count(
    report_member_request: ReportMemberRequest = Body(...),
    session=Depends(get_session),
    token=Depends(get_admin_access_token)
) -> dict:
    
    # 요청한 사용자의 idx를 사용하여 사용자 권한을 데이터베이스에서 조회
    requester_idx = token.get("member_idx")

    if not requester_idx:
        raise HTTPException(status_code=401, detail="사용자 정보가 없습니다.")
    
    requester = session.get(Member, requester_idx)
    if not requester:
        raise HTTPException(status_code=404, detail="요청한 사용자를 찾을 수 없습니다.")
    
    if requester.authority != "관리자":
        raise HTTPException(status_code=401, detail="사용 권한이 없습니다.")

    member = session.get(Member, report_member_request.member_idx)
    
    if not member:
        raise HTTPException(status_code=404, detail="멤버를 찾을 수 없습니다.")
    
    member.reported = report_member_request.reported  # `reported` 값 업데이트
    session.add(member)
    session.commit()

    return {"message": "신고가 완료되었습니다"}