"""User 도메인 엔티티"""
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class UserRole(str, Enum):
    """사용자 권한"""
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    """사용자 엔티티"""
    user_id: UUID = field(default_factory=uuid4)
    username: str = ""
    password_hash: str = ""
    nickname: str = ""
    bank_name: str = ""
    account_number: str = ""
    account_holder: str = ""
    role: UserRole = UserRole.USER
    daily_limit: Decimal = Decimal("100000.00")
    today_total_bet: Decimal = Decimal("0.00")
    last_bet_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_restricted: bool = False

    def update_password(self, new_password_hash: str) -> None:
        """비밀번호 변경"""
        self.password_hash = new_password_hash
        self.updated_at = datetime.utcnow()

    def update_profile(
        self,
        nickname: Optional[str] = None,
        bank_name: Optional[str] = None,
        account_number: Optional[str] = None,
        account_holder: Optional[str] = None,
    ) -> None:
        """프로필 정보 업데이트"""
        if nickname:
            self.nickname = nickname
        if bank_name:
            self.bank_name = bank_name
        if account_number:
            self.account_number = account_number
        if account_holder:
            self.account_holder = account_holder
        self.updated_at = datetime.utcnow()

    def set_daily_limit(self, limit: Decimal) -> None:
        """일일 배팅 한도 설정"""
        if limit < Decimal("10000") or limit > Decimal("1000000"):
            raise ValueError("일일 한도는 10,000원에서 1,000,000원 사이여야 합니다")
        self.daily_limit = limit
        self.updated_at = datetime.utcnow()

    def can_bet(self, amount: Decimal, today: date) -> bool:
        """배팅 가능 여부 확인"""
        if self.is_restricted:
            return False

        # 날짜가 바뀌면 오늘 총 배팅액 초기화
        if self.last_bet_date != today:
            self.today_total_bet = Decimal("0.00")
            self.last_bet_date = today

        # 일일 한도 확인
        return self.today_total_bet + amount <= self.daily_limit

    def record_bet(self, amount: Decimal, today: date) -> None:
        """배팅 기록"""
        if not self.can_bet(amount, today):
            raise ValueError("일일 배팅 한도를 초과했습니다")

        if self.last_bet_date != today:
            self.today_total_bet = Decimal("0.00")
            self.last_bet_date = today

        self.today_total_bet += amount
        self.updated_at = datetime.utcnow()

    def set_restriction(self, is_restricted: bool) -> None:
        """자가 제한 설정"""
        self.is_restricted = is_restricted
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """계정 비활성화"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """계정 활성화"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
