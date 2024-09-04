from fastapi import Request
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

async def handle_integrity_error(request: Request, exc: IntegrityError):
    if "UNIQUE constraint failed" in str(exc.orig):
        return JSONResponse(
            status_code=409,
            content={"detail": "이미 존재하는 사용자입니다"},
        )
    elif "NOT NULL constraint failed" in str(exc.orig):
        return JSONResponse(
            status_code=400,
            content={"detail": "필수 입력 필드가 누락되었습니다"},
        )
    return JSONResponse(
        status_code=400,
        content={"detail": "데이터베이스 제약 조건 위반: " + str(exc)},
    )
