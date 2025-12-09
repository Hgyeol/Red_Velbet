"""BettingOption and Bet API 엔드포인트"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.betting.use_cases import BettingOptionUseCases, BettingUseCases
from src.application.betting.dto import CreateBettingOptionDTO, UpdateBettingOptionDTO, PlaceBetRequestDTO
from src.presentation.schemas.betting import (
    BettingOptionResponse,
    CreateBettingOptionRequest,
    UpdateBettingOptionRequest,
    PlaceBetRequest,
    BetResponse,
)
from src.presentation.api.dependencies import (
    get_betting_option_use_cases,
    get_betting_use_cases,
    CurrentUserId,
)

# betting-options router
options_router = APIRouter(prefix="/betting-options", tags=["betting-options"])

@options_router.post(
    "",
    response_model=BettingOptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="배팅 옵션 생성",
    description="새로운 배팅 옵션을 생성합니다."
)
async def create_betting_option(
    request: CreateBettingOptionRequest,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> BettingOptionResponse:
    try:
        create_dto = CreateBettingOptionDTO(**request.model_dump())
        option_dto = await use_cases.create_option(create_dto)
        return BettingOptionResponse.model_validate(option_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@options_router.get(
    "/game/{game_id}",
    response_model=List[BettingOptionResponse],
    summary="게임별 배팅 옵션 목록 조회",
    description="특정 게임에 대한 모든 배팅 옵션을 조회합니다."
)
async def get_options_for_game(
    game_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> List[BettingOptionResponse]:
    options = await use_cases.get_options_for_game(game_id)
    return [BettingOptionResponse.model_validate(opt) for opt in options]

@options_router.get(
    "/{option_id}",
    response_model=BettingOptionResponse,
    summary="배팅 옵션 상세 조회",
    description="특정 배팅 옵션의 상세 정보를 조회합니다."
)
async def get_betting_option(
    option_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> BettingOptionResponse:
    option_dto = await use_cases.get_option_by_id(option_id)
    if not option_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"배팅 옵션을 찾을 수 없습니다: {option_id}"
        )
    return BettingOptionResponse.model_validate(option_dto)

@options_router.patch(
    "/{option_id}",
    response_model=BettingOptionResponse,
    summary="배팅 옵션 수정",
    description="배팅 옵션의 배당률 또는 활성화 상태를 수정합니다."
)
async def update_betting_option(
    option_id: str,
    request: UpdateBettingOptionRequest,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> BettingOptionResponse:
    try:
        update_dto = UpdateBettingOptionDTO(**request.model_dump(exclude_unset=True))
        option_dto = await use_cases.update_option(option_id, update_dto)
        return BettingOptionResponse.model_validate(option_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@options_router.delete(
    "/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="배팅 옵션 삭제",
    description="배팅 옵션을 삭제합니다."
)
async def delete_betting_option(
    option_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> None:
    success = await use_cases.delete_option(option_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"배팅 옵션을 찾을 수 없습니다: {option_id}"
        )

# bets router
bets_router = APIRouter(prefix="/bets", tags=["bets"])

@bets_router.post(
    "",
    response_model=BetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="배팅하기",
    description="선택한 옵션으로 배팅을 합니다."
)
async def place_bet(
    user_id: CurrentUserId,
    request: PlaceBetRequest,
    use_cases: BettingUseCases = Depends(get_betting_use_cases)
) -> BetResponse:
    try:
        request_dto = PlaceBetRequestDTO(**request.model_dump())
        bet_dto = await use_cases.place_bet(str(user_id), request_dto)
        return BetResponse.model_validate(bet_dto)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@bets_router.get(
    "/my-bets",
    response_model=List[BetResponse],
    summary="내 배팅 내역 조회",
    description="현재 로그인한 사용자의 모든 배팅 내역을 조회합니다."
)
async def get_my_bets(
    user_id: CurrentUserId,
    use_cases: BettingUseCases = Depends(get_betting_use_cases)
) -> List[BetResponse]:
    bets = await use_cases.get_my_bets(str(user_id))
    return [BetResponse.model_validate(bet) for bet in bets]
