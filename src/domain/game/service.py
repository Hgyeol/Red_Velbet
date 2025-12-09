"""Game 도메인 서비스"""
from src.domain.game.repository import GameRepository
from src.domain.betting.repository import BetRepository, BetSlipRepository
from src.domain.wallet.service import WalletService
from src.domain.game.entity import Game
from src.domain.betting.entity import Bet, BetSlip, BettingOption
from src.domain.betting.enums import BetStatusEnum, BetSlipResultEnum
from typing import List


class GameService:
    def __init__(
        self,
        game_repository: GameRepository,
        bet_repository: BetRepository,
        bet_slip_repository: BetSlipRepository,
        wallet_service: WalletService,
    ):
        self.game_repository = game_repository
        self.bet_repository = bet_repository
        self.bet_slip_repository = bet_slip_repository
        self.wallet_service = wallet_service

    async def settle_game(self, game_id: str, winning_option_ids: List[str]):
        game = await self.game_repository.find_by_id(game_id)
        if not game:
            raise ValueError("게임을 찾을 수 없습니다.")

        bets_to_settle = await self.bet_repository.find_by_game_id(game_id) # This method needs to be added to the repository

        for bet in bets_to_settle:
            slips = await self.bet_slip_repository.find_by_bet_id(bet.id)
            is_win = True
            for slip in slips:
                if slip.option_id in winning_option_ids:
                    slip.result = BetSlipResultEnum.WIN
                else:
                    slip.result = BetSlipResultEnum.LOSS
                    is_win = False
                await self.bet_slip_repository.save(slip)
            
            if is_win:
                bet.win()
                await self.wallet_service.deposit(
                    user_id=bet.user_id,
                    amount=bet.potential_return,
                    transaction_type="REFUND", # This should be an enum
                )
            else:
                bet.lose()
            
            await self.bet_repository.save(bet)
