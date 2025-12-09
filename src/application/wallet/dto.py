from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Literal


class WalletBalanceDto(BaseModel):
    """지갑 잔액 조회 DTO"""
    wallet_id: UUID
    balance: Decimal
    updated_at: datetime


class WalletDepositRequestDto(BaseModel):
    """지갑 충전 요청 DTO"""
    amount: Decimal
    payment_method: Literal["card", "bank_transfer"]


class WalletWithdrawRequestDto(BaseModel):
    """지갑 출금 요청 DTO"""
    amount: Decimal
    bank_account: str


class TransactionTypeEnum(str, Literal["충전", "출금", "배팅", "환급"]):
    """거래 타입 Enum"""
    pass


class TransactionDto(BaseModel):
    """거래 내역 DTO"""
    transaction_id: UUID
    wallet_id: UUID
    transaction_type: TransactionTypeEnum
    amount: Decimal
    balance_after: Decimal
    created_at: datetime