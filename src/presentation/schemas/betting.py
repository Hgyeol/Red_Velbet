"""Betting API 스키마"""
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from src.domain.betting.enums import BettingOptionTypeEnum, BetTypeEnum


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


class BetSelectionRequest(BaseModel):
    """배팅 선택 요청 스키마"""
    option_id: str = Field(..., description="선택한 배팅 옵션 ID")


class PlaceBetRequest(BaseModel):
    """배팅 요청 스키마"""
    selections: List[BetSelectionRequest] = Field(..., min_items=1, description="배팅 선택 목록")
    amount: Decimal = Field(..., gt=0, description="배팅 금액")
    bet_type: BetTypeEnum = Field(..., description="배팅 타입 (단일/조합)")


class BetSlipResponse(BaseModel):
    """배팅 슬립 응답 스키마"""
    slip_id: str
    bet_id: str
    game_id: str
    option_id: str
    odds: Decimal
    result: str

    class Config:
        orm_mode = True


class BetResponse(BaseModel):
    """배팅 응답 스키마"""
    bet_id: str
    user_id: str
    bet_type: str
    total_amount: Decimal
    potential_return: Decimal
    total_odds: Decimal
    status: str
    slips: List[BetSlipResponse]

    class Config:
        orm_mode = True
