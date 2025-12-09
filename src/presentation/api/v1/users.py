"""사용자 API 엔드포인트"""
from fastapi import APIRouter, HTTPException, status

from src.application.user.dto import UpdateProfileDTO
from src.application.user.use_cases import (
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
)
from src.domain.common.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
)
from src.presentation.schemas.user import UserResponse, UpdateProfileRequest
from src.presentation.api.dependencies import UserRepository, CurrentUserId

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="내 프로필 조회",
    description="현재 로그인한 사용자의 프로필을 조회합니다"
)
async def get_my_profile(
    user_id: CurrentUserId,
    user_repository: UserRepository,
):
    """내 프로필 조회"""
    try:
        use_case = GetUserProfileUseCase(user_repository)
        user_dto = await use_case.execute(user_id)

        return UserResponse(**user_dto.__dict__)

    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="프로필 수정",
    description="현재 사용자의 프로필 정보를 수정합니다"
)
async def update_my_profile(
    request: UpdateProfileRequest,
    user_id: CurrentUserId,
    user_repository: UserRepository,
):
    """프로필 수정"""
    try:
        dto = UpdateProfileDTO(
            nickname=request.nickname,
            bank_name=request.bank_name,
            account_number=request.account_number,
            account_holder=request.account_holder,
        )

        use_case = UpdateUserProfileUseCase(user_repository)
        user_dto = await use_case.execute(user_id, dto)

        return UserResponse(**user_dto.__dict__)

    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DuplicateEntityException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
