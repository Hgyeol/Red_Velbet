"""Game Repository 인터페이스"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import Game


class GameRepository(ABC):
    """게임 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, game: Game) -> None:
        """게임을 저장"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, game_id: str) -> Optional[Game]:
        """ID로 게임 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        league_id: Optional[str] = None,
        status: Optional[str] = None,
        is_live: Optional[bool] = None,
        page: int = 1,
        limit: int = 20
    ) -> List[Game]:
        """조건에 맞는 게임 목록 조회"""
        raise NotImplementedError
    
    @abstractmethod
    async def count_all(
        self,
        league_id: Optional[str] = None,
        status: Optional[str] = None,
        is_live: Optional[bool] = None
    ) -> int:
        """조건에 맞는 게임 수 조회"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, game_id: str) -> bool:
        """게임을 삭제"""
        raise NotImplementedError
