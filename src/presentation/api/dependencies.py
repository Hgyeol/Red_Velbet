"""FastAPI 의존성 주입"""
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.user_repository import UserRepositoryImpl
from src.infrastructure.database.repositories.wallet_repository import WalletRepositoryImpl
from src.infrastructure.database.repositories.league_repository import LeagueRepositoryImpl
from src.infrastructure.database.repositories.game_repository import GameRepositoryImpl
from src.infrastructure.database.repositories.betting_repository import (
    BettingOptionRepositoryImpl,
    BetRepositoryImpl,
    BetSlipRepositoryImpl,
)
from src.infrastructure.auth.jwt_handler import jwt_handler
from src.infrastructure.auth.token_repository import token_repository
from src.domain.common.exceptions import AuthenticationException, EntityNotFoundException
from src.domain.user.service import UserService
from src.domain.wallet.service import WalletService
from src.domain.betting.service import BettingService
from src.domain.game.service import GameService
from src.application.user.use_cases import UserUseCases as UserUseCasesClass
from src.application.wallet.use_cases import WalletUseCases as WalletUseCasesClass
from src.application.league.use_cases import LeagueUseCases as LeagueUseCasesClass
from src.application.game.use_cases import GameUseCases as GameUseCasesClass
from src.application.betting.use_cases import (
    BettingOptionUseCases as BettingOptionUseCasesClass,
    BettingUseCases as BettingUseCasesClass,
)
from src.presentation.schemas.user import UserResponse


# HTTP Bearer 토큰 스키마
security = HTTPBearer()


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepositoryImpl:
    """User Repository 의존성"""
    return UserRepositoryImpl(session)


async def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> WalletRepositoryImpl:
    """Wallet Repository 의존성"""
    return WalletRepositoryImpl(session)


async def get_league_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> LeagueRepositoryImpl:
    """League Repository 의존성"""
    return LeagueRepositoryImpl(session)


async def get_game_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> GameRepositoryImpl:
    """Game Repository 의존성"""
    return GameRepositoryImpl(session)


async def get_betting_option_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> BettingOptionRepositoryImpl:
    """BettingOption Repository 의존성"""
    return BettingOptionRepositoryImpl(session)


async def get_bet_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> BetRepositoryImpl:
    """Bet Repository 의존성"""
    return BetRepositoryImpl(session)


async def get_bet_slip_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> BetSlipRepositoryImpl:
    """BetSlip Repository 의존성"""
    return BetSlipRepositoryImpl(session)


async def get_user_service(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> UserService:
    """User Service 의존성"""
    return UserService(user_repository)


async def get_wallet_service(
    wallet_repository: Annotated[WalletRepositoryImpl, Depends(get_wallet_repository)]
) -> WalletService:
    """Wallet Service 의존성"""
    return WalletService(wallet_repository)


async def get_betting_service(
    bet_repository: Annotated[BetRepositoryImpl, Depends(get_bet_repository)],
    bet_slip_repository: Annotated[BetSlipRepositoryImpl, Depends(get_bet_slip_repository)],
    betting_option_repository: Annotated[BettingOptionRepositoryImpl, Depends(get_betting_option_repository)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
) -> BettingService:
    """Betting Service 의존성"""
    return BettingService(
        bet_repository,
        bet_slip_repository,
        betting_option_repository,
        wallet_service,
    )


async def get_game_service(
    game_repository: Annotated[GameRepositoryImpl, Depends(get_game_repository)],
    bet_repository: Annotated[BetRepositoryImpl, Depends(get_bet_repository)],
    bet_slip_repository: Annotated[BetSlipRepositoryImpl, Depends(get_bet_slip_repository)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
) -> GameService:
    """Game Service 의존성"""
    return GameService(
        game_repository,
        bet_repository,
        bet_slip_repository,
        wallet_service,
    )


async def get_user_use_cases(
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)]
) -> UserUseCasesClass:
    """User Use Cases 의존성"""
    return UserUseCasesClass(user_repository)


async def get_wallet_use_cases(
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)]
) -> WalletUseCasesClass:
    """Wallet Use Cases 의존성"""
    return WalletUseCasesClass(wallet_service)


async def get_league_use_cases(
    league_repository: Annotated[LeagueRepositoryImpl, Depends(get_league_repository)]
) -> LeagueUseCasesClass:
    """League Use Cases 의존성"""
    return LeagueUseCasesClass(league_repository)


async def get_game_use_cases(
    game_repository: Annotated[GameRepositoryImpl, Depends(get_game_repository)],
    game_service: Annotated[GameService, Depends(get_game_service)],
) -> GameUseCasesClass:
    """Game Use Cases 의존성"""
    return GameUseCasesClass(game_repository, game_service)


async def get_betting_option_use_cases(
    betting_option_repository: Annotated[BettingOptionRepositoryImpl, Depends(get_betting_option_repository)]
) -> BettingOptionUseCasesClass:
    """BettingOption Use Cases 의존성"""
    return BettingOptionUseCasesClass(betting_option_repository)


async def get_betting_use_cases(
    betting_service: Annotated[BettingService, Depends(get_betting_service)],
    bet_repository: Annotated[BetRepositoryImpl, Depends(get_bet_repository)],
) -> BettingUseCasesClass:
    """Betting Use Cases 의존성"""
    return BettingUseCasesClass(betting_service, bet_repository)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> UUID:
    """현재 로그인한 사용자 ID 추출"""
    try:
        token = credentials.credentials
        if await token_repository.is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 무효화되었습니다",
            )
        user_id = jwt_handler.get_user_id_from_token(token)
        return user_id
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 정보입니다",
        )


async def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    user_use_cases: Annotated[UserUseCasesClass, Depends(get_user_use_cases)]
) -> UserResponse:
    """현재 로그인한 사용자 정보 추출"""
    try:
        user_dto = await user_use_cases.get_user_profile(user_id)
        return UserResponse.model_validate(user_dto)
    except EntityNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="사용자 정보를 가져오는 중 오류가 발생했습니다.",
        )


async def get_current_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """현재 Access Token 추출"""
    return credentials.credentials


# 타입 별칭
CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]
CurrentToken = Annotated[str, Depends(get_current_token)]
CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
UserRepository = Annotated[UserRepositoryImpl, Depends(get_user_repository)]
WalletRepository = Annotated[WalletRepositoryImpl, Depends(get_wallet_repository)]
LeagueRepository = Annotated[LeagueRepositoryImpl, Depends(get_league_repository)]
GameRepository = Annotated[GameRepositoryImpl, Depends(get_game_repository)]
BettingOptionRepository = Annotated[BettingOptionRepositoryImpl, Depends(get_betting_option_repository)]
BetRepository = Annotated[BetRepositoryImpl, Depends(get_bet_repository)]
BetSlipRepository = Annotated[BetSlipRepositoryImpl, Depends(get_bet_slip_repository)]
UserUseCases = Annotated[UserUseCasesClass, Depends(get_user_use_cases)]
WalletUseCases = Annotated[WalletUseCasesClass, Depends(get_wallet_use_cases)]
LeagueUseCases = Annotated[LeagueUseCasesClass, Depends(get_league_use_cases)]
GameUseCases = Annotated[GameUseCasesClass, Depends(get_game_use_cases)]
BettingOptionUseCases = Annotated[BettingOptionUseCasesClass, Depends(get_betting_option_use_cases)]
BettingUseCases = Annotated[BettingUseCasesClass, Depends(get_betting_use_cases)]
GameService = Annotated[GameService, Depends(get_game_service)]
