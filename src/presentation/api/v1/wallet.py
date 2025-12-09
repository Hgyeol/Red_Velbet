from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.application.wallet.dto import WalletDepositRequestDto, WalletWithdrawRequestDto
from src.application.wallet.use_cases import WalletUseCases
from src.domain.common.exceptions import EntityNotFoundException, DomainException
from src.presentation.api.dependencies import get_current_user, get_wallet_use_cases
from src.presentation.schemas.common import SuccessResponse
from src.presentation.schemas.user import UserResponse
from src.presentation.schemas.wallet import WalletBalanceResponse, WalletDepositRequest, WalletWithdrawRequest


router = APIRouter()


@router.get(
    "/balance",
    response_model=SuccessResponse[WalletBalanceResponse],
    summary="지갑 잔액 조회",
    description="현재 로그인한 사용자의 지갑 잔액을 조회합니다.",
    status_code=status.HTTP_200_OK
)
async def get_wallet_balance(
    current_user: UserResponse = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_use_cases)
):
    """
    현재 로그인한 사용자의 지갑 잔액을 조회합니다.
    """
    try:
        balance_dto = await wallet_use_cases.get_wallet_balance(current_user.user_id)
        return SuccessResponse[WalletBalanceResponse](
            data=WalletBalanceResponse(**balance_dto.model_dump())
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/deposit",
    response_model=SuccessResponse[WalletBalanceResponse],
    summary="지갑 충전",
    description="지갑에 금액을 충전합니다.",
    status_code=status.HTTP_200_OK # 201 Created도 가능하지만, 잔액 업데이트는 200 OK도 적절
)
async def deposit_to_wallet(
    request: WalletDepositRequest,
    current_user: UserResponse = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_use_cases)
):
    """
    지갑에 금액을 충전합니다.
    """
    deposit_dto = WalletDepositRequestDto(amount=request.amount, payment_method=request.payment_method)
    try:
        balance_dto = await wallet_use_cases.deposit_to_wallet(current_user.user_id, deposit_dto)
        return SuccessResponse[WalletBalanceResponse](
            data=WalletBalanceResponse(**balance_dto.model_dump())
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/withdraw",
    response_model=SuccessResponse[WalletBalanceResponse],
    summary="지갑 출금",
    description="지갑에서 금액을 출금합니다.",
    status_code=status.HTTP_200_OK
)
async def withdraw_from_wallet(
    request: WalletWithdrawRequest,
    current_user: UserResponse = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_use_cases)
):
    """
    지갑에서 금액을 출금합니다.
    """
    withdraw_dto = WalletWithdrawRequestDto(amount=request.amount, bank_account=request.bank_account)
    try:
        balance_dto = await wallet_use_cases.withdraw_from_wallet(current_user.user_id, withdraw_dto)
        return SuccessResponse[WalletBalanceResponse](
            data=WalletBalanceResponse(**balance_dto.model_dump())
        )
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: 거래 내역 조회 엔드포인트 추가 (TransactionService 구현 시)
# @router.get(
#     "/transactions",
#     response_model=SuccessResponse[PaginatedTransactionResponse],
#     summary="거래 내역 조회",
#     description="사용자의 지갑 거래 내역을 조회합니다.",
#     status_code=status.HTTP_200_OK
# )
# async def get_transactions(
#     current_user: UserResponse = Depends(get_current_user),
#     wallet_use_cases: WalletUseCases = Depends(get_wallet_use_cases),
#     transaction_type: Optional[TransactionTypeEnum] = Query(None, description="거래 타입"),
#     start_date: Optional[date] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
#     end_date: Optional[date] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
#     page: int = Query(1, ge=1, description="페이지 번호"),
#     limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수")
# ):
#     """
#     사용자의 지갑 거래 내역을 조회합니다.
#     """
#     filters = {
#         "transaction_type": transaction_type,
#         "start_date": start_date,
#         "end_date": end_date,
#         "page": page,
#         "limit": limit
#     }
#     try:
#         transactions = await wallet_use_cases.get_wallet_transactions(current_user.user_id, **filters)
#         # TODO: PaginatedTransactionResponse에 맞게 데이터 변환 필요
#         return SuccessResponse[PaginatedTransactionResponse](
#             data=PaginatedTransactionResponse(items=transactions, pagination={"page": page, "limit": limit, "total": 0, "total_pages": 0})
#         )
#     except ResourceNotFoundException as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
