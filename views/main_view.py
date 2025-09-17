import tkinter as tk
from tkinter import ttk
from config import STYLE_CONFIG
from .sidebar import Sidebar
from .estante_page import EstantePage
from .placeholder_page import PlaceholderPage
from .edit_livro_page import EditLivroPage
from .add_livro_page import AddLivroPage

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.controller = None
        
        self.title("Minha Estante")
        self.geometry("1100x750")
        self.minsize(800, 600)
        self.configure(bg=STYLE_CONFIG["BG_COLOR"])

        self._configurar_estilos_ttk()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.page_container = ttk.Frame(self)
        self.page_container.grid(row=0, column=1, sticky="nsew")
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}

    def set_controller(self, controller):
        """Recebe o controller e finaliza a configuração da UI."""
        self.controller = controller
        
        self.sidebar = Sidebar(self, self.controller)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        for PageClass, name in [(EstantePage, "EstantePage"), 
                                (EditLivroPage, "EditLivroPage"),
                                (AddLivroPage, "AddLivroPage"),
                                (PlaceholderPage, "StatsPage")]:
            if PageClass == PlaceholderPage:
                page = PageClass(self.page_container, self.controller, page_name=name.replace("Page", ""))
            else:
                page = PageClass(self.page_container, self.controller)
            
            self.pages[name] = page
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name, *args):
        """Mostra a página especificada pelo nome."""
        if not self.controller:
            return

        page = self.pages[page_name]
        
        if hasattr(page, 'on_show'):
            page.on_show(*args)

        page.tkraise()

        if page_name in ["EstantePage", "StatsPage", "AddLivroPage"]:
            self.sidebar.highlight_button(page_name)
    
    def start(self):
        """Inicia o loop principal da aplicação."""
        self.show_page("EstantePage")
        self.mainloop()
    
    def _configurar_estilos_ttk(self):
        """Configura os estilos do ttk."""
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background=STYLE_CONFIG["BG_COLOR"], foreground=STYLE_CONFIG["FG_COLOR"], font=STYLE_CONFIG["FONT_NORMAL"])
        style.configure('TFrame', background=STYLE_CONFIG["BG_COLOR"])
        style.configure('TLabel', background=STYLE_CONFIG["BG_COLOR"])
        style.configure('Header.TFrame', background=STYLE_CONFIG["HEADER_BG"])
        style.configure('Header.TLabel', background=STYLE_CONFIG["HEADER_BG"], font=STYLE_CONFIG["FONT_TITLE"], foreground=STYLE_CONFIG["FG_COLOR"])
        style.configure('Card.TFrame', background=STYLE_CONFIG["COMPONENT_BG"])
        style.configure('Card.TLabel', background=STYLE_CONFIG["COMPONENT_BG"])
        style.configure('Filter.TRadiobutton', font=STYLE_CONFIG["FONT_HEADING"], padding=(10, 5), anchor='center')
        style.map('Filter.TRadiobutton', background=[('selected', STYLE_CONFIG["ACCENT_COLOR"]), ('active', STYLE_CONFIG["HEADER_BG"])], foreground=[('selected', STYLE_CONFIG["COMPONENT_BG"])])
        style.configure('Delete.TButton', background=STYLE_CONFIG["DELETE_COLOR"], foreground='white', font=STYLE_CONFIG["FONT_NORMAL"])
        style.map('Delete.TButton', background=[('active', '#C70039')])
        style.configure('Card.TCombobox', font=STYLE_CONFIG["FONT_NORMAL"], padding=5)
        self.option_add('*TCombobox*Listbox.font', STYLE_CONFIG["FONT_NORMAL"])
        self.option_add('*TCombobox*Listbox.background', STYLE_CONFIG["COMPONENT_BG"])
        self.option_add('*TCombobox*Listbox.foreground', STYLE_CONFIG["FG_COLOR"])
        self.option_add('*TCombobox*Listbox.selectBackground', STYLE_CONFIG["ACCENT_COLOR"])
        self.option_add('*TCombobox*Listbox.selectForeground', STYLE_CONFIG["COMPONENT_BG"])