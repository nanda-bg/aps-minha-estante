import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from .base_page import BasePage
from config import STYLE_CONFIG, IMAGES_DIR, STATUS_OPCOES

class AddLivroPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.caminho_capa_selecionada = None

        self.titulo_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.ano_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._create_widgets()

    def on_show(self):
        """ Limpa o formulário para um novo cadastro. """
        self.titulo_var.set("")
        self.autor_var.set("")
        self.genero_var.set("")
        self.ano_var.set("")
        self.status_var.set("Quero Ler")
        self.caminho_capa_selecionada = None
        self._carregar_imagem_capa(None)

    def _create_widgets(self):
        """Cria os widgets da página de adicionar livro."""
        main_frame = ttk.Frame(self, padding=(20, 20))
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_columnconfigure(1, weight=1)

        frame_capa = ttk.Frame(main_frame, padding=(0, 0, 20, 0))
        frame_capa.grid(row=0, column=0, sticky='nsw', rowspan=2)

        self.label_capa = ttk.Label(frame_capa)
        self.label_capa.pack(pady=(0, 10))

        btn_selecionar_capa = ttk.Button(frame_capa, text="Selecionar Capa", command=self._selecionar_capa)
        btn_selecionar_capa.pack(fill='x')

        frame_detalhes = ttk.Frame(main_frame)
        frame_detalhes.grid(row=0, column=1, sticky='nsew')
        frame_detalhes.grid_columnconfigure(1, weight=1)
        
        ttk.Label(frame_detalhes, text="Título:").grid(row=0, column=0, sticky='w', pady=5)
        entry_titulo = ttk.Entry(frame_detalhes, textvariable=self.titulo_var)
        entry_titulo.grid(row=0, column=1, sticky='ew', pady=5)

        ttk.Label(frame_detalhes, text="Autor:").grid(row=1, column=0, sticky='w', pady=5)
        entry_autor = ttk.Entry(frame_detalhes, textvariable=self.autor_var)
        entry_autor.grid(row=1, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame_detalhes, text="Gênero:").grid(row=2, column=0, sticky='w', pady=5)
        entry_genero = ttk.Entry(frame_detalhes, textvariable=self.genero_var)
        entry_genero.grid(row=2, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame_detalhes, text="Ano:").grid(row=3, column=0, sticky='w', pady=5)
        entry_ano = ttk.Entry(frame_detalhes, textvariable=self.ano_var)
        entry_ano.grid(row=3, column=1, sticky='ew', pady=5)

        ttk.Label(frame_detalhes, text="Status:").grid(row=4, column=0, sticky='w', pady=5)
        combo_status = ttk.Combobox(frame_detalhes, textvariable=self.status_var, values=STATUS_OPCOES, state='readonly')
        combo_status.grid(row=4, column=1, sticky='ew', pady=5)

        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.grid(row=1, column=1, sticky='es', pady=(20, 0))

        btn_cadastrar = ttk.Button(frame_botoes, text="Cadastrar Livro", command=self._cadastrar_livro, style="Accent.TButton")
        btn_cadastrar.pack(side='right', padx=(10, 0))

        btn_cancelar = ttk.Button(frame_botoes, text="Cancelar", command=lambda: self.controller.show_page("EstantePage"))
        btn_cancelar.pack(side='right')

    def _carregar_imagem_capa(self, caminho_imagem):
        """ Carrega e exibe a imagem da capa do livro. Se o caminho for None ou inválido, exibe um placeholder. """
        try:
            if not caminho_imagem: raise FileNotFoundError
            img = Image.open(caminho_imagem).resize((150, 225), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.label_capa.config(image=photo)
            self.label_capa.image = photo
        except (FileNotFoundError, AttributeError):
            img_placeholder = Image.new('RGB', (150, 225), color = '#cccccc')
            photo_placeholder = ImageTk.PhotoImage(img_placeholder)
            self.label_capa.config(image=photo_placeholder)
            self.label_capa.image = photo_placeholder

    def _selecionar_capa(self):
        """ Abre uma janelinha para selecionar a imagem da capa do livro. """
        filepath = filedialog.askopenfilename(
            title="Selecione uma capa para o livro",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filepath:
            self.caminho_capa_selecionada = filepath
            self._carregar_imagem_capa(filepath)

    def _cadastrar_livro(self):
        """ Valida os dados e pede ao controller para adicionar o novo livro. """
        titulo = self.titulo_var.get().strip()
        autor = self.autor_var.get().strip()
        genero = self.genero_var.get().strip()
        ano = self.ano_var.get().strip()
        
        if not all([titulo, autor, genero, ano, self.caminho_capa_selecionada]):
            messagebox.showerror("Erro de Validação", "Todos os campos, incluindo a capa, são obrigatórios!")
            return
        
        if not ano.isdigit() or not len(ano) == 4:
            messagebox.showerror("Erro de Validação", "O ano deve ser um número com 4 dígitos.")
            return

        dados_novo_livro = {
            'titulo': titulo,
            'autor': autor,
            'genero': genero,
            'ano': int(ano),
            'status_nome': self.status_var.get(),
            'caminho_imagem_temporario': self.caminho_capa_selecionada
        }


        self.controller.adicionar_novo_livro(dados_novo_livro)