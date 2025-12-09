"""Betting DTOs"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List

from src.domain.betting.enums import BettingOptionTypeEnum, BetTypeEnum, BetStatusEnum


@dataclass
class BettingOptionDTO:
    """배팅 옵션 정보 DTO"""
    option_id: str
    game_id: str
    option_type: str
    option_name: str
    odds: Decimal
    is_active: bool
    handicap_value: Optional[Decimal]
    over_under_line: Optional[Decimal]


@dataclass
class CreateBettingOptionDTO:
    """배팅 옵션 생성 DTO"""
    game_id: str
    option_type: BettingOptionTypeEnum
    option_name: str
    odds: Decimal
    handicap_value: Optional[Decimal] = None
    over_under_line: Optional[Decimal] = None


@dataclass
class UpdateBettingOptionDTO:
    """배팅 옵션 수정 DTO"""
    odds: Optional[Decimal] = None
    is_active: Optional[bool] = None


@dataclass
class BetSelectionDTO:
    """배팅 선택 DTO"""
    option_id: str


@dataclass
class PlaceBetRequestDTO:
    """배팅 요청 DTO"""
    selections: List[BetSelectionDTO]
    amount: Decimal
    bet_type: BetTypeEnum


@dataclass
class BetSlipDTO:
    """배팅 슬립 DTO"""
    slip_id: str
    bet_id: str
    game_id: str
    option_id: str
    odds: Decimal
    result: str


@dataclass
class BetDTO:
    """배팅 정보 DTO"""
    bet_id: str
    user_id: str
    bet_type: str
    total_amount: Decimal
    potential_return: Decimal
    total_odds: Decimal
    status: str
    slips: List[BetSlipDTO]
