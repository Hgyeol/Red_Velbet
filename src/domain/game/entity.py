"""Game 엔티티"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from src.domain.game.enums import GameStatusEnum, SportTypeEnum


@dataclass
class Game:
    """경기 엔티티"""
    league_id: str
    home_team: str
    away_team: str
    start_time: datetime
    betting_deadline: datetime
    sport_type: SportTypeEnum
    status: GameStatusEnum = GameStatusEnum.SCHEDULED
    is_live: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    external_id: Optional[str] = None
    final_score_home: Optional[int] = None
    final_score_away: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def change_status(self, new_status: GameStatusEnum):
        """경기 상태 변경"""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def set_final_score(self, home_score: int, away_score: int):
        """경기 최종 스코어 설정"""
        if self.status not in [GameStatusEnum.LIVE, GameStatusEnum.FINISHED]:
            raise ValueError("경기가 진행중이거나 종료된 상태에서만 스코어를 설정할 수 있습니다.")
        self.final_score_home = home_score
        self.final_score_away = away_score
        self.change_status(GameStatusEnum.FINISHED)

    def to_live(self):
        """라이브 상태로 변경"""
        self.is_live = True
        self.change_status(GameStatusEnum.LIVE)
