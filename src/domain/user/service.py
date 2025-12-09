from src.domain.user.repository import UserRepository
from src.domain.user.entity import User
from src.domain.common.value_objects import Password
from uuid import UUID


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        # 여기에 사용자 생성 로직을 추가
        # 예: 비밀번호 해싱, 유효성 검사 등
        # user.password = Password(some_hashing_function(user.password.value))
        return await self.user_repository.create(user)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_by_username(username)

    # 추가 서비스 메서드를 여기에 정의
    # 예: update_user, delete_user 등
