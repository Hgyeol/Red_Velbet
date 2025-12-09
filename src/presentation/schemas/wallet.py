from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Literal, Optional

from src.application.wallet.dto import TransactionTypeEnum


class WalletBalanceResponse(BaseModel):
    """지갑 잔액 조회 응답 스키마"""
    wallet_id: UUID = Field(..., description="지갑 ID")
    balance: Decimal = Field(..., gt==-1, description="현재 잔액")
    updated_at: datetime = Field(..., description="마지막 업데이트 시각 (UTC)")


class WalletDepositRequest(BaseModel):
    """지갑 충전 요청 스키마"""
    amount: Decimal = Field(..., gt=0, description="충전 금액")
    payment_method: Literal["card", "bank_transfer"] = Field(..., description="결제 수단")


class WalletWithdrawRequest(BaseModel):
    """지갑 출금 요청 스키마"""
    amount: Decimal = Field(..., gt=0, description="출금 금액")
    bank_account: str = Field(..., min_length=5, description="출금 은행 계좌 번호")


class TransactionResponse(BaseModel):
    """거래 내역 응답 스키마"""
    transaction_id: UUID = Field(..., description="거래 ID")
    wallet_id: UUID = Field(..., description="지갑 ID")
    transaction_type: TransactionTypeEnum = Field(..., description="거래 타입")
    amount: Decimal = Field(..., description="거래 금액 (양수: 충전/환급, 음수: 출금/배팅)")
    balance_after: Decimal = Field(..., description="거래 후 잔액")
    created_at: datetime = Field(..., description="거래 발생 시각 (UTC)")


class PaginatedTransactionResponse(BaseModel):
    """페이지네이션된 거래 내역 응답 스키마"""
    items: List[TransactionResponse]
    pagination: dict # TODO: Replace with a proper Pagination schema

