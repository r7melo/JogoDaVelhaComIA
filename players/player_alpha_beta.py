from typing import Optional
from board import Board
from players.i_player import IPlayer, PlayerStatus
from controll import Controll
from time import sleep

class PlayerAlphaBeta(IPlayer):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
                super().__init__(symbol, board, controll)
    
    def get_decision(self) -> Optional[int]:
        pass

    def set_decision(self, decision: int) -> None:
        self.board.set_play(decision, self.symbol)

    def player_playing(self) -> None:


        self.board.get_cells() 
        decision = self.board.get_cells()[-1] 
        print(f"Player {self.symbol} selected position {decision}")

        sleep(2)


        self.set_decision(decision)

        self.status = PlayerStatus.FINISHED