import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from .base_page import BasePage
from config import STYLE_CONFIG, IMAGES_DIR, STATUS_OPCOES

class EstantePage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.last_width = 0
        self._create_widgets()

    def on_show(self):
        """ Atualiza a lista de livros ao mostrar a página. """
        self.after(50, self.filtrar_lista)

    def update_display(self, livros_para_mostrar):
        """ Atualiza a exibição dos livros na estante. """
        for widget in self.frame_lista_livros.winfo_children():
            widget.destroy()

        if not livros_para_mostrar:
            self.frame_lista_livros.grid_rowconfigure(0, weight=1)
            self.frame_lista_livros.grid_columnconfigure(0, weight=1)
            filtro = self.filtro_status_var.get()
            mensagem = f"Nenhum livro encontrado com o status '{filtro}'."
            if filtro == "Todos" and not self.controller.get_livros():
                  mensagem = "Sua estante está vazia.\nAdicione seu primeiro livro!"
            ttk.Label(self.frame_lista_livros, text=mensagem, font=STYLE_CONFIG["FONT_HEADING"], justify='center', anchor='center').grid(row=0, column=0, pady=50, sticky='nsew')
            return
            
        container_width = self.canvas.winfo_width()
        card_width_estimado = 240
        num_colunas = max(1, container_width // card_width_estimado)

        for i, livro in enumerate(livros_para_mostrar):
            row, col = divmod(i, num_colunas)
            self._criar_card_livro(livro, row, col)
            self.frame_lista_livros.grid_columnconfigure(col, weight=1)
    
    def filtrar_lista(self):
        """ Filtra a lista de livros com base no status selecionado. """
        filtro = self.filtro_status_var.get()
        livros = self.controller.get_livros(filtro)
        self.update_display(livros)

    def mudar_status(self, livro_id, novo_status):
        """ Muda o status do livro especificado. """
        self.controller.mudar_status(livro_id, novo_status)
    
    def _abrir_edicao(self, livro_id):
        """ Abre a página de edição para o livro especificado. """
        self.controller.show_edit_page(livro_id)

    def _create_widgets(self):
        """ Cria os widgets da página da estante. """
        header_frame = ttk.Frame(self, style='Header.TFrame', padding=(20, 15))
        header_frame.pack(fill='x', side='top')

        filtros_frame = ttk.Frame(header_frame, style='Header.TFrame', padding=(0, 15, 0, 0))
        filtros_frame.pack()

        self.filtro_status_var = tk.StringVar(value="Todos")
        opcoes_filtro = ["Todos"] + STATUS_OPCOES

        for opcao in opcoes_filtro:
            rb = ttk.Radiobutton(filtros_frame, text=opcao, variable=self.filtro_status_var, value=opcao, command=self.filtrar_lista, style='Filter.TRadiobutton')
            rb.pack(side='left', padx=5)

        container = ttk.Frame(self, padding=10)
        container.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(container, bg=STYLE_CONFIG["BG_COLOR"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.frame_lista_livros = ttk.Frame(self.canvas, style='TFrame')
        self.frame_lista_livros.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame_lista_livros, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _criar_card_livro(self, livro, row, col):
        """ Cria um card para exibir as informações do livro. """
        card = ttk.Frame(self.frame_lista_livros, style='Card.TFrame', padding=15)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        callback = lambda event, b_id=livro.get_id(): self._abrir_edicao(b_id)

        card.bind("<Button-1>", callback)

        label_img = None
        try:
            caminho_img = os.path.join(IMAGES_DIR, os.path.basename(livro.get_caminho_imagem()))
            photo = ImageTk.PhotoImage(Image.open(caminho_img).resize((120, 180), Image.Resampling.LANCZOS))
            label_img = ttk.Label(card, image=photo, style='Card.TLabel')
            label_img.image = photo
            label_img.pack(pady=(0, 10))
        except Exception:
            placeholder = tk.Canvas(card, width=120, height=180, bg="#cccccc", highlightthickness=0)
            placeholder.create_text(60, 90, text="Capa\nIndisponível", fill="white", font=STYLE_CONFIG["FONT_NORMAL"], justify="center")
            placeholder.pack(pady=(0, 10))
            placeholder.bind("<Button-1>", callback)
        
        if label_img:
            label_img.bind("<Button-1>", callback)
            
        label_titulo = ttk.Label(card, text=livro.get_titulo(), style='Card.TLabel', font=STYLE_CONFIG["FONT_CARD_TITLE"], wraplength=180, justify='center')
        label_titulo.pack(fill='x', pady=5, expand=True)
        label_titulo.bind("<Button-1>", callback)

        label_autor = ttk.Label(card, text=livro.get_autor().get_nome(), style='Card.TLabel', font=STYLE_CONFIG["FONT_NORMAL"], justify='center')
        label_autor.pack(fill='x', pady=(0, 15), expand=True)
        label_autor.bind("<Button-1>", callback)

        status_var = tk.StringVar()
        menu_status = ttk.Combobox(card, textvariable=status_var, values=STATUS_OPCOES, state="readonly", style="Card.TCombobox")
        
        if livro.get_status():
            status_var.set(livro.get_status().get_nome())

        menu_status.pack(fill='x', side='bottom')
        menu_status.bind("<<ComboboxSelected>>", lambda event, b_id=livro.get_id(), var=status_var: self.mudar_status(b_id, var.get()))

    def on_canvas_resize(self, event):
        """ Ajusta o layout dos cards quando a tela é redimensionada. """
        new_width = event.width
        self.canvas.itemconfig(self.frame_id, width=new_width)
        card_width_estimado = 240
        old_cols = max(1, self.last_width // card_width_estimado)
        new_cols = max(1, new_width // card_width_estimado)
        if old_cols != new_cols:
            self.last_width = new_width
            self.filtrar_lista()