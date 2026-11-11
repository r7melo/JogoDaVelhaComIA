from typing import Optional
from board import Board
from players.i_player import IPlayer, PlayerStatus
from controll import Controll
from time import sleep

class PlayerHuman(IPlayer):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
        super().__init__(symbol, board, controll)

        for index, button in enumerate(self.controll.buttons):
            button.bind(on_release=lambda _, i=index: self.set_decision(i))

    def get_decision(self) -> Optional[int]:
        pass

    def set_decision(self, decision: int) -> None:

        if self.status == PlayerStatus.WAITING:
            return
        
        if self.status == PlayerStatus.PLAYING and self.board.valide_play(decision):
            print(f"Player {self.symbol} selected position {decision}")
            self.decision = decision
            self.board.set_play(self.decision, self.symbol)
            self.decision = None
            self.status = PlayerStatus.FINISHED

    def player_playing(self) -> None:

        while self.decision is None:
            sleep(0.1)

    def __str__(self):
        return f"Jogador {self.symbol}"
            