"""SQLAlchemy 데이터베이스 모델"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Numeric, Date, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.mysql import CHAR
import enum

from .connection import Base


class UserRoleEnum(str, enum.Enum):
    """사용자 권한 Enum"""
    USER = "user"
    ADMIN = "admin"


class UserModel(Base):
    """사용자 테이블"""
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nickname = Column(String(50), nullable=False)
    role = Column(SQLEnum(UserRoleEnum), default=UserRoleEnum.USER, nullable=False, index=True)
    daily_limit = Column(Numeric(15, 2), default=100000.00, nullable=False)
    today_total_bet = Column(Numeric(15, 2), default=0.00, nullable=False)
    last_bet_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_restricted = Column(Boolean, default=False, nullable=False)
