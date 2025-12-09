"""Game API 스키마"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from src.domain.game.enums import GameStatusEnum, SportTypeEnum
from .common import PaginationInfo


class GameResponse(BaseModel):
    """게임 응답 스키마"""
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

    class Config:
        orm_mode = True


class CreateGameRequest(BaseModel):
    """게임 생성 요청 스키마"""
    league_id: str = Field(..., description="리그 ID")
    home_team: str = Field(..., description="홈팀 이름")
    away_team: str = Field(..., description="어웨이팀 이름")
    start_time: datetime = Field(..., description="경기 시작 시간")
    betting_deadline: datetime = Field(..., description="배팅 마감 시간")
    sport_type: SportTypeEnum = Field(..., description="스포츠 종류")


class UpdateGameRequest(BaseModel):
    """게임 수정 요청 스키마"""
    home_team: Optional[str] = Field(None, description="홈팀 이름")
    away_team: Optional[str] = Field(None, description="어웨이팀 이름")
    start_time: Optional[datetime] = Field(None, description="경기 시작 시간")
    betting_deadline: Optional[datetime] = Field(None, description="배팅 마감 시간")
    status: Optional[GameStatusEnum] = Field(None, description="경기 상태")
    is_live: Optional[bool] = Field(None, description="라이브 여부")


class SetFinalScoreRequest(BaseModel):
    """최종 스코어 설정 요청 스키마"""
    home_score: int = Field(..., ge=0, description="홈팀 최종 스코어")
    away_score: int = Field(..., ge=0, description="어웨이팀 최종 스코어")


class GameListResponse(BaseModel):
    """게임 목록 응답 스키마"""
    items: List[GameResponse]
    pagination: PaginationInfo


class SettleGameRequest(BaseModel):
    """게임 정산 요청 스키마"""
    winning_option_ids: List[str] = Field(..., min_items=1, description="적중한 배팅 옵션 ID 목록")
