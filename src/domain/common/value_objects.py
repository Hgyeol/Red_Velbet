"""도메인 공통 Value Objects"""
from dataclasses import dataclass
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
