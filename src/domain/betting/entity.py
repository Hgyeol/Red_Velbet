"""Betting 엔티티"""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional, List
import uuid

from src.domain.betting.enums import BettingOptionTypeEnum, BetTypeEnum, BetStatusEnum, BetSlipResultEnum


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


@dataclass
class BetSlip:
    """배팅 슬립 엔티티"""
    bet_id: str
    game_id: str
    option_id: str
    odds: Decimal
    result: BetSlipResultEnum = BetSlipResultEnum.PENDING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Bet:
    """배팅 엔티티"""
    user_id: str
    bet_type: BetTypeEnum
    total_amount: Decimal
    potential_return: Decimal
    total_odds: Decimal
    status: BetStatusEnum = BetStatusEnum.PENDING
    slips: List[BetSlip] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def win(self):
        """배팅 적중"""
        self.status = BetStatusEnum.WIN

    def lose(self):
        """배팅 미적중"""
        self.status = BetStatusEnum.LOSS

    def cancel(self):
        """배팅 취소"""
        self.status = BetStatusEnum.CANCELLED
