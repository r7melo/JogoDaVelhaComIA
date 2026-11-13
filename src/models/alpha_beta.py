
import math
from src.board import Board, SYMBOL_VOID


class AlphaBeta:

    def __init__(self, board: Board, symbol: str):
        self.board = board.copy_state()
        self.AGENT = symbol
        self.ADVERSARY = "X" if symbol == "O" else "O"

    def search(
        self,
        board: Board,
        maximizing: bool,
        alpha: float = -math.inf,
        beta: float = math.inf
    ):

        winner = board.get_winner()

        if winner == self.AGENT:
            return 10

        if winner == self.ADVERSARY:
            return -10

        if board.is_end_game():
            return 0

        if maximizing:

            best_score = -math.inf

            for i in range(9):

                new_board = board.copy_state()

                if new_board.set_play(i, self.AGENT):

                    score = self.search(new_board, False, alpha, beta)

                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)

                    if alpha >= beta:
                        break

            return best_score

        else:

            best_score = math.inf

            for i in range(9):

                new_board = board.copy_state()

                if new_board.set_play(i, self.ADVERSARY):

                    score = self.search(new_board, True, alpha, beta)

                    best_score = min(best_score, score)
                    beta = min(beta, best_score)

                    if alpha >= beta:
                        break

            return best_score

    def best_decision(self):

        best_score = -math.inf
        best_pos = -1

        alpha = -math.inf
        beta = math.inf

        for i in range(9):

            new_board = self.board.copy_state()

            if new_board.set_play(i, self.AGENT):

                score = self.search(new_board, False, alpha, beta)

                if score > best_score:
                    best_score = score
                    best_pos = i

                alpha = max(alpha, best_score)

        return best_pos
