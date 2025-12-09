"""Betting 도메인 관련 Enums"""
import enum


class BettingOptionTypeEnum(str, enum.Enum):
    """배팅 옵션 타입 Enum"""
    WIN_DRAW_LOSS = "승무패"
    HANDICAP = "핸디캡"
    OVER_UNDER = "언오버"
    WINNER_PREDICTION = "승자예상"


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


class BetSlipResultEnum(str, enum.Enum):
    """배팅 슬립 결과 Enum"""
    PENDING = "대기"
    WIN = "적중"
    LOSS = "미적중"
