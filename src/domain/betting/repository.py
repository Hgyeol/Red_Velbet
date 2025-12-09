"""Betting Repository 인터페이스"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import BettingOption


class BettingOptionRepository(ABC):
    """배팅 옵션 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, option: BettingOption) -> None:
        """배팅 옵션을 저장"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, option_id: str) -> Optional[BettingOption]:
        """ID로 배팅 옵션 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_game_id(self, game_id: str) -> List[BettingOption]:
        """게임 ID로 배팅 옵션 목록 조회"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, option_id: str) -> bool:
        """배팅 옵션을 삭제"""
        raise NotImplementedError
