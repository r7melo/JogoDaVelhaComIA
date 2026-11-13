import threading

from kivy.uix.screenmanager import Clock, Screen, SlideTransition
from board import Board
from gui import *
from players.i_player import IPlayer, PlayerStatus, PlayerStatus
from players.player_alpha_beta import PlayerAlphaBeta
from players.player_human import PlayerHuman
from players.player_minimax import PlayerMinimax
from controll import Controll

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
            threading.Thread(target=self.current_player.player_playing, daemon=True).start()
            self.current_player.status = PlayerStatus.PLAYING

        if self.current_player.status == PlayerStatus.FINISHED:
            self.current_player, self.next_player = self.next_player, self.current_player
            self.current_player.status = PlayerStatus.START
            self.next_player.status = PlayerStatus.WAITING

            print(self.board.all_cells())

    def on_release_btn_reset(self, *_):
        self.board.reset_game()
        self.on_enter()

    def on_release_btn_menu(self, *_):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "menu"

    def on_enter(self, *_):

        x, o = self.mode["X"], self.mode["O"]

        if x == "Player":
            self.current_player: IPlayer = PlayerHuman("X", self.board, self.controll)
        if x == "Minimax":
            self.current_player: IPlayer = PlayerMinimax("X", self.board, self.controll)
        if x == "Alpha-Beta":
            self.current_player: IPlayer = PlayerAlphaBeta("X", self.board, self.controll)

        if o == "Player":
            self.next_player: IPlayer = PlayerHuman("O", self.board, self.controll)
        if o == "Minimax":
            self.next_player: IPlayer = PlayerMinimax("O", self.board, self.controll)
        if o == "Alpha-Beta":
            self.next_player: IPlayer = PlayerAlphaBeta("O", self.board, self.controll)

        self._loop = Clock.schedule_interval(self.update_game, 1 / 30)
        self.current_player.status = PlayerStatus.START   
        self.next_player.status = PlayerStatus.WAITING


    def on_leave(self, *_):
        if self._loop:
            self._loop.cancel()
            self._loop = None
            self.current_player.status = PlayerStatus.WAITING
        


