"""Game Repository 구현"""
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.game.entity import Game
from src.domain.game.enums import GameStatusEnum, SportTypeEnum
from src.domain.game.repository import GameRepository
from src.infrastructure.database.models import GameModel


class GameRepositoryImpl(GameRepository):
    """Game Repository 구현"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, game: Game) -> None:
        """게임을 저장"""
        game_model = GameModel(
            id=game.id,
            league_id=game.league_id,
            external_id=game.external_id,
            sport_type=game.sport_type,
            home_team=game.home_team,
            away_team=game.away_team,
            start_time=game.start_time,
            status=game.status,
            final_score_home=game.final_score_home,
            final_score_away=game.final_score_away,
            betting_deadline=game.betting_deadline,
            is_live=game.is_live,
            created_at=game.created_at,
            updated_at=game.updated_at
        )
        self.session.add(game_model)
        await self.session.flush()

    async def find_by_id(self, game_id: str) -> Optional[Game]:
        """ID로 게임 조회"""
        stmt = select(GameModel).where(GameModel.id == game_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_all(
        self,
        league_id: Optional[str] = None,
        status: Optional[str] = None,
        is_live: Optional[bool] = None,
        page: int = 1,
        limit: int = 20
    ) -> List[Game]:
        """조건에 맞는 게임 목록 조회"""
        stmt = select(GameModel)
        if league_id:
            stmt = stmt.where(GameModel.league_id == league_id)
        if status:
            stmt = stmt.where(GameModel.status == GameStatusEnum(status))
        if is_live is not None:
            stmt = stmt.where(GameModel.is_live == is_live)
        
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def count_all(
        self,
        league_id: Optional[str] = None,
        status: Optional[str] = None,
        is_live: Optional[bool] = None
    ) -> int:
        """조건에 맞는 게임 수 조회"""
        stmt = select(func.count(GameModel.id))
        if league_id:
            stmt = stmt.where(GameModel.league_id == league_id)
        if status:
            stmt = stmt.where(GameModel.status == GameStatusEnum(status))
        if is_live is not None:
            stmt = stmt.where(GameModel.is_live == is_live)
        
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, game_id: str) -> bool:
        """게임을 삭제"""
        stmt = select(GameModel).where(GameModel.id == game_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    def _to_entity(self, model: GameModel) -> Game:
        """GameModel을 Game 엔티티로 변환"""
        return Game(
            id=model.id,
            league_id=model.league_id,
            external_id=model.external_id,
            sport_type=SportTypeEnum(model.sport_type),
            home_team=model.home_team,
            away_team=model.away_team,
            start_time=model.start_time,
            status=GameStatusEnum(model.status),
            final_score_home=int(model.final_score_home) if model.final_score_home is not None else None,
            final_score_away=int(model.final_score_away) if model.final_score_away is not None else None,
            betting_deadline=model.betting_deadline,
            is_live=model.is_live,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
