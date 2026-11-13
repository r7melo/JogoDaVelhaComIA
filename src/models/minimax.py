
import math
from src.board import Board, SYMBOL_VOID


class Minimax:

    def __init__(self, board: Board, symbol: str):
        self.board = board.copy_state()
        self.AGENT = symbol
        self.ADVERSARY = "X" if symbol == "O" else "O"

    def search(self, board: Board, maximizing: bool):

        winner = board.get_winner()

        if winner == self.AGENT: return 1
        if winner == self.ADVERSARY: return -1
        if board.is_end_game() : return 0

        if maximizing:

            best_score = -math.inf

            for i in range(9):

                if board.get_symbol(i) == SYMBOL_VOID:

                    new_board = board.copy_state()

                    new_board.set_play(i, self.AGENT)

                    score = self.search(new_board, False)

                    best_score = max(best_score, score)

            return best_score

        else:

            best_score = math.inf

            for i in range(9):

                if board.get_symbol(i) == SYMBOL_VOID:

                    # Criar estado independente
                    new_board = board.copy_state()

                    # Simular jogada do adversário
                    new_board.set_play(i, self.ADVERSARY)

                    # Avaliar próxima jogada
                    score = self.search(new_board, True)

                    best_score = min(best_score, score)

            return best_score

    def best_decision(self):

        best_score = -math.inf
        best_pos = -1

        for i in range(9):

            if self.board.get_symbol(i) == SYMBOL_VOID:

                # Simular jogada inicial
                new_board = self.board.copy_state()
                new_board.set_play(i, self.AGENT)

                # Avaliar possibilidades futuras
                score = self.search(new_board, False)

                if score > best_score:
                    best_score = score
                    best_pos = i

        return best_pos
