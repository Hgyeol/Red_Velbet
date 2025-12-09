"""League Repository 구현"""
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.league.entity import League
from src.domain.league.repository import LeagueRepository
from ..models import LeagueModel


class SQLAlchemyLeagueRepository(LeagueRepository):
    """SQLAlchemy를 사용한 League Repository 구현"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, league: League) -> League:
        """리그 저장"""
        league_model = LeagueModel(
            id=league.league_id,
            league_name=league.league_name,
            sport_type=league.sport_type,
            country=league.country,
            is_active=league.is_active,
            created_at=league.created_at
        )
        self.session.add(league_model)
        await self.session.flush()
        return league

    async def find_by_id(self, league_id: str) -> Optional[League]:
        """ID로 리그 조회"""
        query = select(LeagueModel).where(LeagueModel.id == league_id)
        result = await self.session.execute(query)
        league_model = result.scalar_one_or_none()

        if not league_model:
            return None

        return self._to_entity(league_model)

    async def find_all(
        self,
        sport_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[League], int]:
        """리그 목록 조회"""
        # 기본 쿼리
        query = select(LeagueModel)
        count_query = select(func.count(LeagueModel.id))

        # 필터 적용
        if sport_type is not None:
            query = query.where(LeagueModel.sport_type == sport_type)
            count_query = count_query.where(LeagueModel.sport_type == sport_type)

        if is_active is not None:
            query = query.where(LeagueModel.is_active == is_active)
            count_query = count_query.where(LeagueModel.is_active == is_active)

        # 전체 개수 조회
        total_result = await self.session.execute(count_query)
        total = total_result.scalar()

        # 페이지네이션 적용
        query = query.offset(skip).limit(limit)

        # 결과 조회
        result = await self.session.execute(query)
        league_models = result.scalars().all()

        leagues = [self._to_entity(model) for model in league_models]
        return leagues, total

    async def update(self, league: League) -> League:
        """리그 정보 업데이트"""
        query = select(LeagueModel).where(LeagueModel.id == league.league_id)
        result = await self.session.execute(query)
        league_model = result.scalar_one_or_none()

        if not league_model:
            raise ValueError(f"League not found: {league.league_id}")

        league_model.league_name = league.league_name
        league_model.sport_type = league.sport_type
        league_model.country = league.country
        league_model.is_active = league.is_active

        await self.session.flush()
        return league

    async def delete(self, league_id: str) -> bool:
        """리그 삭제"""
        query = select(LeagueModel).where(LeagueModel.id == league_id)
        result = await self.session.execute(query)
        league_model = result.scalar_one_or_none()

        if not league_model:
            return False

        await self.session.delete(league_model)
        await self.session.flush()
        return True

    @staticmethod
    def _to_entity(model: LeagueModel) -> League:
        """모델을 엔티티로 변환"""
        return League(
            league_id=model.id,
            league_name=model.league_name,
            sport_type=model.sport_type.value,
            country=model.country,
            is_active=model.is_active,
            created_at=model.created_at
        )
