from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from controll import Controll

from abc import ABC, abstractmethod
from enum import Enum
from board import Board 
from typing import Optional




class PlayerStatus(Enum):
    WAITING = 1
    START = 2
    PLAYING = 3
    FINISHED = 4

class IPlayer(ABC):
    def __init__(self, symbol: str, board: Board, controll: Controll) -> None:
        self.symbol = symbol
        self.board = board
        self.controll = controll
        self.status = PlayerStatus.WAITING
        self.decision = None

    @abstractmethod
    def get_decision(self) -> None:
        pass

    @abstractmethod
    def set_decision(self, decision: int) -> None:
        pass

    @abstractmethod
    def player_playing(self) -> None:
        pass

    @abstractmethod
    def __str__(self):
        pass
