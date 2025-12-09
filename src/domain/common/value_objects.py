"""도메인 공통 Value Objects"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class Email:
    """이메일 Value Object"""
    value: str

    def __post_init__(self):
        if not self.value or "@" not in self.value:
            raise ValueError("유효하지 않은 이메일 형식입니다")


@dataclass(frozen=True)
class Username:
    """사용자명 Value Object"""
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 4 or len(self.value) > 50:
            raise ValueError("사용자명은 4-50자 사이여야 합니다")
        if not self.value.replace("_", "").isalnum():
            raise ValueError("사용자명은 영문, 숫자, 언더스코어만 허용됩니다")


@dataclass(frozen=True)
class Password:
    """비밀번호 Value Object"""
    value: str

    def __post_init__(self):
        if not self.value or len(self.value) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다")

        # 영문, 숫자, 특수문자 포함 여부 확인
        has_letter = any(c.isalpha() for c in self.value)
        has_digit = any(c.isdigit() for c in self.value)
        has_special = any(not c.isalnum() for c in self.value)

        if not (has_letter and has_digit and has_special):
            raise ValueError("비밀번호는 영문, 숫자, 특수문자를 모두 포함해야 합니다")


@dataclass(frozen=True)
class Money:
    """금액 Value Object"""
    amount: Decimal

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, 'amount', Decimal(str(self.amount)))
        if self.amount < 0:
            raise ValueError("금액은 0 이상이어야 합니다")

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 더할 수 있습니다")
        return Money(self.amount + other.amount)

    def __sub__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 뺄 수 있습니다")
        return Money(self.amount - other.amount)

    def __lt__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 비교할 수 있습니다")
        return self.amount < other.amount

    def __le__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 비교할 수 있습니다")
        return self.amount <= other.amount

    def __gt__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 비교할 수 있습니다")
        return self.amount > other.amount

    def __ge__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            raise TypeError("Money 타입과만 비교할 수 있습니다")
        return self.amount >= other.amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount

    def __str__(self) -> str:
        return f"{self.amount}"
