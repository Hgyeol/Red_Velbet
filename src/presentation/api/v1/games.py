"""Game API 엔드포인트"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.game.use_cases import GameUseCases
from src.application.game.dto import CreateGameDTO, UpdateGameDTO, SetFinalScoreDTO
from src.presentation.schemas.game import (
    GameResponse,
    CreateGameRequest,
    UpdateGameRequest,
    SetFinalScoreRequest,
    GameListResponse,
    SettleGameRequest,
)
from src.presentation.api.dependencies import get_game_use_cases

router = APIRouter(prefix="/games", tags=["games"])


@router.post(
    "",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED,
    summary="게임 생성",
    description="새로운 게임을 생성합니다."
)
async def create_game(
    request: CreateGameRequest,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> GameResponse:
    """게임 생성"""
    try:
        create_dto = CreateGameDTO(**request.model_dump())
        game_dto = await use_cases.create_game(create_dto)
        return GameResponse.model_validate(game_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=GameListResponse,
    summary="게임 목록 조회",
    description="게임 목록을 조회합니다. 필터링 및 페이지네이션을 지원합니다."
)
async def get_games(
    league_id: Optional[str] = Query(None, description="리그 ID 필터"),
    status: Optional[str] = Query(None, description="경기 상태 필터"),
    is_live: Optional[bool] = Query(None, description="라이브 여부 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> GameListResponse:
    """게임 목록 조회"""
    game_list_dto = await use_cases.get_games(
        league_id=league_id,
        status=status,
        is_live=is_live,
        page=page,
        limit=limit
    )
    return GameListResponse(
        items=[GameResponse.model_validate(dto) for dto in game_list_dto.items],
        pagination=game_list_dto
    )


@router.get(
    "/{game_id}",
    response_model=GameResponse,
    summary="게임 상세 조회",
    description="특정 게임의 상세 정보를 조회합니다."
)
async def get_game(
    game_id: str,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> GameResponse:
    """게임 상세 조회"""
    game_dto = await use_cases.get_game_by_id(game_id)
    if not game_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"게임을 찾을 수 없습니다: {game_id}"
        )
    return GameResponse.model_validate(game_dto)


@router.patch(
    "/{game_id}",
    response_model=GameResponse,
    summary="게임 정보 수정",
    description="게임 정보를 수정합니다."
)
async def update_game(
    game_id: str,
    request: UpdateGameRequest,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> GameResponse:
    """게임 정보 수정"""
    try:
        update_dto = UpdateGameDTO(**request.model_dump(exclude_unset=True))
        game_dto = await use_cases.update_game(game_id, update_dto)
        return GameResponse.model_validate(game_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/{game_id}/score",
    response_model=GameResponse,
    summary="최종 스코어 설정",
    description="경기의 최종 스코어를 설정하고 상태를 '종료'로 변경합니다."
)
async def set_final_score(
    game_id: str,
    request: SetFinalScoreRequest,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> GameResponse:
    """최종 스코어 설정"""
    try:
        score_dto = SetFinalScoreDTO(**request.model_dump())
        game_dto = await use_cases.set_final_score(game_id, score_dto)
        return GameResponse.model_validate(game_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{game_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게임 삭제",
    description="게임을 삭제합니다."
)
async def delete_game(
    game_id: str,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> None:
    """게임 삭제"""
    success = await use_cases.delete_game(game_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"게임을 찾을 수 없습니다: {game_id}"
        )


@router.post(
    "/{game_id}/settle",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게임 정산",
    description="게임 결과를 정산하고 배팅을 처리합니다."
)
async def settle_game(
    game_id: str,
    request: SettleGameRequest,
    use_cases: GameUseCases = Depends(get_game_use_cases)
) -> None:
    """게임 정산"""
    try:
        request_dto = SettleGameRequestDTO(**request.model_dump())
        await use_cases.settle_game(game_id, request_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
