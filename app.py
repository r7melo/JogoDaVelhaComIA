from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from menu import MenuScreen
from game import GameScreen

class JogoDaVelhaApp(App):
    def build(self):
        Builder.load_file("style.kv")
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == "__main__":
    JogoDaVelhaApp().run()
