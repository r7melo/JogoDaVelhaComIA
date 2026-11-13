from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition
from src.gui import *

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        background_screen = BackgroundScreen(orientation="vertical", padding=60, spacing=20)
        background_screen.add_widget(TitleGame(text="Jogo da Velha"))

        # Labels X e O em cima
        labels_row = BoxLayout(orientation="horizontal", spacing=40)
        labels_row.add_widget(Label(text="X", font_size=64, bold=True))
        labels_row.add_widget(Label(text="O", font_size=64, bold=True))
        background_screen.add_widget(labels_row)

        # Spinners embaixo
        spinners_row = BoxLayout(orientation="horizontal", spacing=40, size_hint=(1, None), height=50)
        self.spinner_x = SpinnerMenu(
            text="Player",
            values=["Player", "Minimax", "Alpha-Beta"],
        )
        self.spinner_o = SpinnerMenu(
            text="Player",
            values=["Player", "Minimax", "Alpha-Beta"],
        )
        spinners_row.add_widget(self.spinner_x)
        spinners_row.add_widget(self.spinner_o)
        background_screen.add_widget(spinners_row)

        # Botão Play
        btn_play = ButtonMenu(text="Play")
        btn_play.bind(on_release=self.go_game)
        background_screen.add_widget(btn_play)

        self.add_widget(background_screen)
        
    def go_game(self, instance):

        game_screen = self.manager.get_screen("game")

        game_screen.mode = {
            "X": self.spinner_x.text,
            "O": self.spinner_o.text,
        }

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "game"
