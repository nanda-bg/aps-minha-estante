import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from .base_page import BasePage
from config import STYLE_CONFIG, IMAGES_DIR
from PIL import Image, ImageTk

class AnotacoesPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.livro_id = None
        self.anotacao_selecionada = None
        self._create_widgets()

    def on_show(self, livro_id):
        """ Carrega as anotações do livro. """
        self.livro_id = livro_id
        self.anotacao_selecionada = None
        
        livro = self.controller.get_livro_by_id(self.livro_id)
        if livro:
            self.label_titulo_livro.config(text=livro.get_titulo())
            self._carregar_info_livro(livro)
        
        self._limpar_formulario()
        self._atualizar_lista_anotacoes()
        self._atualizar_avaliacao_display()

    def _create_widgets(self):
        """ Cria os widgets da página de anotações. """
        main_frame = ttk.Frame(self, padding=(20, 20))
        main_frame.pack(fill='both', expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        frame_capa = ttk.Frame(header_frame)
        frame_capa.grid(row=0, column=0, sticky='nw', padx=(0, 20))
        
        self.label_capa = ttk.Label(frame_capa)
        self.label_capa.pack()
        
        info_frame = ttk.Frame(header_frame)
        info_frame.grid(row=0, column=1, sticky='nsew')
        
        self.label_titulo_livro = ttk.Label(info_frame, text="", 
                                           font=STYLE_CONFIG["FONT_TITLE"])
        self.label_titulo_livro.pack(anchor='w', pady=(0, 5))
        
        self.label_autor = ttk.Label(info_frame, text="", 
                                     font=STYLE_CONFIG["FONT_NORMAL"])
        self.label_autor.pack(anchor='w', pady=(0, 15))
        
        avaliacao_label = ttk.Label(info_frame, text="Avaliação:", font=STYLE_CONFIG["FONT_HEADING"])
        avaliacao_label.pack(anchor='w', pady=(0, 5))
        
        avaliacao_frame = ttk.Frame(info_frame)
        avaliacao_frame.pack(fill='x', anchor='w', pady=(0, 10))
        
        frame_estrelas = ttk.Frame(avaliacao_frame)
        frame_estrelas.pack(anchor='w')
        
        self.avaliacao_var = tk.IntVar(value=0)
        self.estrelas_buttons = []
        
        for i in range(1, 6):
            btn = tk.Button(frame_estrelas, text="☆", font=("Georgia", 16), 
                          bd=0, bg=STYLE_CONFIG["COMPONENT_BG"], fg=STYLE_CONFIG["FG_COLOR"],
                          activebackground=STYLE_CONFIG["COMPONENT_BG"],
                          command=lambda nota=i: self._selecionar_avaliacao(nota))
            btn.pack(side='left', padx=2)
            self.estrelas_buttons.append(btn)
        
        btn_remover_avaliacao = ttk.Button(frame_estrelas, text="Remover", 
                                          command=self._remover_avaliacao)
        btn_remover_avaliacao.pack(side='left', padx=(10, 0))
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=3)
        
        left_column = ttk.Frame(content_frame)
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        left_column.grid_rowconfigure(0, weight=1)
        left_column.grid_columnconfigure(0, weight=1)
        
        lista_frame = ttk.LabelFrame(left_column, text="Minhas Anotações", padding=10)
        lista_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox_anotacoes = tk.Listbox(lista_frame, yscrollcommand=scrollbar.set,
                                            font=STYLE_CONFIG["FONT_NORMAL"],
                                            selectmode='single')
        self.listbox_anotacoes.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox_anotacoes.yview)
        
        self.listbox_anotacoes.bind('<<ListboxSelect>>', self._on_selecionar_anotacao)
        self.listbox_anotacoes.bind('<Configure>', self._ajustar_preview_anotacoes)
        
        btn_voltar = ttk.Button(left_column, text="Voltar", 
                               command=self._voltar_para_estante)
        btn_voltar.grid(row=1, column=0, sticky='w')
        
        form_frame = ttk.LabelFrame(content_frame, text="Adicionar/Editar Anotação", padding=10)
        form_frame.grid(row=0, column=1, sticky='nsew')
        
        self.text_anotacao = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, 
                                                       font=STYLE_CONFIG["FONT_NORMAL"],
                                                       height=15)
        self.text_anotacao.pack(fill='both', expand=True, pady=(0, 10))
        
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.pack(fill='x')
        
        btn_nova = ttk.Button(botoes_frame, text="Nova Anotação", 
                             command=self._limpar_formulario)
        btn_nova.pack(side='left', padx=(0, 5))
        
        btn_salvar = ttk.Button(botoes_frame, text="Salvar", 
                               command=self._salvar_anotacao, style="Accent.TButton")
        btn_salvar.pack(side='left', padx=5)
        
        btn_excluir = ttk.Button(botoes_frame, text="Excluir", 
                                command=self._excluir_anotacao, style="Delete.TButton")
        btn_excluir.pack(side='right')

    def _atualizar_lista_anotacoes(self):
        """ Atualiza a listbox com as anotações do livro. """

        self.listbox_anotacoes.config(state='normal')
        self.listbox_anotacoes.delete(0, tk.END)
        
        anotacoes = self.controller.get_anotacoes_por_livro(self.livro_id)
        
        if not anotacoes:
            self.listbox_anotacoes.insert(tk.END, "Nenhuma anotação encontrada")
            self.listbox_anotacoes.config(state='disabled')
        else:
            largura_listbox = self.listbox_anotacoes.winfo_width()
            char_width = 8 
            max_chars = (largura_listbox // char_width) - 20
            
            for anotacao in anotacoes:
                try:
                    data_obj = datetime.fromisoformat(anotacao.get_data_criacao())
                    data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
                except:
                    data_formatada = "Data desconhecida"
                
                texto_completo = anotacao.get_texto()
                texto_preview = texto_completo[:max_chars]
                if len(texto_completo) > max_chars:
                    texto_preview += "..."
                
                display_text = f"{data_formatada} - {texto_preview}"
                self.listbox_anotacoes.insert(tk.END, display_text)
    
    def _ajustar_preview_anotacoes(self, event=None):
        """ Recarrega as anotações quando o frame é redimensionado. """
        if hasattr(self, 'livro_id') and self.livro_id:
            self.after(100, self._atualizar_lista_anotacoes)

    def _on_selecionar_anotacao(self, event):
        """ Carrega a anotação selecionada no formulário. """
        selection = self.listbox_anotacoes.curselection()
        if not selection:
            return
        
        index = selection[0]
        anotacoes = self.controller.get_anotacoes_por_livro(self.livro_id)
        
        if index < len(anotacoes):
            self.anotacao_selecionada = anotacoes[index]
            self.text_anotacao.delete('1.0', tk.END)
            self.text_anotacao.insert('1.0', self.anotacao_selecionada.get_texto())

    def _limpar_formulario(self):
        """ Limpa o formulário para criar uma nova anotação. """
        self.anotacao_selecionada = None
        self.text_anotacao.delete('1.0', tk.END)
        self.listbox_anotacoes.selection_clear(0, tk.END)

    def _salvar_anotacao(self):
        """ Salva a anotação (nova ou editada). """
        texto = self.text_anotacao.get('1.0', tk.END).strip()
        
        if not texto:
            messagebox.showerror("Erro", "A anotação não pode estar vazia!")
            return
        
        if self.anotacao_selecionada:
            sucesso = self.controller.atualizar_anotacao(
                self.anotacao_selecionada.get_id(), texto
            )
            if sucesso:
                messagebox.showinfo("Sucesso", "Anotação atualizada com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao atualizar a anotação.")
        else:
            nova_anotacao = self.controller.adicionar_anotacao(self.livro_id, texto)
            if nova_anotacao:
                messagebox.showinfo("Sucesso", "Anotação adicionada com sucesso!")
            else:
                messagebox.showerror("Erro", "Apenas livros com status 'Lido' podem ter anotações.")
                return
        
        self._limpar_formulario()
        self._atualizar_lista_anotacoes()

    def _excluir_anotacao(self):
        """ Exclui a anotação selecionada. """
        if not self.anotacao_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma anotação para excluir.")
            return
        
        confirmado = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja excluir esta anotação?\n\nEsta ação não pode ser desfeita.",
            icon='warning'
        )
        
        if confirmado:
            self.controller.excluir_anotacao(self.anotacao_selecionada.get_id())
            messagebox.showinfo("Sucesso", "Anotação excluída com sucesso!")
            self._limpar_formulario()
            self._atualizar_lista_anotacoes()

    def _voltar_para_estante(self):
        """ Volta para a página da estante. """
        self.controller.show_page("EstantePage")
    
    def _abrir_edicao(self):
        """ Abre a página de edição do livro. """
        self.controller.show_edit_page(self.livro_id)
    
    def _carregar_info_livro(self, livro):
        """ Carrega as informações do livro no header. """

        self.label_autor.config(text=livro.get_autor().get_nome())
        
        try:
            caminho_img = os.path.join(IMAGES_DIR, os.path.basename(livro.get_caminho_imagem()))
            img = Image.open(caminho_img).resize((100, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.label_capa.config(image=photo)
            self.label_capa.image = photo
        except Exception:
            img_placeholder = Image.new('RGB', (100, 150), color='#cccccc')
            photo_placeholder = ImageTk.PhotoImage(img_placeholder)
            self.label_capa.config(image=photo_placeholder)
            self.label_capa.image = photo_placeholder
    
    def _selecionar_avaliacao(self, nota):
        """ Seleciona a avaliação e atualiza a exibição das estrelas. """
        livro = self.controller.get_livro_by_id(self.livro_id)
        if not livro or not livro.get_status() or livro.get_status().get_id() != 3:
            messagebox.showwarning("Aviso", "Apenas livros com status 'Lido' podem ser avaliados.")
            return
        
        self.avaliacao_var.set(nota)
        self._atualizar_estrelas_display(nota)

        self.controller.adicionar_ou_atualizar_avaliacao(self.livro_id, nota)
        messagebox.showinfo("Sucesso", f"Avaliação de {nota} estrela(s) salva!")
    
    def _atualizar_estrelas_display(self, nota):
        """ Atualiza a exibição visual das estrelas. """
        for i, btn in enumerate(self.estrelas_buttons, start=1):
            if i <= nota:
                btn.config(text="★", fg="#FFD700")
            else:
                btn.config(text="☆", fg=STYLE_CONFIG["FG_COLOR"])
    
    def _atualizar_avaliacao_display(self):
        """ Carrega e exibe a avaliação existente do livro. """
        avaliacao = self.controller.get_avaliacao_por_livro(self.livro_id)
        if avaliacao:
            nota = avaliacao.get_nota()
            self.avaliacao_var.set(nota)
            self._atualizar_estrelas_display(nota)
        else:
            self.avaliacao_var.set(0)
            self._atualizar_estrelas_display(0)
    
    def _remover_avaliacao(self):
        """ Remove a avaliação do livro. """
        confirmado = messagebox.askyesno(
            "Confirmar Remoção",
            "Tem certeza que deseja remover a avaliação deste livro?",
            icon='question'
        )
        if confirmado:
            self.controller.excluir_avaliacao(self.livro_id)
            self.avaliacao_var.set(0)
            self._atualizar_estrelas_display(0)
            messagebox.showinfo("Sucesso", "Avaliação removida com sucesso!")
