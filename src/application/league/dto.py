"""League DTO (Data Transfer Object)"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LeagueDTO:
    """리그 정보 DTO"""
    league_id: str
    league_name: str
    sport_type: str
    country: str
    is_active: bool
    created_at: datetime


@dataclass
class CreateLeagueDTO:
    """리그 생성 요청 DTO"""
    league_name: str
    sport_type: str
    country: str
    is_active: bool = True


@dataclass
class UpdateLeagueDTO:
    """리그 업데이트 요청 DTO"""
    league_name: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class LeagueListDTO:
    """리그 목록 DTO"""
    items: list[LeagueDTO]
    total: int
    page: int
    limit: int

    @property
    def total_pages(self) -> int:
        """전체 페이지 수 계산"""
        return (self.total + self.limit - 1) // self.limit
