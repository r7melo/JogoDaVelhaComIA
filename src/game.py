import threading

from kivy.uix.screenmanager import Clock, Screen, SlideTransition
from src.board import Board
from src.gui import *
from src.players.i_player import IPlayer, PlayerStatus, PlayerStatus
from src.players.player_alpha_beta import PlayerAlphaBeta
from src.players.player_human import PlayerHuman
from src.players.player_minimax import PlayerMinimax
from src.controll import Controll

PLAYERS = {"Player": PlayerHuman, "Minimax": PlayerMinimax, "Alpha-Beta": PlayerAlphaBeta}


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._loop = None
        self.board = Board()
        self.current_player: IPlayer = None
        self.next_player: IPlayer = None
        self.controll = Controll()
        self.mode = "PVP"

        background_screen = BackgroundScreen(orientation="vertical", padding=10, spacing=10)

        bar_menu = BarTopScreen()

        btn_menu = ButtonMenu(
            text="Menu",
            size_hint_x=None, 
            width=120, 
            on_release=self.on_release_btn_menu
        )

        btn_reset = ButtonMenu(
            text="Reiniciar", 
            size_hint_x=None, 
            width=140, 
            on_release=self.on_release_btn_reset
        )

        bar_menu.add_widget(btn_menu)
        bar_menu.add_widget(btn_reset)


        self.status = Status(text=f"", size_hint_y=None, height=40)

        background_screen.add_widget(bar_menu)
        background_screen.add_widget(self.status)
        background_screen.add_widget(self.controll)
        self.add_widget(background_screen)

    def update_game(self, dt):
        
        self.controll.update(self.board.all_cells())

        self.status.text = f"Vez do {self.current_player.__str__()}"

        has_winner, winner = self.board.has_winner()
        if has_winner:
            self.status.text = f"{self.current_player.__str__()} venceu!"
            self.on_leave()

        elif self.board.is_end_game():
            self.status.text = "Empate!"
            self.on_leave()

        if self.current_player.status == PlayerStatus.START:
            self.current_player.status = PlayerStatus.PLAYING
            threading.Thread(target=self.current_player.player_playing, daemon=True).start()

        if self.current_player.status == PlayerStatus.FINISHED:
            self.current_player, self.next_player = self.next_player, self.current_player
            self.current_player.status = PlayerStatus.START
            self.next_player.status = PlayerStatus.WAITING

            #print(self.board.all_cells())

    def on_release_btn_reset(self, *_):
        self.board.reset_game()
        self.on_enter()

    def on_release_btn_menu(self, *_):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"

    def _stop_loop(self):
        if self._loop:
            self._loop.cancel()
            self._loop = None

    def on_enter(self, *_):
        self._stop_loop()
        self.controll.on_cell = None
        self.board = Board()
        self.controll.update(self.board.all_cells())
        self.current_player = PLAYERS[self.mode["X"]]("X", self.board, self.controll)
        self.next_player = PLAYERS[self.mode["O"]]("O", self.board, self.controll)
        self.current_player.status = PlayerStatus.START
        self._loop = Clock.schedule_interval(self.update_game, 1 / 30)

    def on_leave(self, *_):
        self._stop_loop()

    
        


