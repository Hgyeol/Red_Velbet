"""인증 관련 Pydantic 스키마"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """회원가입 요청"""
    username: str = Field(..., min_length=4, max_length=50, description="사용자명")
    password: str = Field(..., min_length=8, description="비밀번호")
    email: EmailStr = Field(..., description="이메일")
    nickname: str = Field(..., min_length=2, max_length=50, description="닉네임")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "user123",
                "password": "password123!",
                "email": "user@example.com",
                "nickname": "닉네임"
            }]
        }
    }


class LoginRequest(BaseModel):
    """로그인 요청"""
    username: str = Field(..., description="사용자명")
    password: str = Field(..., description="비밀번호")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "user123",
                "password": "password123!"
            }]
        }
    }


class RefreshTokenRequest(BaseModel):
    """토큰 갱신 요청"""
    refresh_token: str = Field(..., description="Refresh Token")


class ChangePasswordRequest(BaseModel):
    """비밀번호 변경 요청"""
    current_password: str = Field(..., description="현재 비밀번호")
    new_password: str = Field(..., min_length=8, description="새 비밀번호")


class TokenResponse(BaseModel):
    """토큰 응답"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 900

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "550e8400-e29b-41d4-a716-446655440000",
                "token_type": "Bearer",
                "expires_in": 900
            }]
        }
    }


class LoginResponse(BaseModel):
    """로그인 응답"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: dict

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "550e8400-e29b-41d4-a716-446655440000",
                "token_type": "Bearer",
                "expires_in": 900,
                "user": {
                    "user_id": "550e8400-e29b-41d4-a716-446655440000",
                    "username": "user123",
                    "email": "user@example.com",
                    "nickname": "닉네임",
                    "role": "user"
                }
            }]
        }
    }


class MessageResponse(BaseModel):
    """일반 메시지 응답"""
    message: str
