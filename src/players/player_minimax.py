from typing import Optional
from src.board import Board
from src.controll import Controll
from src.players.i_player import IPlayer, PlayerStatus
from src.models.minimax import Minimax

class PlayerMinimax(IPlayer):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
        super().__init__(symbol, board, controll)
    
    def get_decision(self) -> Optional[int]:
        pass

    def set_decision(self, decision: int) -> None:
        self.board.set_play(decision, self.symbol)

    def player_playing(self) -> None:

        d = Minimax(self.board, self.symbol).best_decision()
        self.last_decision = d
        self.set_decision(d.position)
        self.status = PlayerStatus.FINISHED

        print(f"Minimax: symbol={self.symbol}, pos={d.position}, valor={d.value:+.1f}, nos={d.nodes}, tempo={d.time_ms:.2f} ms")


    def __str__(self):
        return "Minimax"
    