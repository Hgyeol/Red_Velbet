"""비밀번호 해싱 유틸리티"""
from passlib.context import CryptContext

from src.config import settings


class PasswordHasher:
    """bcrypt를 사용한 비밀번호 해싱"""

    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=settings.BCRYPT_ROUNDS
        )

    def hash(self, password: str) -> str:
        """비밀번호 해싱"""
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def needs_update(self, hashed_password: str) -> bool:
        """해시가 업데이트가 필요한지 확인"""
        return self.pwd_context.needs_update(hashed_password)


# 싱글톤 인스턴스
password_hasher = PasswordHasher()
