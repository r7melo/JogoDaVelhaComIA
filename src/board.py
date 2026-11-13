from typing import List, Optional, Tuple

SYMBOL_VOID: str = ""
VICTORY_CONDITION: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

class Board:

    def __init__(self) -> None:
        self._cells: List[str] = [SYMBOL_VOID] * 9

    def all_cells(self) -> List[str]:
        return list(self._cells)

    def get_symbol(self, pos: int) -> str:
        return self._cells[pos]

    def valide_play(self, pos: int) -> bool:
        if pos < 0 or pos > 8:
            return False
        return self._cells[pos] == SYMBOL_VOID

    def set_play(self, pos: int, symbol: str) -> bool:
        if not self.valide_play(pos):
            return False
        self._cells[pos] = symbol
        return True

    def get_cells(self) -> List[int]:
        return [i for i, symbol in enumerate(self._cells) if symbol == SYMBOL_VOID]

    def get_winner(self) -> Optional[str]:
        for a, b, c in VICTORY_CONDITION:
            if (
                self._cells[a] != SYMBOL_VOID
                and self._cells[a] == self._cells[b] == self._cells[c]
            ):
                return self._cells[a]
        return None

    def is_end_game(self) -> bool:
        return SYMBOL_VOID not in self._cells

    def has_winner(self) -> tuple[bool, Optional[str]]:
        winner = self.get_winner()
        return winner is not None, winner

    def reset_game(self) -> None:
        self._cells = [SYMBOL_VOID] * 9

    def copy_state(self) -> "Board":
        novo = Board()
        novo._cells = list(self._cells)
        return novo
