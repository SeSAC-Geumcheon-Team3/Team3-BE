from sqlmodel import create_engine, SQLModel, Session
from pydantic_settings import BaseSettings
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

# sqlite 연결 정보
# database_file = "planner.db"
# database_connection_string = f"sqlite:///{database_file}"
# connect_args = {"check_same_thread":False}
# engine_url = create_engine(database_connection_string, echo=True, connect_args=connect_args)


class Settings(BaseSettings):
    """
    .env의 변수를 가져옴
    """
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    EXP: Optional[int] = None
    ALGORITHM: Optional[str] = None
    UPLOAD_DIRECTORY: Optional[str] = None
    class Config:
        env_file = ".env"

# mysql 연결 정보
settings = Settings()
engine_url = create_engine(settings.DATABASE_URL, echo=True)

def conn():
    """
    DB와의 연결 생성
    """
    SQLModel.metadata.create_all(engine_url)    # 테이블 생성


def drop_create():
    """
    테이블 삭제 및 재생성
    """
    


def get_session():
    """
    DB와의 상호작용을 관리
    """
    try:
        with Session(engine_url) as session:
            yield session                           # 세션이 호출자에게 반환. return과 달리 종료x
    except Exception as e:
        print(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Session 생성 실패")
