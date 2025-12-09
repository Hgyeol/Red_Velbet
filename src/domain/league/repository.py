"""League Repository 인터페이스"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entity import League


class LeagueRepository(ABC):
    """리그 리포지토리 인터페이스"""

    @abstractmethod
    async def save(self, league: League) -> League:
        """리그 저장

        Args:
            league: 저장할 리그 엔티티

        Returns:
            League: 저장된 리그 엔티티
        """
        pass

    @abstractmethod
    async def find_by_id(self, league_id: str) -> Optional[League]:
        """ID로 리그 조회

        Args:
            league_id: 리그 ID

        Returns:
            Optional[League]: 조회된 리그 엔티티 또는 None
        """
        pass

    @abstractmethod
    async def find_all(
        self,
        sport_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[League], int]:
        """리그 목록 조회

        Args:
            sport_type: 스포츠 종류 필터
            is_active: 활성화 여부 필터
            skip: 건너뛸 개수
            limit: 조회할 최대 개수

        Returns:
            tuple[List[League], int]: (리그 목록, 전체 개수)
        """
        pass

    @abstractmethod
    async def update(self, league: League) -> League:
        """리그 정보 업데이트

        Args:
            league: 업데이트할 리그 엔티티

        Returns:
            League: 업데이트된 리그 엔티티
        """
        pass

    @abstractmethod
    async def delete(self, league_id: str) -> bool:
        """리그 삭제

        Args:
            league_id: 삭제할 리그 ID

        Returns:
            bool: 삭제 성공 여부
        """
        pass
