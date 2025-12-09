"""인증 API 엔드포인트"""
from fastapi import APIRouter, HTTPException, status

from src.application.user.dto import (
    RegisterUserDTO,
    LoginDTO,
    ChangePasswordDTO,
)
from src.application.user.use_cases import (
    RegisterUserUseCase,
    LoginUseCase,
    RefreshTokenUseCase,
    LogoutUseCase,
    ChangePasswordUseCase,
)
from src.domain.common.exceptions import (
    DuplicateEntityException,
    AuthenticationException,
    ValidationException,
)
from src.presentation.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    TokenResponse,
    LoginResponse,
    MessageResponse,
)
from src.presentation.schemas.user import UserResponse
from src.presentation.api.dependencies import UserRepository, CurrentUserId, CurrentToken

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="새로운 사용자 계정을 생성합니다"
)
async def register(
    request: RegisterRequest,
    user_repository: UserRepository,
):
    """회원가입"""
    try:
        dto = RegisterUserDTO(
            username=request.username,
            password=request.password,
            email=request.email,
            nickname=request.nickname,
        )

        use_case = RegisterUserUseCase(user_repository)
        user_dto = await use_case.execute(dto)

        return UserResponse(**user_dto.__dict__)

    except DuplicateEntityException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="로그인",
    description="사용자 인증 후 토큰을 발급받습니다"
)
async def login(
    request: LoginRequest,
    user_repository: UserRepository,
):
    """로그인"""
    try:
        dto = LoginDTO(
            username=request.username,
            password=request.password,
        )

        use_case = LoginUseCase(user_repository)
        auth_token, user_dto = await use_case.execute(dto)

        return LoginResponse(
            access_token=auth_token.access_token,
            refresh_token=auth_token.refresh_token,
            token_type=auth_token.token_type,
            expires_in=auth_token.expires_in,
            user={
                "user_id": str(user_dto.user_id),
                "username": user_dto.username,
                "email": user_dto.email,
                "nickname": user_dto.nickname,
                "role": user_dto.role,
            },
        )

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="토큰 갱신",
    description="만료된 Access Token을 Refresh Token으로 갱신합니다"
)
async def refresh_token(
    request: RefreshTokenRequest,
    user_id: CurrentUserId,
    user_repository: UserRepository,
):
    """토큰 갱신"""
    try:
        use_case = RefreshTokenUseCase(user_repository)
        auth_token = await use_case.execute(user_id, request.refresh_token)

        return TokenResponse(
            access_token=auth_token.access_token,
            refresh_token=auth_token.refresh_token,
            token_type=auth_token.token_type,
            expires_in=auth_token.expires_in,
        )

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="로그아웃",
    description="현재 세션을 종료합니다"
)
async def logout(
    user_id: CurrentUserId,
    access_token: CurrentToken,
):
    """로그아웃"""
    use_case = LogoutUseCase()
    await use_case.execute(user_id, access_token)

    return MessageResponse(message="로그아웃되었습니다")


@router.put(
    "/password",
    response_model=MessageResponse,
    summary="비밀번호 변경",
    description="현재 사용자의 비밀번호를 변경합니다"
)
async def change_password(
    request: ChangePasswordRequest,
    user_id: CurrentUserId,
    user_repository: UserRepository,
):
    """비밀번호 변경"""
    try:
        dto = ChangePasswordDTO(
            current_password=request.current_password,
            new_password=request.new_password,
        )

        use_case = ChangePasswordUseCase(user_repository)
        await use_case.execute(user_id, dto)

        return MessageResponse(message="비밀번호가 변경되었습니다")

    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
