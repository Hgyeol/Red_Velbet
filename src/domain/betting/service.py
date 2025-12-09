"""Betting 도메인 서비스"""
from decimal import Decimal
from typing import List

from src.domain.betting.repository import BetRepository, BetSlipRepository, BettingOptionRepository
from src.domain.betting.entity import Bet, BetSlip
from src.domain.wallet.service import WalletService
from src.domain.common.exceptions import InsufficientFundsException, ValidationException
from src.application.betting.dto import PlaceBetRequestDTO


class BettingService:
    def __init__(
        self,
        bet_repository: BetRepository,
        bet_slip_repository: BetSlipRepository,
        betting_option_repository: BettingOptionRepository,
        wallet_service: WalletService,
    ):
        self.bet_repository = bet_repository
        self.bet_slip_repository = bet_slip_repository
        self.betting_option_repository = betting_option_repository
        self.wallet_service = wallet_service

    async def place_bet(self, user_id: str, place_bet_dto: PlaceBetRequestDTO) -> Bet:
        # 1. Validate bet selections
        if not place_bet_dto.selections:
            raise ValidationException("하나 이상의 배팅을 선택해야 합니다.")

        total_odds = Decimal(1.0)
        for selection in place_bet_dto.selections:
            option = await self.betting_option_repository.find_by_id(selection.option_id)
            if not option or not option.is_active:
                raise ValidationException(f"유효하지 않은 배팅 옵션입니다: {selection.option_id}")
            total_odds *= option.odds

        # 2. Check user's balance
        await self.wallet_service.withdraw(
            user_id=user_id,
            amount=place_bet_dto.amount,
            transaction_type="BET", # This should be an enum
        )

        # 3. Create Bet and BetSlips
        potential_return = place_bet_dto.amount * total_odds
        new_bet = Bet(
            user_id=user_id,
            bet_type=place_bet_dto.bet_type,
            total_amount=place_bet_dto.amount,
            potential_return=potential_return,
            total_odds=total_odds,
        )
        await self.bet_repository.save(new_bet)

        for selection in place_bet_dto.selections:
            option = await self.betting_option_repository.find_by_id(selection.option_id)
            new_slip = BetSlip(
                bet_id=new_bet.id,
                game_id=option.game_id,
                option_id=selection.option_id,
                odds=option.odds,
            )
            await self.bet_slip_repository.save(new_slip)
            new_bet.slips.append(new_slip)

        return new_bet
