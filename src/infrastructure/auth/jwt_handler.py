"""JWT 토큰 생성 및 검증"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID

from jose import JWTError, jwt

from src.config import settings
from src.domain.common.exceptions import AuthenticationException


class JWTHandler:
    """JWT 토큰 핸들러"""

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(
        self,
        user_id: UUID,
        username: str,
        role: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Access Token 생성"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode = {
            "user_id": str(user_id),
            "username": username,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        """토큰 디코드 및 검증"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise AuthenticationException(f"토큰 검증 실패: {str(e)}")

    def verify_token(self, token: str) -> bool:
        """토큰 유효성 검증"""
        try:
            self.decode_token(token)
            return True
        except AuthenticationException:
            return False

    def get_user_id_from_token(self, token: str) -> UUID:
        """토큰에서 사용자 ID 추출"""
        payload = self.decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise AuthenticationException("토큰에 사용자 ID가 없습니다")
        return UUID(user_id)

    def get_username_from_token(self, token: str) -> str:
        """토큰에서 사용자명 추출"""
        payload = self.decode_token(token)
        username = payload.get("username")
        if not username:
            raise AuthenticationException("토큰에 사용자명이 없습니다")
        return username


# 싱글톤 인스턴스
jwt_handler = JWTHandler()
