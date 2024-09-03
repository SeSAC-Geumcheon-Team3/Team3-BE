from contextlib import asynccontextmanager
from fastapi import FastAPI
# from routes.users import user_router
# from routes.events import event_router
from connection import conn
from fastapi.middleware.cors import CORSMiddleware #참고: https://fastapi.tiangolo.com/ko/tutorial/cors/#corsmiddleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    conn()  # 어플리케이션 구동 시점에 conn 실행-db연결 생성
    yield   # 애플리케이션 종료 시점에 실행할 코드를 yield 밑에 추가


# FastAPI 객체 생성. lifespan: fastAPI 객체의 라이프사이클 중 특정 시점에 수행할 함수
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:3000/",
    "http://localhost:3000/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# user 추가
# app.include_router(user_router, prefix="/user")
# app.include_router(event_router, prefix="/event")


# main이라는 이름의 파일이 직접 실행되는가(다른 모듈에 포함되어 실행되는 것이 아님)
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

