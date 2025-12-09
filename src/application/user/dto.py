"""User DTO (Data Transfer Object)"""
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class UserDTO:
    """사용자 DTO"""
    user_id: UUID
    username: str
    nickname: str
    bank_name: str
    account_number: str
    account_holder: str
    role: str
    daily_limit: Decimal
    today_total_bet: Decimal
    last_bet_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_restricted: bool


@dataclass
class RegisterUserDTO:
    """회원가입 요청 DTO"""
    username: str
    password: str
    nickname: str
    bank_name: str
    account_number: str
    account_holder: str


@dataclass
class LoginDTO:
    """로그인 요청 DTO"""
    username: str
    password: str


@dataclass
class AuthTokenDTO:
    """인증 토큰 DTO"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900  # 15분


@dataclass
class UpdateProfileDTO:
    """프로필 수정 DTO"""
    nickname: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_holder: Optional[str] = None


@dataclass
class ChangePasswordDTO:
    """비밀번호 변경 DTO"""
    current_password: str
    new_password: str
