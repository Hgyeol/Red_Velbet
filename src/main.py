from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import init_db, close_db
from src.infrastructure.cache.redis_client import redis_client
from src.presentation.api.v1 import auth, users, wallet, leagues, games
from src.presentation.api.v1.betting import options_router, bets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클"""
    # Startup
    await init_db()
    await redis_client.connect()
    yield
    # Shutdown
    await close_db()
    await redis_client.disconnect()


app = FastAPI(
    title="배팅 사이트 API",
    description="스포츠 배팅 플랫폼 백엔드 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Wallet"])
app.include_router(leagues.router, prefix="/api/v1")
app.include_router(games.router, prefix="/api/v1")
app.include_router(options_router, prefix="/api/v1")
app.include_router(bets_router, prefix="/api/v1")


@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {
        "message": "배팅 사이트 API",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
