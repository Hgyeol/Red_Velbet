from uuid import UUID
from decimal import Decimal
from typing import List, Optional

from src.application.wallet.dto import WalletBalanceDto, WalletDepositRequestDto, WalletWithdrawRequestDto, TransactionDto
from src.domain.wallet.service import WalletService
from src.domain.common.value_objects import Money
from src.domain.common.exceptions import EntityNotFoundException, DomainException


class WalletUseCases:
    """
    지갑 관련 비즈니스 로직을 처리하는 유스케이스
    """

    def __init__(self, wallet_service: WalletService):
        self.wallet_service = wallet_service

    async def get_wallet_balance(self, user_id: UUID) -> WalletBalanceDto:
        """
        사용자 ID로 지갑 잔액을 조회합니다.
        """
        wallet = await self.wallet_service.get_wallet_by_user_id(user_id)
        return WalletBalanceDto(
            wallet_id=wallet.id,
            balance=wallet.balance.amount,
            updated_at=wallet.updated_at
        )

    async def deposit_to_wallet(self, user_id: UUID, request_dto: WalletDepositRequestDto) -> WalletBalanceDto:
        """
        사용자 지갑에 금액을 입금하고 잔액을 업데이트합니다.
        """
        amount = Money(request_dto.amount)
        updated_wallet = await self.wallet_service.deposit_to_wallet(user_id, amount)
        # TODO: 트랜잭션 기록 (TransactionService 구현 시)
        return WalletBalanceDto(
            wallet_id=updated_wallet.id,
            balance=updated_wallet.balance.amount,
            updated_at=updated_wallet.updated_at
        )

    async def withdraw_from_wallet(self, user_id: UUID, request_dto: WalletWithdrawRequestDto) -> WalletBalanceDto:
        """
        사용자 지갑에서 금액을 출금하고 잔액을 업데이트합니다.
        """
        amount = Money(request_dto.amount)
        updated_wallet = await self.wallet_service.withdraw_from_wallet(user_id, amount)
        # TODO: 트랜잭션 기록 (TransactionService 구현 시)
        return WalletBalanceDto(
            wallet_id=updated_wallet.id,
            balance=updated_wallet.balance.amount,
            updated_at=updated_wallet.updated_at
        )

    # TODO: 지갑 거래 내역 조회 (TransactionService 구현 시)
    # async def get_wallet_transactions(self, user_id: UUID, **filters) -> List[TransactionDto]:
    #     """
    #     사용자 지갑의 거래 내역을 조회합니다.
    #     """
    #     wallet = await self.wallet_service.get_wallet_by_user_id(user_id)
    #     transactions = await self.transaction_service.get_transactions_by_wallet_id(wallet.id, **filters)
    #     return [
    #         TransactionDto(
    #             transaction_id=t.id,
    #             wallet_id=t.wallet_id,
    #             transaction_type=t.transaction_type,
    #             amount=t.amount.amount,
    #             balance_after=t.balance_after.amount,
    #             created_at=t.created_at
    #         ) for t in transactions
    #     ]
