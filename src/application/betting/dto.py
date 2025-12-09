"""Betting DTOs"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List

from src.domain.betting.enums import BettingOptionTypeEnum


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
