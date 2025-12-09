"""Game 도메인 관련 Enums"""
import enum


class SportTypeEnum(str, enum.Enum):
    """스포츠 종류 Enum"""
    SOCCER = "축구"
    BASEBALL = "야구"
    BASKETBALL = "농구"
    VOLLEYBALL = "배구"


class GameStatusEnum(str, enum.Enum):
    """경기 상태 Enum"""
    SCHEDULED = "예정"
    LIVE = "라이브"
    CLOSED = "마감"
    FINISHED = "종료"
    CANCELLED = "취소"
