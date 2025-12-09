from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.common.value_objects import Money


@dataclass
class Wallet:
    """
    지갑 도메인 엔티티
    사용자의 자산 정보를 나타냅니다.
    """
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    balance: Money = field(default_factory=lambda: Money(Decimal('0.00')))
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def deposit(self, amount: Money) -> None:
        """
        지갑에 금액을 입금합니다.
        """
        if amount.amount <= 0:
            raise ValueError("입금액은 0보다 커야 합니다.")
        self.balance += amount
        self.updated_at = datetime.utcnow()

    def withdraw(self, amount: Money) -> None:
        """
        지갑에서 금액을 출금합니다.
        잔액 부족 시 오류를 발생시킵니다.
        """
        if amount.amount <= 0:
            raise ValueError("출금액은 0보다 커야 합니다.")
        if self.balance < amount:
            raise ValueError("잔액이 부족합니다.")
        self.balance -= amount
        self.updated_at = datetime.utcnow()

    def __post_init__(self):
        if not isinstance(self.balance, Money):
            self.balance = Money(self.balance)
