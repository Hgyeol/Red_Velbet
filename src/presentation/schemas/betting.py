"""Betting API 스키마"""
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from src.domain.betting.enums import BettingOptionTypeEnum


class BettingOptionResponse(BaseModel):
    """배팅 옵션 응답 스키마"""
    option_id: str
    game_id: str
    option_type: str
    option_name: str
    odds: Decimal
    is_active: bool
    handicap_value: Optional[Decimal] = None
    over_under_line: Optional[Decimal] = None

    class Config:
        orm_mode = True


class CreateBettingOptionRequest(BaseModel):
    """배팅 옵션 생성 요청 스키마"""
    game_id: str = Field(..., description="게임 ID")
    option_type: BettingOptionTypeEnum = Field(..., description="배팅 옵션 타입")
    option_name: str = Field(..., description="배팅 옵션 이름 (e.g., '홈팀 승', '오버')")
    odds: Decimal = Field(..., gt=0, description="배당률")
    handicap_value: Optional[Decimal] = Field(None, description="핸디캡 값 (핸디캡 배팅 시)")
    over_under_line: Optional[Decimal] = Field(None, description="언오버 기준점 (언오버 배팅 시)")


class UpdateBettingOptionRequest(BaseModel):
    """배팅 옵션 수정 요청 스키마"""
    odds: Optional[Decimal] = Field(None, gt=0, description="새로운 배당률")
    is_active: Optional[bool] = Field(None, description="활성화 여부")
