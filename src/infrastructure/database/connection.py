"""데이터베이스 연결 관리"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config import settings

# SQLAlchemy Base
Base = declarative_base()

# MySQL Async Engine (mysqlclient는 동기 전용이므로 asyncmy 또는 aiomysql 사용)
# 참고: requirements.txt에 aiomysql 추가 필요
# DATABASE_URL 형식: mysql+aiomysql://user:password@host:port/database
ASYNC_DATABASE_URL = settings.database_url.replace("mysql://", "mysql+aiomysql://")

# 비동기 엔진 생성
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """데이터베이스 세션 의존성"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """데이터베이스 테이블 생성"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """데이터베이스 연결 종료"""
    await engine.dispose()
