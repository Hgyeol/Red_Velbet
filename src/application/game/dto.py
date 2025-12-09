"""Game DTOs"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.domain.game.enums import GameStatusEnum, SportTypeEnum


@dataclass
class GameDTO:
    """게임 정보 DTO"""
    game_id: str
    league_id: str
    home_team: str
    away_team: str
    start_time: datetime
    betting_deadline: datetime
    sport_type: str
    status: str
    is_live: bool
    final_score_home: Optional[int]
    final_score_away: Optional[int]
    created_at: datetime
    updated_at: datetime


@dataclass
class CreateGameDTO:
    """게임 생성 DTO"""
    league_id: str
    home_team: str
    away_team: str
    start_time: datetime
    betting_deadline: datetime
    sport_type: SportTypeEnum


@dataclass
class UpdateGameDTO:
    """게임 수정 DTO"""
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    start_time: Optional[datetime] = None
    betting_deadline: Optional[datetime] = None
    status: Optional[GameStatusEnum] = None
    is_live: Optional[bool] = None


@dataclass
class SetFinalScoreDTO:
    """최종 스코어 설정 DTO"""
    home_score: int
    away_score: int


@dataclass
class GameListDTO:
    """게임 목록 DTO"""
    items: List[GameDTO]
    total: int
    page: int
    limit: int
    total_pages: int


@dataclass
class SettleGameRequestDTO:
    """게임 정산 요청 DTO"""
    winning_option_ids: List[str]
