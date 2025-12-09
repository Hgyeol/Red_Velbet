from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.domain.wallet.entity import Wallet


class WalletRepository(ABC):
    """
    Wallet 엔티티를 위한 추상 리포지토리 인터페이스
    """

    @abstractmethod
    async def get_by_id(self, wallet_id: UUID) -> Optional[Wallet]:
        """지갑 ID로 지갑을 조회합니다."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Wallet]:
        """사용자 ID로 지갑을 조회합니다."""
        pass

    @abstractmethod
    async def save(self, wallet: Wallet) -> None:
        """지갑 엔티티를 저장하거나 업데이트합니다."""
        pass

    @abstractmethod
    async def create(self, wallet: Wallet) -> None:
        """새로운 지갑 엔티티를 생성합니다."""
        pass

    @abstractmethod
    async def delete(self, wallet_id: UUID) -> None:
        """지갑 ID로 지갑을 삭제합니다."""
        pass