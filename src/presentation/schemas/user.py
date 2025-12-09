"""사용자 관련 Pydantic 스키마"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4


class UserResponse(BaseModel):
    """사용자 응답"""
    user_id: UUID4
    username: str
    email: str
    nickname: str
    role: str
    daily_limit: Decimal
    today_total_bet: Decimal
    last_bet_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_restricted: bool

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "username": "user123",
                "email": "user@example.com",
                "nickname": "닉네임",
                "role": "user",
                "daily_limit": 100000,
                "today_total_bet": 35000,
                "last_bet_date": "2024-01-15",
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-15T11:30:00Z",
                "is_active": True,
                "is_restricted": False
            }]
        }
    }


class UpdateProfileRequest(BaseModel):
    """프로필 수정 요청"""
    nickname: Optional[str] = Field(None, min_length=2, max_length=50, description="닉네임")
    email: Optional[EmailStr] = Field(None, description="이메일")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "nickname": "새닉네임",
                "email": "newemail@example.com"
            }]
        }
    }
