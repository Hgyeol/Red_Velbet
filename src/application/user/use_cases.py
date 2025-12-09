"""User 및 Auth Use Cases"""
from uuid import UUID
from typing import Optional

from src.domain.user.entity import User, UserRole
from src.domain.user.repository import UserRepository
from src.domain.common.exceptions import (
    DuplicateEntityException,
    AuthenticationException,
    EntityNotFoundException,
)
from src.domain.common.value_objects import Email, Username, Password
from src.infrastructure.auth.password_hasher import password_hasher
from src.infrastructure.auth.jwt_handler import jwt_handler
from src.infrastructure.auth.token_repository import token_repository
from .dto import (
    UserDTO,
    RegisterUserDTO,
    LoginDTO,
    AuthTokenDTO,
    ChangePasswordDTO,
    UpdateProfileDTO,
)


class RegisterUserUseCase:
    """회원가입 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto: RegisterUserDTO) -> UserDTO:
        """회원가입 실행"""
        # 유효성 검증
        Username(dto.username)
        Email(dto.email)
        Password(dto.password)

        # 중복 체크
        if await self.user_repository.exists_by_username(dto.username):
            raise DuplicateEntityException("이미 존재하는 사용자명입니다")

        if await self.user_repository.exists_by_email(dto.email):
            raise DuplicateEntityException("이미 존재하는 이메일입니다")

        # 비밀번호 해싱
        password_hash = password_hasher.hash(dto.password)

        # User 엔티티 생성
        user = User(
            username=dto.username,
            password_hash=password_hash,
            email=dto.email,
            nickname=dto.nickname,
            role=UserRole.USER,
        )

        # 저장
        saved_user = await self.user_repository.save(user)

        # DTO로 변환
        return UserDTO(
            user_id=saved_user.user_id,
            username=saved_user.username,
            email=saved_user.email,
            nickname=saved_user.nickname,
            role=saved_user.role.value,
            daily_limit=saved_user.daily_limit,
            today_total_bet=saved_user.today_total_bet,
            last_bet_date=saved_user.last_bet_date,
            created_at=saved_user.created_at,
            updated_at=saved_user.updated_at,
            is_active=saved_user.is_active,
            is_restricted=saved_user.is_restricted,
        )


class LoginUseCase:
    """로그인 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, dto: LoginDTO) -> tuple[AuthTokenDTO, UserDTO]:
        """로그인 실행"""
        # 사용자 조회
        user = await self.user_repository.find_by_username(dto.username)
        if not user:
            raise AuthenticationException("아이디 또는 비밀번호가 잘못되었습니다")

        # 비밀번호 검증
        if not password_hasher.verify(dto.password, user.password_hash):
            raise AuthenticationException("아이디 또는 비밀번호가 잘못되었습니다")

        # 계정 활성 상태 확인
        if not user.is_active:
            raise AuthenticationException("비활성화된 계정입니다")

        # Access Token 생성
        access_token = jwt_handler.create_access_token(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role.value,
        )

        # Refresh Token 생성 및 저장
        refresh_token = token_repository.generate_refresh_token()
        await token_repository.save_refresh_token(user.user_id, refresh_token)

        # 토큰 DTO
        auth_token = AuthTokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        # User DTO
        user_dto = UserDTO(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            nickname=user.nickname,
            role=user.role.value,
            daily_limit=user.daily_limit,
            today_total_bet=user.today_total_bet,
            last_bet_date=user.last_bet_date,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_restricted=user.is_restricted,
        )

        return auth_token, user_dto


class RefreshTokenUseCase:
    """토큰 갱신 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID, refresh_token: str) -> AuthTokenDTO:
        """토큰 갱신 실행"""
        # Refresh Token 검증
        is_valid = await token_repository.verify_refresh_token(user_id, refresh_token)
        if not is_valid:
            raise AuthenticationException("유효하지 않은 Refresh Token입니다")

        # 사용자 조회
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("사용자를 찾을 수 없습니다")

        # 새로운 Access Token 생성
        access_token = jwt_handler.create_access_token(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role.value,
        )

        # 새로운 Refresh Token 생성 및 저장 (선택사항)
        new_refresh_token = token_repository.generate_refresh_token()
        await token_repository.save_refresh_token(user.user_id, new_refresh_token)

        return AuthTokenDTO(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )


class LogoutUseCase:
    """로그아웃 Use Case"""

    async def execute(self, user_id: UUID, access_token: str) -> None:
        """로그아웃 실행"""
        # Refresh Token 삭제
        await token_repository.delete_refresh_token(user_id)

        # Access Token을 블랙리스트에 추가
        await token_repository.add_to_blacklist(access_token)


class ChangePasswordUseCase:
    """비밀번호 변경 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID, dto: ChangePasswordDTO) -> None:
        """비밀번호 변경 실행"""
        # 사용자 조회
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("사용자를 찾을 수 없습니다")

        # 현재 비밀번호 검증
        if not password_hasher.verify(dto.current_password, user.password_hash):
            raise AuthenticationException("현재 비밀번호가 일치하지 않습니다")

        # 새 비밀번호 유효성 검증
        Password(dto.new_password)

        # 새 비밀번호 해싱
        new_password_hash = password_hasher.hash(dto.new_password)

        # 비밀번호 변경
        user.update_password(new_password_hash)

        # 저장
        await self.user_repository.update(user)


class GetUserProfileUseCase:
    """사용자 프로필 조회 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID) -> UserDTO:
        """프로필 조회 실행"""
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("사용자를 찾을 수 없습니다")

        return UserDTO(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            nickname=user.nickname,
            role=user.role.value,
            daily_limit=user.daily_limit,
            today_total_bet=user.today_total_bet,
            last_bet_date=user.last_bet_date,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_restricted=user.is_restricted,
        )


class UpdateUserProfileUseCase:
    """사용자 프로필 수정 Use Case"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID, dto: UpdateProfileDTO) -> UserDTO:
        """프로필 수정 실행"""
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise EntityNotFoundException("사용자를 찾을 수 없습니다")

        # 이메일 변경 시 중복 체크
        if dto.email and dto.email != user.email:
            Email(dto.email)
            if await self.user_repository.exists_by_email(dto.email):
                raise DuplicateEntityException("이미 존재하는 이메일입니다")

        # 프로필 업데이트
        user.update_profile(nickname=dto.nickname, email=dto.email)

        # 저장
        updated_user = await self.user_repository.update(user)

        return UserDTO(
            user_id=updated_user.user_id,
            username=updated_user.username,
            email=updated_user.email,
            nickname=updated_user.nickname,
            role=updated_user.role.value,
            daily_limit=updated_user.daily_limit,
            today_total_bet=updated_user.today_total_bet,
            last_bet_date=updated_user.last_bet_date,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            is_active=updated_user.is_active,
            is_restricted=updated_user.is_restricted,
        )


class UserUseCases:
    """User Use Cases 통합 클래스"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.register_user = RegisterUserUseCase(user_repository)
        self.login = LoginUseCase(user_repository)
        self.refresh_token = RefreshTokenUseCase(user_repository)
        self.logout = LogoutUseCase()
        self.change_password = ChangePasswordUseCase(user_repository)
        self.get_user_profile = GetUserProfileUseCase(user_repository)
        self.update_user_profile = UpdateUserProfileUseCase(user_repository)
