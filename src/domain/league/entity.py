"""League 엔티티"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class League:
    """리그 엔티티

    스포츠 리그의 핵심 정보를 담고 있는 엔티티
    """
    league_id: str
    league_name: str
    sport_type: str  # 축구, 야구, 농구, 배구
    country: str
    is_active: bool
    created_at: Optional[datetime] = None

    @staticmethod
    def create(
        league_name: str,
        sport_type: str,
        country: str,
        is_active: bool = True
    ) -> "League":
        """새로운 리그 생성

        Args:
            league_name: 리그 이름
            sport_type: 스포츠 종류 (축구, 야구, 농구, 배구)
            country: 국가
            is_active: 활성화 여부

        Returns:
            League: 새로운 리그 엔티티
        """
        return League(
            league_id=str(uuid.uuid4()),
            league_name=league_name,
            sport_type=sport_type,
            country=country,
            is_active=is_active,
            created_at=datetime.utcnow()
        )

    def activate(self) -> None:
        """리그 활성화"""
        self.is_active = True

    def deactivate(self) -> None:
        """리그 비활성화"""
        self.is_active = False
