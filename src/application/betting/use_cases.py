"""BettingOption Use Cases"""
from typing import List, Optional

from src.domain.betting.entity import BettingOption
from src.domain.betting.repository import BettingOptionRepository
from .dto import (
    BettingOptionDTO,
    CreateBettingOptionDTO,
    UpdateBettingOptionDTO,
)


class BettingOptionUseCases:
    """배팅 옵션 관련 Use Cases"""

    def __init__(self, betting_option_repository: BettingOptionRepository):
        self.betting_option_repository = betting_option_repository

    async def create_option(self, create_dto: CreateBettingOptionDTO) -> BettingOptionDTO:
        """배팅 옵션 생성"""
        new_option = BettingOption(
            game_id=create_dto.game_id,
            option_type=create_dto.option_type,
            option_name=create_dto.option_name,
            odds=create_dto.odds,
            handicap_value=create_dto.handicap_value,
            over_under_line=create_dto.over_under_line,
        )
        await self.betting_option_repository.save(new_option)
        return self._to_dto(new_option)

    async def get_option_by_id(self, option_id: str) -> Optional[BettingOptionDTO]:
        """ID로 배팅 옵션 조회"""
        option = await self.betting_option_repository.find_by_id(option_id)
        return self._to_dto(option) if option else None

    async def get_options_for_game(self, game_id: str) -> List[BettingOptionDTO]:
        """특정 게임의 모든 배팅 옵션 조회"""
        options = await self.betting_option_repository.find_by_game_id(game_id)
        return [self._to_dto(option) for option in options]

    async def update_option(self, option_id: str, update_dto: UpdateBettingOptionDTO) -> BettingOptionDTO:
        """배팅 옵션 수정"""
        option = await self.betting_option_repository.find_by_id(option_id)
        if not option:
            raise ValueError("배팅 옵션을 찾을 수 없습니다.")

        if update_dto.odds is not None:
            option.update_odds(update_dto.odds)
        if update_dto.is_active is not None and not update_dto.is_active:
            option.deactivate()

        await self.betting_option_repository.save(option)
        return self._to_dto(option)

    async def delete_option(self, option_id: str) -> bool:
        """배팅 옵션 삭제"""
        return await self.betting_option_repository.delete(option_id)

    def _to_dto(self, option: BettingOption) -> BettingOptionDTO:
        """BettingOption 엔티티를 BettingOptionDTO로 변환"""
        return BettingOptionDTO(
            option_id=option.id,
            game_id=option.game_id,
            option_type=option.option_type.value,
            option_name=option.option_name,
            odds=option.odds,
            is_active=option.is_active,
            handicap_value=option.handicap_value,
            over_under_line=option.over_under_line,
        )
