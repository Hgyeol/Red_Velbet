"""Betting Repository 구현"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.betting.entity import BettingOption
from src.domain.betting.enums import BettingOptionTypeEnum
from src.domain.betting.repository import BettingOptionRepository
from src.infrastructure.database.models import BettingOptionModel


class BettingOptionRepositoryImpl(BettingOptionRepository):
    """BettingOption Repository 구현"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, option: BettingOption) -> None:
        """배팅 옵션을 저장"""
        option_model = BettingOptionModel(
            id=option.id,
            game_id=option.game_id,
            option_type=option.option_type,
            option_name=option.option_name,
            odds=option.odds,
            handicap_value=option.handicap_value,
            over_under_line=option.over_under_line,
            is_active=option.is_active,
        )
        self.session.add(option_model)
        await self.session.flush()

    async def find_by_id(self, option_id: str) -> Optional[BettingOption]:
        """ID로 배팅 옵션 조회"""
        stmt = select(BettingOptionModel).where(BettingOptionModel.id == option_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_game_id(self, game_id: str) -> List[BettingOption]:
        """게임 ID로 배팅 옵션 목록 조회"""
        stmt = select(BettingOptionModel).where(BettingOptionModel.game_id == game_id)
        result = await self.session.execute(stmt)
        return [self._to_entity(model) for model in result.scalars().all()]

    async def delete(self, option_id: str) -> bool:
        """배팅 옵션을 삭제"""
        stmt = select(BettingOptionModel).where(BettingOptionModel.id == option_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    def _to_entity(self, model: BettingOptionModel) -> BettingOption:
        """BettingOptionModel을 BettingOption 엔티티로 변환"""
        return BettingOption(
            id=model.id,
            game_id=model.game_id,
            option_type=BettingOptionTypeEnum(model.option_type),
            option_name=model.option_name,
            odds=model.odds,
            handicap_value=model.handicap_value,
            over_under_line=model.over_under_line,
            is_active=model.is_active,
        )
