"""Betting 엔티티"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
import uuid

from src.domain.betting.enums import BettingOptionTypeEnum


@dataclass
class BettingOption:
    """배팅 옵션 엔티티"""
    game_id: str
    option_type: BettingOptionTypeEnum
    option_name: str
    odds: Decimal
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    handicap_value: Optional[Decimal] = None
    over_under_line: Optional[Decimal] = None

    def deactivate(self):
        """옵션 비활성화"""
        self.is_active = False

    def update_odds(self, new_odds: Decimal):
        """배당률 업데이트"""
        if new_odds <= 0:
            raise ValueError("배당률은 0보다 커야 합니다.")
        self.odds = new_odds
