"""League Use Cases"""
from typing import Optional

from src.domain.league.entity import League
from src.domain.league.repository import LeagueRepository
from .dto import LeagueDTO, CreateLeagueDTO, UpdateLeagueDTO, LeagueListDTO


class LeagueUseCases:
    """리그 관련 Use Cases"""

    def __init__(self, league_repository: LeagueRepository):
        self.league_repository = league_repository

    async def create_league(self, create_dto: CreateLeagueDTO) -> LeagueDTO:
        """리그 생성

        Args:
            create_dto: 리그 생성 정보

        Returns:
            LeagueDTO: 생성된 리그 정보

        Raises:
            ValueError: 유효하지 않은 스포츠 타입
        """
        # 스포츠 타입 검증
        valid_sport_types = ["축구", "야구", "농구", "배구"]
        if create_dto.sport_type not in valid_sport_types:
            raise ValueError(f"유효하지 않은 스포츠 타입입니다: {create_dto.sport_type}")

        # 리그 엔티티 생성
        league = League.create(
            league_name=create_dto.league_name,
            sport_type=create_dto.sport_type,
            country=create_dto.country,
            is_active=create_dto.is_active
        )

        # 저장
        saved_league = await self.league_repository.save(league)

        # DTO로 변환하여 반환
        return self._to_dto(saved_league)

    async def get_league_by_id(self, league_id: str) -> Optional[LeagueDTO]:
        """리그 ID로 조회

        Args:
            league_id: 리그 ID

        Returns:
            Optional[LeagueDTO]: 조회된 리그 정보 또는 None
        """
        league = await self.league_repository.find_by_id(league_id)
        if not league:
            return None
        return self._to_dto(league)

    async def get_leagues(
        self,
        sport_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        limit: int = 20
    ) -> LeagueListDTO:
        """리그 목록 조회

        Args:
            sport_type: 스포츠 종류 필터
            is_active: 활성화 여부 필터
            page: 페이지 번호 (1부터 시작)
            limit: 페이지당 항목 수

        Returns:
            LeagueListDTO: 리그 목록 및 페이지네이션 정보
        """
        skip = (page - 1) * limit
        leagues, total = await self.league_repository.find_all(
            sport_type=sport_type,
            is_active=is_active,
            skip=skip,
            limit=limit
        )

        league_dtos = [self._to_dto(league) for league in leagues]

        return LeagueListDTO(
            items=league_dtos,
            total=total,
            page=page,
            limit=limit
        )

    async def update_league(
        self,
        league_id: str,
        update_dto: UpdateLeagueDTO
    ) -> LeagueDTO:
        """리그 정보 업데이트

        Args:
            league_id: 리그 ID
            update_dto: 업데이트할 정보

        Returns:
            LeagueDTO: 업데이트된 리그 정보

        Raises:
            ValueError: 리그를 찾을 수 없음
        """
        # 기존 리그 조회
        league = await self.league_repository.find_by_id(league_id)
        if not league:
            raise ValueError(f"리그를 찾을 수 없습니다: {league_id}")

        # 업데이트할 필드만 변경
        if update_dto.league_name is not None:
            league.league_name = update_dto.league_name
        if update_dto.country is not None:
            league.country = update_dto.country
        if update_dto.is_active is not None:
            if update_dto.is_active:
                league.activate()
            else:
                league.deactivate()

        # 저장
        updated_league = await self.league_repository.update(league)

        return self._to_dto(updated_league)

    async def delete_league(self, league_id: str) -> bool:
        """리그 삭제

        Args:
            league_id: 리그 ID

        Returns:
            bool: 삭제 성공 여부
        """
        return await self.league_repository.delete(league_id)

    @staticmethod
    def _to_dto(league: League) -> LeagueDTO:
        """엔티티를 DTO로 변환"""
        return LeagueDTO(
            league_id=league.league_id,
            league_name=league.league_name,
            sport_type=league.sport_type,
            country=league.country,
            is_active=league.is_active,
            created_at=league.created_at
        )
