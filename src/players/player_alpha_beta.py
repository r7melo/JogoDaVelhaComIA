from typing import Optional
from src.board import Board
from src.players.i_player import IPlayer, PlayerStatus
from src.controll import Controll
from time import sleep
from src.models.alpha_beta import AlphaBeta

class PlayerAlphaBeta(IPlayer):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
                super().__init__(symbol, board, controll)
    
    def get_decision(self) -> Optional[int]:
        pass

    def set_decision(self, decision: int) -> None:
        self.board.set_play(decision, self.symbol)

    def player_playing(self) -> None:
        
        decision = AlphaBeta(self.board, self.symbol).best_decision()

        #print(f"Player {self.symbol} selected position {decision}")


        self.set_decision(decision)

        self.status = PlayerStatus.FINISHED

    def __str__(self):
        return "AlphaBeta"