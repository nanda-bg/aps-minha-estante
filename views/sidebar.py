import tkinter as tk
from tkinter import ttk
from config import STYLE_CONFIG

class Sidebar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Header.TFrame')
        self.controller = controller
        self.buttons = {}

        title_label = ttk.Label(
            self,
            text="Minha Estante",
            font=STYLE_CONFIG["FONT_TITLE"],
            style='Header.TLabel',
            anchor="center"
        )
        title_label.pack(pady=30, padx=10, fill='x')

        pages = {
            "Estante": "EstantePage",
            "Adicionar Livro": "AddLivroPage",
            "Estatísticas": "StatsPage"
        }

        for text, page_name in pages.items():
            button = tk.Button(
                self,
                text=text,
                font=STYLE_CONFIG["FONT_HEADING"],
                bg=STYLE_CONFIG["COMPONENT_BG"],
                fg=STYLE_CONFIG["FG_COLOR"],
                relief="flat",
                anchor="w",
                padx=20,
                pady=12,
                command=lambda p=page_name: self.controller.show_page(p)
            )
            button.pack(fill='x', pady=3, padx=15)
            self.buttons[page_name] = button

    def highlight_button(self, page_name):
        """Destaca o botão da página atualmente visível."""
        for name, button in self.buttons.items():
            if name == page_name:
                button.config(
                    bg=STYLE_CONFIG["ACCENT_COLOR"],
                    fg=STYLE_CONFIG["COMPONENT_BG"]
                )
            else:
                button.config(
                    bg=STYLE_CONFIG["COMPONENT_BG"],
                    fg=STYLE_CONFIG["FG_COLOR"]
                )