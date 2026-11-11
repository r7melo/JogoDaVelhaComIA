from kivy.uix.gridlayout import GridLayout
from gui import ButtonControll

class Controll(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = 8

        self.buttons = []

        for i in range(9):
            button = ButtonControll()
            self.buttons.append(button)
            self.add_widget(button)

    def update(self, cells: list):
        for i, symbol in enumerate(cells):
            self.buttons[i].text = symbol

