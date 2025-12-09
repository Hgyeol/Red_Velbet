from uuid import UUID
from typing import Optional

from src.domain.wallet.entity import Wallet
from src.domain.wallet.repository import WalletRepository
from src.domain.common.value_objects import Money
from src.domain.common.exceptions import ResourceNotFoundException, DomainException


class WalletService:
    """
    지갑 도메인 서비스를 정의합니다.
    주요 비즈니스 로직을 처리합니다.
    """

    def __init__(self, wallet_repository: WalletRepository):
        self.wallet_repository = wallet_repository

    async def get_wallet_by_user_id(self, user_id: UUID) -> Wallet:
        """
        사용자 ID로 지갑을 조회합니다.
        """
        wallet = await self.wallet_repository.get_by_user_id(user_id)
        if not wallet:
            raise ResourceNotFoundException(f"User with ID {user_id} does not have a wallet.")
        return wallet

    async def deposit_to_wallet(self, user_id: UUID, amount: Money) -> Wallet:
        """
        사용자 지갑에 금액을 입금합니다.
        """
        wallet = await self.get_wallet_by_user_id(user_id)
        try:
            wallet.deposit(amount)
            await self.wallet_repository.save(wallet)
            return wallet
        except ValueError as e:
            raise DomainException(str(e))

    async def withdraw_from_wallet(self, user_id: UUID, amount: Money) -> Wallet:
        """
        사용자 지갑에서 금액을 출금합니다.
        """
        wallet = await self.get_wallet_by_user_id(user_id)
        try:
            wallet.withdraw(amount)
            await self.wallet_repository.save(wallet)
            return wallet
        except ValueError as e:
            raise DomainException(str(e))

    async def create_initial_wallet(self, user_id: UUID) -> Wallet:
        """
        새로운 사용자를 위한 초기 지갑을 생성합니다.
        """
        existing_wallet = await self.wallet_repository.get_by_user_id(user_id)
        if existing_wallet:
            raise DomainException(f"Wallet already exists for user ID {user_id}")

        wallet = Wallet(user_id=user_id, balance=Money(Decimal('0.00')))
        await self.wallet_repository.create(wallet)
        return wallet
