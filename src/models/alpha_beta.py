import math
from time import perf_counter

from src.board import Board
from src.models.minimax import Minimax, Decision, opponent


class AlphaBeta(Minimax):

    def search(self, board: Board, player: str,
               alpha: float = -math.inf, beta: float = math.inf) -> int:
        self.nodes += 1

        u = self.utility(board)
        if u is not None:
            return u

        if player == "X":
            best = -math.inf
            for pos in self.moves(board):
                child = board.copy_state()
                child.set_play(pos, player)
                best = max(best, self.search(child, opponent(player), alpha, beta))
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return best
        else:
            best = math.inf
            for pos in self.moves(board):
                child = board.copy_state()
                child.set_play(pos, player)
                best = min(best, self.search(child, opponent(player), alpha, beta))
                beta = min(beta, best)
                if alpha >= beta:
                    break
            return best

    def best_decision(self) -> Decision:
        self.nodes = 0
        start = perf_counter()

        maximizing = self.AGENT == "X"
        best_value = -math.inf if maximizing else math.inf
        best_pos = -1
        alpha, beta = -math.inf, math.inf

        for pos in self.moves(self.board):
            child = self.board.copy_state()
            child.set_play(pos, self.AGENT)
            value = self.search(child, opponent(self.AGENT), alpha, beta)
            if (maximizing and value > best_value) or (not maximizing and value < best_value):
                best_value, best_pos = value, pos
            if maximizing:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value)

        elapsed = (perf_counter() - start) * 1000
        return Decision(best_pos, best_value, self.nodes, elapsed)