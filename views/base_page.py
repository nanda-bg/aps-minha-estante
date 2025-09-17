from tkinter import ttk

class BasePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

    def on_show(self):
        """Método chamado sempre que a página é exibida."""
        pass