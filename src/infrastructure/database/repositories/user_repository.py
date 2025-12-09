"""User Repository 구현"""
from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.entity import User, UserRole
from src.domain.user.repository import UserRepository as UserRepositoryInterface
from src.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepositoryInterface):
    """User Repository 구현 클래스"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """SQLAlchemy 모델을 도메인 엔티티로 변환"""
        return User(
            user_id=UUID(model.id),
            username=model.username,
            password_hash=model.password_hash,
            email=model.email,
            nickname=model.nickname,
            role=UserRole(model.role.value),
            daily_limit=model.daily_limit,
            today_total_bet=model.today_total_bet,
            last_bet_date=model.last_bet_date,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
            is_restricted=model.is_restricted,
        )

    def _to_model(self, entity: User) -> UserModel:
        """도메인 엔티티를 SQLAlchemy 모델로 변환"""
        return UserModel(
            id=str(entity.user_id),
            username=entity.username,
            password_hash=entity.password_hash,
            email=entity.email,
            nickname=entity.nickname,
            role=entity.role.value,
            daily_limit=entity.daily_limit,
            today_total_bet=entity.today_total_bet,
            last_bet_date=entity.last_bet_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active,
            is_restricted=entity.is_restricted,
        )

    async def save(self, user: User) -> User:
        """사용자 저장"""
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """ID로 사용자 조회"""
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def exists_by_username(self, username: str) -> bool:
        """사용자명 존재 여부 확인"""
        stmt = select(UserModel.id).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def exists_by_email(self, email: str) -> bool:
        """이메일 존재 여부 확인"""
        stmt = select(UserModel.id).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def update(self, user: User) -> User:
        """사용자 정보 업데이트"""
        stmt = select(UserModel).where(UserModel.id == str(user.user_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"User with id {user.user_id} not found")

        # 모델 필드 업데이트
        model.username = user.username
        model.password_hash = user.password_hash
        model.email = user.email
        model.nickname = user.nickname
        model.role = user.role.value
        model.daily_limit = user.daily_limit
        model.today_total_bet = user.today_total_bet
        model.last_bet_date = user.last_bet_date
        model.updated_at = user.updated_at
        model.is_active = user.is_active
        model.is_restricted = user.is_restricted

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: UUID) -> None:
        """사용자 삭제"""
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.flush()
