"""BettingOption API 엔드포인트"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.betting.use_cases import BettingOptionUseCases
from src.application.betting.dto import CreateBettingOptionDTO, UpdateBettingOptionDTO
from src.presentation.schemas.betting import (
    BettingOptionResponse,
    CreateBettingOptionRequest,
    UpdateBettingOptionRequest,
)
from src.presentation.api.dependencies import get_betting_option_use_cases # This will be created later

router = APIRouter(prefix="/betting-options", tags=["betting-options"])


@router.post(
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
    """배팅 옵션 생성"""
    try:
        create_dto = CreateBettingOptionDTO(**request.model_dump())
        option_dto = await use_cases.create_option(create_dto)
        return BettingOptionResponse.model_validate(option_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/game/{game_id}",
    response_model=List[BettingOptionResponse],
    summary="게임별 배팅 옵션 목록 조회",
    description="특정 게임에 대한 모든 배팅 옵션을 조회합니다."
)
async def get_options_for_game(
    game_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> List[BettingOptionResponse]:
    """게임별 배팅 옵션 목록 조회"""
    options = await use_cases.get_options_for_game(game_id)
    return [BettingOptionResponse.model_validate(opt) for opt in options]


@router.get(
    "/{option_id}",
    response_model=BettingOptionResponse,
    summary="배팅 옵션 상세 조회",
    description="특정 배팅 옵션의 상세 정보를 조회합니다."
)
async def get_betting_option(
    option_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> BettingOptionResponse:
    """배팅 옵션 상세 조회"""
    option_dto = await use_cases.get_option_by_id(option_id)
    if not option_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"배팅 옵션을 찾을 수 없습니다: {option_id}"
        )
    return BettingOptionResponse.model_validate(option_dto)


@router.patch(
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
    """배팅 옵션 수정"""
    try:
        update_dto = UpdateBettingOptionDTO(**request.model_dump(exclude_unset=True))
        option_dto = await use_cases.update_option(option_id, update_dto)
        return BettingOptionResponse.model_validate(option_dto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="배팅 옵션 삭제",
    description="배팅 옵션을 삭제합니다."
)
async def delete_betting_option(
    option_id: str,
    use_cases: BettingOptionUseCases = Depends(get_betting_option_use_cases)
) -> None:
    """배팅 옵션 삭제"""
    success = await use_cases.delete_option(option_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"배팅 옵션을 찾을 수 없습니다: {option_id}"
        )
