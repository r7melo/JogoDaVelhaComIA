from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from gui import BackgroundScreen, TitleGame, ButtonMenu

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        background_screen = BackgroundScreen(orientation="vertical", padding=60, spacing=20)
        background_screen.add_widget(TitleGame(text="Jogo da Velha"))

        btn_play_pvp = ButtonMenu(text="Player vs Player")
        btn_play_pvp.mode = "PVP"
        btn_play_pvp.bind(on_release=self.go_game)

        btn_play_pvm = ButtonMenu(text="Player vs Minimax")
        btn_play_pvm.mode = "PVM"
        btn_play_pvm.bind(on_release=self.go_game)

        btn_play_pva = ButtonMenu(text="Player vs Alpha-Beta")
        btn_play_pva.mode = "PVA"
        btn_play_pva.bind(on_release=self.go_game)

        btn_play_mva = ButtonMenu(text="Minimax vs Alpha-Beta")
        btn_play_mva.mode = "MVA"
        btn_play_mva.bind(on_release=self.go_game)

        background_screen.add_widget(btn_play_pvp)
        background_screen.add_widget(btn_play_pvm)
        background_screen.add_widget(btn_play_pva)
        background_screen.add_widget(btn_play_mva)
        self.add_widget(background_screen)

    def go_game(self, instance):

        game_screen = self.manager.get_screen("game")
        game_screen.mode = instance.mode

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "game"
