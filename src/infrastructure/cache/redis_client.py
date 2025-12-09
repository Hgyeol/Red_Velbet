"""Redis 클라이언트"""
from typing import Optional
import redis.asyncio as aioredis

from src.config import settings


class RedisClient:
    """Redis 클라이언트"""

    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def connect(self):
        """Redis 연결"""
        self.redis = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )

    async def disconnect(self):
        """Redis 연결 해제"""
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[str]:
        """값 조회"""
        if not self.redis:
            await self.connect()
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None):
        """값 저장"""
        if not self.redis:
            await self.connect()
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        """값 삭제"""
        if not self.redis:
            await self.connect()
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """키 존재 여부 확인"""
        if not self.redis:
            await self.connect()
        return await self.redis.exists(key) > 0


# 싱글톤 인스턴스
redis_client = RedisClient()
