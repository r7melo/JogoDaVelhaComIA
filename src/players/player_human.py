from typing import Optional
from src.board import Board
from src.players.i_player import IPlayer, PlayerStatus
from src.controll import Controll
from time import sleep

class PlayerHuman(IPlayer):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
        super().__init__(symbol, board, controll)
        controll.on_cell = self.set_decision

    def get_decision(self) -> Optional[int]:
        pass

    def set_decision(self, decision: int) -> None:

        if self.status == PlayerStatus.PLAYING and self.board.valide_play(decision):
            self.board.set_play(decision, self.symbol)
            self.status = PlayerStatus.FINISHED

    def player_playing(self) -> None:
        pass

    def __str__(self):
        return f"Jogador {self.symbol}"
            