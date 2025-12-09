"""토큰 저장소 (Redis)"""
from uuid import UUID, uuid4
from typing import Optional

from src.config import settings
from src.infrastructure.cache.redis_client import redis_client


class TokenRepository:
    """Refresh Token 저장소"""

    def __init__(self):
        self.redis = redis_client
        self.refresh_token_ttl = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # 초 단위
        self.access_token_ttl = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 초 단위

    async def save_refresh_token(self, user_id: UUID, token: str) -> None:
        """Refresh Token 저장"""
        key = f"refresh_token:{user_id}"
        await self.redis.set(key, token, expire=self.refresh_token_ttl)

    async def get_refresh_token(self, user_id: UUID) -> Optional[str]:
        """Refresh Token 조회"""
        key = f"refresh_token:{user_id}"
        return await self.redis.get(key)

    async def delete_refresh_token(self, user_id: UUID) -> None:
        """Refresh Token 삭제"""
        key = f"refresh_token:{user_id}"
        await self.redis.delete(key)

    async def verify_refresh_token(self, user_id: UUID, token: str) -> bool:
        """Refresh Token 검증"""
        stored_token = await self.get_refresh_token(user_id)
        return stored_token == token

    async def add_to_blacklist(self, token: str) -> None:
        """Access Token을 블랙리스트에 추가 (로그아웃 시)"""
        key = f"blacklist:{token}"
        await self.redis.set(key, "1", expire=self.access_token_ttl)

    async def is_blacklisted(self, token: str) -> bool:
        """토큰이 블랙리스트에 있는지 확인"""
        key = f"blacklist:{token}"
        return await self.redis.exists(key)

    def generate_refresh_token(self) -> str:
        """Refresh Token 생성 (UUID)"""
        return str(uuid4())


# 싱글톤 인스턴스
token_repository = TokenRepository()
