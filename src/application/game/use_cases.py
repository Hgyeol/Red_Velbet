"""Game Use Cases"""
import math
from typing import Optional

from src.domain.game.entity import Game
from src.domain.game.repository import GameRepository
from .dto import (
    GameDTO,
    CreateGameDTO,
    UpdateGameDTO,
    SetFinalScoreDTO,
    GameListDTO,
)


class GameUseCases:
    """게임 관련 Use Cases"""

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    async def create_game(self, create_dto: CreateGameDTO) -> GameDTO:
        """게임 생성"""
        new_game = Game(
            league_id=create_dto.league_id,
            home_team=create_dto.home_team,
            away_team=create_dto.away_team,
            start_time=create_dto.start_time,
            betting_deadline=create_dto.betting_deadline,
            sport_type=create_dto.sport_type,
        )
        await self.game_repository.save(new_game)
        return self._to_dto(new_game)

    async def get_game_by_id(self, game_id: str) -> Optional[GameDTO]:
        """ID로 게임 조회"""
        game = await self.game_repository.find_by_id(game_id)
        return self._to_dto(game) if game else None

    async def get_games(
        self,
        league_id: Optional[str] = None,
        status: Optional[str] = None,
        is_live: Optional[bool] = None,
        page: int = 1,
        limit: int = 20
    ) -> GameListDTO:
        """게임 목록 조회"""
        games = await self.game_repository.find_all(
            league_id=league_id,
            status=status,
            is_live=is_live,
            page=page,
            limit=limit,
        )
        total = await self.game_repository.count_all(
            league_id=league_id,
            status=status,
            is_live=is_live,
        )
        
        return GameListDTO(
            items=[self._to_dto(game) for game in games],
            total=total,
            page=page,
            limit=limit,
            total_pages=math.ceil(total / limit)
        )

    async def update_game(self, game_id: str, update_dto: UpdateGameDTO) -> GameDTO:
        """게임 정보 수정"""
        game = await self.game_repository.find_by_id(game_id)
        if not game:
            raise ValueError("게임을 찾을 수 없습니다.")

        if update_dto.home_team is not None:
            game.home_team = update_dto.home_team
        if update_dto.away_team is not None:
            game.away_team = update_dto.away_team
        if update_dto.start_time is not None:
            game.start_time = update_dto.start_time
        if update_dto.betting_deadline is not None:
            game.betting_deadline = update_dto.betting_deadline
        if update_dto.status is not None:
            game.change_status(update_dto.status)
        if update_dto.is_live is not None and update_dto.is_live:
            game.to_live()
        
        await self.game_repository.save(game)
        return self._to_dto(game)

    async def set_final_score(self, game_id: str, score_dto: SetFinalScoreDTO) -> GameDTO:
        """최종 스코어 설정"""
        game = await self.game_repository.find_by_id(game_id)
        if not game:
            raise ValueError("게임을 찾을 수 없습니다.")
        
        game.set_final_score(score_dto.home_score, score_dto.away_score)
        await self.game_repository.save(game)
        return self._to_dto(game)

    async def delete_game(self, game_id: str) -> bool:
        """게임 삭제"""
        return await self.game_repository.delete(game_id)

    def _to_dto(self, game: Game) -> GameDTO:
        """Game 엔티티를 GameDTO로 변환"""
        return GameDTO(
            game_id=game.id,
            league_id=game.league_id,
            home_team=game.home_team,
            away_team=game.away_team,
            start_time=game.start_time,
            betting_deadline=game.betting_deadline,
            sport_type=game.sport_type.value,
            status=game.status.value,
            is_live=game.is_live,
            final_score_home=game.final_score_home,
            final_score_away=game.final_score_away,
            created_at=game.created_at,
            updated_at=game.updated_at,
        )
