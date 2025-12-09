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


class WalletModel(Base):
    """지갑 테이블"""
    __tablename__ = "wallets"

    id = Column(CHAR(36), primary_key=True, index=True)
    user_id = Column(CHAR(36), unique=True, nullable=False, index=True)
    balance = Column(Numeric(15, 2), default=0.00, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SportTypeEnum(str, enum.Enum):
    """스포츠 종류 Enum"""
    SOCCER = "축구"
    BASEBALL = "야구"
    BASKETBALL = "농구"
    VOLLEYBALL = "배구"


class LeagueModel(Base):
    """리그 테이블"""
    __tablename__ = "leagues"

    id = Column(CHAR(36), primary_key=True, index=True)
    league_name = Column(String(100), nullable=False)
    sport_type = Column(SQLEnum(SportTypeEnum), nullable=False, index=True)
    country = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class GameStatusEnum(str, enum.Enum):
    """경기 상태 Enum"""
    SCHEDULED = "예정"
    LIVE = "라이브"
    CLOSED = "마감"
    FINISHED = "종료"
    CANCELLED = "취소"


class GameModel(Base):
    """경기 테이블"""
    __tablename__ = "games"

    id = Column(CHAR(36), primary_key=True, index=True)
    league_id = Column(CHAR(36), nullable=False, index=True)
    external_id = Column(String(100), nullable=True, index=True)
    sport_type = Column(SQLEnum(SportTypeEnum), nullable=False, index=True)
    home_team = Column(String(100), nullable=False)
    away_team = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False, index=True)
    status = Column(SQLEnum(GameStatusEnum), default=GameStatusEnum.SCHEDULED, nullable=False, index=True)
    final_score_home = Column(Numeric(10, 0), nullable=True)
    final_score_away = Column(Numeric(10, 0), nullable=True)
    betting_deadline = Column(DateTime, nullable=False)
    is_live = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class BettingOptionTypeEnum(str, enum.Enum):
    """배팅 옵션 타입 Enum"""
    WIN_DRAW_LOSS = "승무패"
    HANDICAP = "핸디캡"
    OVER_UNDER = "언오버"
    WINNER_PREDICTION = "승자예상"


class BettingOptionModel(Base):
    """배팅 옵션 테이블"""
    __tablename__ = "betting_options"

    id = Column(CHAR(36), primary_key=True, index=True)
    game_id = Column(CHAR(36), nullable=False, index=True)
    option_type = Column(SQLEnum(BettingOptionTypeEnum), nullable=False, index=True)
    option_name = Column(String(100), nullable=False)
    odds = Column(Numeric(10, 2), nullable=False)
    handicap_value = Column(Numeric(5, 2), nullable=True)
    over_under_line = Column(Numeric(5, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class FavoriteModel(Base):
    """즐겨찾기 테이블"""
    __tablename__ = "favorites"

    id = Column(CHAR(36), primary_key=True, index=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    game_id = Column(CHAR(36), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class BetTypeEnum(str, enum.Enum):
    """배팅 타입 Enum"""
    SINGLE = "단일"
    COMBO = "조합"


class BetStatusEnum(str, enum.Enum):
    """배팅 상태 Enum"""
    PENDING = "대기"
    WIN = "적중"
    LOSS = "미적중"
    CANCELLED = "취소"


class BetModel(Base):
    """배팅 테이블"""
    __tablename__ = "bets"

    id = Column(CHAR(36), primary_key=True, index=True)
    user_id = Column(CHAR(36), nullable=False, index=True)
    bet_type = Column(SQLEnum(BetTypeEnum), nullable=False)
    total_amount = Column(Numeric(15, 2), nullable=False)
    potential_return = Column(Numeric(15, 2), nullable=False)
    total_odds = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(BetStatusEnum), default=BetStatusEnum.PENDING, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class BetSlipResultEnum(str, enum.Enum):
    """배팅 슬립 결과 Enum"""
    PENDING = "대기"
    WIN = "적중"
    LOSS = "미적중"


class BetSlipModel(Base):
    """배팅 슬립 테이블"""
    __tablename__ = "bet_slips"

    id = Column(CHAR(36), primary_key=True, index=True)
    bet_id = Column(CHAR(36), nullable=False, index=True)
    game_id = Column(CHAR(36), nullable=False, index=True)
    option_id = Column(CHAR(36), nullable=False)
    odds = Column(Numeric(10, 2), nullable=False)
    result = Column(SQLEnum(BetSlipResultEnum), default=BetSlipResultEnum.PENDING, nullable=False)


class TransactionTypeEnum(str, enum.Enum):
    """거래 타입 Enum"""
    DEPOSIT = "충전"
    WITHDRAW = "출금"
    BET = "배팅"
    REFUND = "환급"


class TransactionModel(Base):
    """거래 내역 테이블"""
    __tablename__ = "transactions"

    id = Column(CHAR(36), primary_key=True, index=True)
    wallet_id = Column(CHAR(36), nullable=False, index=True)
    transaction_type = Column(SQLEnum(TransactionTypeEnum), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    balance_after = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
