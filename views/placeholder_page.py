from tkinter import ttk
from .base_page import BasePage
from config import STYLE_CONFIG

class PlaceholderPage(BasePage):
    def __init__(self, parent, controller, page_name=""):
        super().__init__(parent, controller)
        
        label = ttk.Label(
            self,
            text=f"Página de '{page_name}' em construção...",
            font=STYLE_CONFIG["FONT_TITLE"],
            anchor="center"
        )
        label.pack(expand=True, fill='both')