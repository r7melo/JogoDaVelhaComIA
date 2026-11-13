from kivy.uix.gridlayout import GridLayout
from src.gui import ButtonControll

class Controll(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = 8
        self.on_cell = None
        self.buttons = []

        for i in range(9):
            b = ButtonControll()
            b.bind(on_release=lambda _, i=i: self.on_cell and self.on_cell(i))
            self.buttons.append(b)
            self.add_widget(b)

    def update(self, cells: list):
        for i, symbol in enumerate(cells):
            self.buttons[i].text = symbol

