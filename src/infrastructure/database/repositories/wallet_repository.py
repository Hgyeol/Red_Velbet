from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.wallet.entity import Wallet
from src.domain.wallet.repository import WalletRepository
from src.domain.common.value_objects import Money
from src.infrastructure.database.models import WalletModel


class WalletRepositoryImpl(WalletRepository):
    """
    WalletRepository 인터페이스의 SQLAlchemy 구현체
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, wallet_id: UUID) -> Optional[Wallet]:
        stmt = select(WalletModel).where(WalletModel.id == str(wallet_id))
        result = await self.session.execute(stmt)
        wallet_model = result.scalars().first()
        if wallet_model:
            return self._to_entity(wallet_model)
        return None

    async def get_by_user_id(self, user_id: UUID) -> Optional[Wallet]:
        stmt = select(WalletModel).where(WalletModel.user_id == str(user_id))
        result = await self.session.execute(stmt)
        wallet_model = result.scalars().first()
        if wallet_model:
            return self._to_entity(wallet_model)
        return None

    async def save(self, wallet: Wallet) -> None:
        wallet_model = await self.session.get(WalletModel, str(wallet.id))
        if wallet_model:
            wallet_model.balance = wallet.balance.amount
            wallet_model.updated_at = wallet.updated_at
        else:
            wallet_model = WalletModel(
                id=str(wallet.id),
                user_id=str(wallet.user_id),
                balance=wallet.balance.amount,
                updated_at=wallet.updated_at
            )
            self.session.add(wallet_model)
        await self.session.flush()

    async def create(self, wallet: Wallet) -> None:
        wallet_model = WalletModel(
            id=str(wallet.id),
            user_id=str(wallet.user_id),
            balance=wallet.balance.amount,
            updated_at=wallet.updated_at
        )
        self.session.add(wallet_model)
        await self.session.flush()

    async def delete(self, wallet_id: UUID) -> None:
        wallet_model = await self.session.get(WalletModel, str(wallet_id))
        if wallet_model:
            await self.session.delete(wallet_model)
            await self.session.flush()

    def _to_entity(self, model: WalletModel) -> Wallet:
        return Wallet(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            balance=Money(model.balance),
            updated_at=model.updated_at
        )
