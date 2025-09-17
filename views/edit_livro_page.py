import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import shutil
from .base_page import BasePage
from config import STYLE_CONFIG, IMAGES_DIR, STATUS_OPCOES, STATUS_MAP

class EditLivroPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.livro_id = None
        self.novo_caminho_capa = None

        self.titulo_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        self.genero_var = tk.StringVar()
        self.ano_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._create_widgets()

    def on_show(self, livro_id):
        """
        Chamado quando a página é exibida.
        Carrega os dados do livro selecionado nos campos do formulário.
        """
        self.livro_id = livro_id
        self.novo_caminho_capa = None
        livro = self.controller.get_livro_by_id(self.livro_id)

        if livro:
            self.titulo_var.set(livro.get('titulo', ''))
            self.autor_var.set(livro.get('autor', ''))
            self.genero_var.set(livro.get('genero', ''))
            self.ano_var.set(str(livro.get('ano', '')))
            
            status_id = livro.get('status_id', 1)
            self.status_var.set(STATUS_MAP.get(status_id))
            
            self._carregar_imagem_capa(livro.get('caminho_imagem', ''))

    def _create_widgets(self):
        """ Cria os widgets da página de edição de livro. """
        main_frame = ttk.Frame(self, padding=(20, 20))
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_columnconfigure(1, weight=1)

        frame_capa = ttk.Frame(main_frame, padding=(0, 0, 20, 0))
        frame_capa.grid(row=0, column=0, sticky='nw', rowspan=2)

        self.label_capa = ttk.Label(frame_capa)
        self.label_capa.pack(pady=(0, 10))

        btn_alterar_capa = ttk.Button(frame_capa, text="Alterar Capa", command=self._selecionar_nova_capa)
        btn_alterar_capa.pack(fill='x')

        frame_detalhes = ttk.Frame(main_frame)
        frame_detalhes.grid(row=0, column=1, sticky='nsew')
        frame_detalhes.grid_columnconfigure(1, weight=1)

        ttk.Label(frame_detalhes, text="Título:").grid(row=0, column=0, sticky='w', pady=5)
        entry_titulo = ttk.Entry(frame_detalhes, textvariable=self.titulo_var, font=STYLE_CONFIG['FONT_NORMAL'])
        entry_titulo.grid(row=0, column=1, sticky='ew', pady=5)

        ttk.Label(frame_detalhes, text="Autor:").grid(row=1, column=0, sticky='w', pady=5)
        entry_autor = ttk.Entry(frame_detalhes, textvariable=self.autor_var, font=STYLE_CONFIG['FONT_NORMAL'])
        entry_autor.grid(row=1, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame_detalhes, text="Gênero:").grid(row=2, column=0, sticky='w', pady=5)
        entry_genero = ttk.Entry(frame_detalhes, textvariable=self.genero_var, font=STYLE_CONFIG['FONT_NORMAL'])
        entry_genero.grid(row=2, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame_detalhes, text="Ano:").grid(row=3, column=0, sticky='w', pady=5)
        entry_ano = ttk.Entry(frame_detalhes, textvariable=self.ano_var, font=STYLE_CONFIG['FONT_NORMAL'])
        entry_ano.grid(row=3, column=1, sticky='ew', pady=5)

        ttk.Label(frame_detalhes, text="Status:").grid(row=4, column=0, sticky='w', pady=5)
        combo_status = ttk.Combobox(frame_detalhes, textvariable=self.status_var, values=STATUS_OPCOES, state='readonly', font=STYLE_CONFIG['FONT_NORMAL'])
        combo_status.grid(row=4, column=1, sticky='ew', pady=5)

        frame_botoes_container = ttk.Frame(main_frame)
        frame_botoes_container.grid(row=1, column=1, sticky='e', pady=(20, 0))

        frame_acoes_top = ttk.Frame(frame_botoes_container)
        frame_acoes_top.pack()

        btn_salvar = ttk.Button(frame_acoes_top, text="Salvar Alterações", command=self._salvar_alteracoes, style="Accent.TButton")
        btn_salvar.pack(side='right', padx=(10, 0))

        btn_voltar = ttk.Button(frame_acoes_top, text="Voltar", command=self._voltar_para_estante)
        btn_voltar.pack(side='right')

        btn_excluir = ttk.Button(frame_botoes_container, text="Excluir Livro", command=self._excluir_livro, style="Delete.TButton")
        btn_excluir.pack(pady=(10, 0))

    def _carregar_imagem_capa(self, caminho_imagem):
        """ Carrega e exibe a imagem da capa do livro. Se o caminho for None ou inválido, exibe um placeholder. """
        try:
            caminho_completo = os.path.join(IMAGES_DIR, os.path.basename(caminho_imagem))
            img = Image.open(caminho_completo).resize((150, 225), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.label_capa.config(image=photo)
            self.label_capa.image = photo
        except Exception:
            placeholder = tk.Canvas(self, width=150, height=225, bg="#cccccc", highlightthickness=0)
            placeholder.create_text(75, 112, text="Capa\nIndisponível", fill="white", font=STYLE_CONFIG["FONT_NORMAL"], justify="center")
            self.label_capa.config(image=placeholder)
            
            img_placeholder = Image.new('RGB', (150, 225), color = '#cccccc')
            photo_placeholder = ImageTk.PhotoImage(img_placeholder)
            self.label_capa.config(image=photo_placeholder)
            self.label_capa.image = photo_placeholder


    def _selecionar_nova_capa(self):
        """ Abre uma janelinha para selecionar uma nova imagem de capa para o livro. """
        filepath = filedialog.askopenfilename(
            title="Selecione uma nova capa",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if filepath:
            self.novo_caminho_capa = filepath
            self._carregar_imagem_capa(filepath)

    def _salvar_alteracoes(self):
        """ Pede ao controller para salvar as alterações do livro. """
        titulo = self.titulo_var.get().strip()
        autor = self.autor_var.get().strip()
        genero = self.genero_var.get().strip()
        ano = self.ano_var.get().strip()
        status_nome = self.status_var.get().strip()

        dados_atualizados = {
            'titulo': titulo,
            'autor': autor,
            'genero': genero,
            'ano': ano,
            'status_nome': status_nome
        }

        if not all([titulo, autor, genero, ano]):
            messagebox.showerror("Erro de Validação", "Todos os campos são obrigatórios!")
            return
        
        if not ano.isdigit() or not len(ano) == 4:
            messagebox.showerror("Erro de Validação", "O ano deve ser um número com 4 dígitos.")
            return
        
        if self.novo_caminho_capa:
            try:
                livro_atual = self.controller.get_livro_by_id(self.livro_id)
                caminho_antigo = livro_atual.get('caminho_imagem')
                if caminho_antigo:
                    caminho_completo_antigo = os.path.join(IMAGES_DIR, caminho_antigo)
                    if os.path.exists(caminho_completo_antigo):
                        os.remove(caminho_completo_antigo)
            except Exception as e:
                print(f"Erro ao tentar remover a capa antiga: {e}")

            _, extensao = os.path.splitext(self.novo_caminho_capa)
            novo_nome_arquivo = f"book-cover-{self.livro_id}{extensao}"
            caminho_destino = os.path.join(IMAGES_DIR, novo_nome_arquivo)

            shutil.copy(self.novo_caminho_capa, caminho_destino)
            
            dados_atualizados['caminho_imagem'] = novo_nome_arquivo

        self.controller.atualizar_livro(self.livro_id, dados_atualizados)
        self._voltar_para_estante()

    def _voltar_para_estante(self):
        """ Volta para a página da estante. """
        self.controller.show_page("EstantePage")

    def _excluir_livro(self):
        """ Pede confirmação e, se positivo, solicita a exclusão do livro. """
        titulo_livro = self.titulo_var.get()
        confirmado = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o livro '{titulo_livro}'?\n\nEsta ação não pode ser desfeita.",
            icon='warning'
        )
        if confirmado:
            self.controller.excluir_livro(self.livro_id)