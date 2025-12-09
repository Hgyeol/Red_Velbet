"""League API 엔드포인트"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.application.league.use_cases import LeagueUseCases
from src.application.league.dto import CreateLeagueDTO, UpdateLeagueDTO
from src.presentation.schemas.league import (
    LeagueResponse,
    CreateLeagueRequest,
    UpdateLeagueRequest,
    LeagueListResponse,
    PaginationInfo
)
from src.presentation.api.dependencies import get_league_use_cases

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.post(
    "",
    response_model=LeagueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="리그 생성",
    description="새로운 리그를 생성합니다."
)
async def create_league(
    request: CreateLeagueRequest,
    use_cases: LeagueUseCases = Depends(get_league_use_cases)
) -> LeagueResponse:
    """리그 생성"""
    try:
        create_dto = CreateLeagueDTO(
            league_name=request.league_name,
            sport_type=request.sport_type,
            country=request.country,
            is_active=request.is_active
        )
        league_dto = await use_cases.create_league(create_dto)
        return LeagueResponse(**league_dto.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "",
    response_model=LeagueListResponse,
    summary="리그 목록 조회",
    description="리그 목록을 조회합니다. 필터링 및 페이지네이션을 지원합니다."
)
async def get_leagues(
    sport_type: Optional[str] = Query(None, description="스포츠 종류 필터"),
    is_active: Optional[bool] = Query(None, description="활성화 여부 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    use_cases: LeagueUseCases = Depends(get_league_use_cases)
) -> LeagueListResponse:
    """리그 목록 조회"""
    league_list_dto = await use_cases.get_leagues(
        sport_type=sport_type,
        is_active=is_active,
        page=page,
        limit=limit
    )

    return LeagueListResponse(
        items=[LeagueResponse(**dto.__dict__) for dto in league_list_dto.items],
        pagination=PaginationInfo(
            page=league_list_dto.page,
            limit=league_list_dto.limit,
            total=league_list_dto.total,
            total_pages=league_list_dto.total_pages
        )
    )


@router.get(
    "/{league_id}",
    response_model=LeagueResponse,
    summary="리그 상세 조회",
    description="특정 리그의 상세 정보를 조회합니다."
)
async def get_league(
    league_id: str,
    use_cases: LeagueUseCases = Depends(get_league_use_cases)
) -> LeagueResponse:
    """리그 상세 조회"""
    league_dto = await use_cases.get_league_by_id(league_id)
    if not league_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"리그를 찾을 수 없습니다: {league_id}"
        )
    return LeagueResponse(**league_dto.__dict__)


@router.patch(
    "/{league_id}",
    response_model=LeagueResponse,
    summary="리그 정보 수정",
    description="리그 정보를 수정합니다."
)
async def update_league(
    league_id: str,
    request: UpdateLeagueRequest,
    use_cases: LeagueUseCases = Depends(get_league_use_cases)
) -> LeagueResponse:
    """리그 정보 수정"""
    try:
        update_dto = UpdateLeagueDTO(
            league_name=request.league_name,
            country=request.country,
            is_active=request.is_active
        )
        league_dto = await use_cases.update_league(league_id, update_dto)
        return LeagueResponse(**league_dto.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{league_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="리그 삭제",
    description="리그를 삭제합니다."
)
async def delete_league(
    league_id: str,
    use_cases: LeagueUseCases = Depends(get_league_use_cases)
) -> None:
    """리그 삭제"""
    success = await use_cases.delete_league(league_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"리그를 찾을 수 없습니다: {league_id}"
        )
