"""User Repository 인터페이스"""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from .entity import User


class UserRepository(ABC):
    """사용자 저장소 인터페이스"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """사용자 저장"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """ID로 사용자 조회"""
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        pass

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """사용자명 존재 여부 확인"""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """사용자 정보 업데이트"""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """사용자 삭제"""
        pass
