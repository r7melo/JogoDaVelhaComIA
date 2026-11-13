import math
from dataclasses import dataclass
from time import perf_counter

from src.board import Board


@dataclass
class Decision:
    position: int
    value: int
    nodes: int
    time_ms: float


def opponent(symbol: str) -> str:
    return "O" if symbol == "X" else "X"


class Minimax:
    def __init__(self, board: Board, symbol: str, reverse: bool = False):
        self.board = board.copy_state()
        self.AGENT = symbol
        self.reverse = reverse
        self.nodes = 0

    def moves(self, board: Board) -> list:
        cells = board.get_cells()
        return cells[::-1] if self.reverse else cells

    def utility(self, board: Board):
        winner = board.get_winner()
        if winner == "X":
            return 1
        if winner == "O":
            return -1
        if board.is_end_game():
            return 0
        return None

    def search(self, board: Board, player: str) -> int:
        self.nodes += 1

        u = self.utility(board)
        if u is not None:
            return u

        best = -math.inf if player == "X" else math.inf
        for pos in self.moves(board):
            child = board.copy_state()
            child.set_play(pos, player)
            value = self.search(child, opponent(player))
            best = max(best, value) if player == "X" else min(best, value)
        return best

    def best_decision(self) -> Decision:
        self.nodes = 0
        start = perf_counter()

        maximizing = self.AGENT == "X"
        best_value = -math.inf if maximizing else math.inf
        best_pos = -1

        for pos in self.moves(self.board):
            child = self.board.copy_state()
            child.set_play(pos, self.AGENT)
            value = self.search(child, opponent(self.AGENT))
            if (maximizing and value > best_value) or (not maximizing and value < best_value):
                best_value, best_pos = value, pos

        elapsed = (perf_counter() - start) * 1000
        return Decision(best_pos, best_value, self.nodes, elapsed)