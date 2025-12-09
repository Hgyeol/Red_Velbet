"""FastAPI 의존성 주입"""
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import get_db
from src.infrastructure.database.repositories.user_repository import UserRepositoryImpl
from src.infrastructure.auth.jwt_handler import jwt_handler
from src.infrastructure.auth.token_repository import token_repository
from src.domain.common.exceptions import AuthenticationException

# HTTP Bearer 토큰 스키마
security = HTTPBearer()


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> UserRepositoryImpl:
    """User Repository 의존성"""
    return UserRepositoryImpl(session)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> UUID:
    """현재 로그인한 사용자 ID 추출"""
    try:
        token = credentials.credentials

        # 블랙리스트 확인
        if await token_repository.is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 무효화되었습니다",
            )

        # 토큰 검증 및 사용자 ID 추출
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


async def get_current_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> str:
    """현재 Access Token 추출"""
    return credentials.credentials


# 타입 별칭
CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]
CurrentToken = Annotated[str, Depends(get_current_token)]
UserRepository = Annotated[UserRepositoryImpl, Depends(get_user_repository)]
