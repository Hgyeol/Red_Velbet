"""Betting Repository 인터페이스"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import BettingOption, Bet, BetSlip


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


class BetRepository(ABC):
    """배팅 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, bet: Bet) -> None:
        """배팅을 저장"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, bet_id: str) -> Optional[Bet]:
        """ID로 배팅 조회"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Bet]:
        """사용자 ID로 배팅 목록 조회"""
        raise NotImplementedError


class BetSlipRepository(ABC):
    """배팅 슬립 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, slip: BetSlip) -> None:
        """배팅 슬립을 저장"""
        raise NotImplementedError

    @abstractmethod
    async def find_by_bet_id(self, bet_id: str) -> List[BetSlip]:
        """배팅 ID로 슬립 목록 조회"""
        raise NotImplementedError
