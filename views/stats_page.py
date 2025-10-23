import tkinter as tk
from tkinter import ttk, messagebox
from .base_page import BasePage
from config import STYLE_CONFIG

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge
import matplotlib.ticker

class StatsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.meta_var = tk.StringVar()
        self.canvas_pizza = None
        self.canvas_barras = None
        self.debounce_timer = None
        self._create_widgets()
        self.bind("<Configure>", self._on_resize)

    def on_show(self):
        self._carregar_meta()
        self.after(100, self._desenhar_graficos)

    def _carregar_meta(self):
        meta = self.controller.get_meta_anual()
        self.meta_var.set(str(meta))

    def _salvar_meta(self):
        try:
            nova_meta = int(self.meta_var.get())
            if nova_meta <= 0:
                raise ValueError
            self.controller.salvar_meta_anual(nova_meta)
            messagebox.showinfo("Sucesso", "Sua meta de leitura foi atualizada!")
            self._desenhar_graficos()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido para a meta.")

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(3, weight=1) 

        ttk.Label(main_frame, text="Meta de Leitura atual", 
                  font=STYLE_CONFIG["FONT_HEADING"]).grid(row=0, column=0, columnspan=2, pady=(0, 5))

        meta_controls_frame = ttk.Frame(main_frame)
        meta_controls_frame.grid(row=1, column=0, columnspan=2, pady=(0, 25))

        ttk.Label(meta_controls_frame, text="Definir meta anual:").pack(side='left', padx=(0, 10))
        
        opcoes_meta = [str(i) for i in range(1, 101)]
        self.combo_meta = ttk.Spinbox(meta_controls_frame, textvariable=self.meta_var, values=opcoes_meta, width=5, wrap=True)
        self.combo_meta.pack(side='left', padx=10)

        btn_salvar_meta = ttk.Button(meta_controls_frame, text="Salvar Meta", command=self._salvar_meta, style="Accent.TButton")
        btn_salvar_meta.pack(side='left', padx=10)

        ttk.Label(main_frame, text="Livros Lidos vs. Meta", 
                  font=STYLE_CONFIG["FONT_HEADING"]).grid(row=2, column=0, pady=10)
        ttk.Label(main_frame, text="Livros Lidos por Mês", 
                  font=STYLE_CONFIG["FONT_HEADING"]).grid(row=2, column=1, pady=10)

        frame_pizza_container = ttk.Frame(main_frame)
        frame_pizza_container.grid(row=3, column=0, sticky='nsew', padx=10)

        self.frame_pizza = ttk.Frame(frame_pizza_container)
        self.frame_pizza.pack(fill='both', expand=True)

        self.label_pizza_info = ttk.Label(frame_pizza_container, text="", font=STYLE_CONFIG["FONT_NORMAL"], anchor='center')
        self.label_pizza_info.pack(side='bottom', pady=10)
        
        self.frame_barras = ttk.Frame(main_frame)
        self.frame_barras.grid(row=3, column=1, sticky='nsew', padx=10)

    def _on_resize(self, event=None):
        if self.debounce_timer:
            self.after_cancel(self.debounce_timer)
        self.debounce_timer = self.after(250, self._desenhar_graficos)

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _desenhar_graficos(self, event=None):
        if self.frame_pizza.winfo_width() < 10 or self.frame_barras.winfo_width() < 10:
             self.after(100, self._desenhar_graficos)
             return
             
        self._desenhar_grafico_pizza()
        self._desenhar_grafico_barras()
        
    def _desenhar_grafico_pizza(self):
        self._clear_frame(self.frame_pizza)
        
        total_lidos, meta = self.controller.get_dados_grafico_pizza()
        
        meta_calc = max(1, meta)
        percentual = (total_lidos / meta_calc) * 100
        restante = max(0, meta - total_lidos)

        valores = [total_lidos, restante]
        if total_lidos == 0 and restante == 0:
             valores = [1]
             cores = ['#CCCCCC']
        else:
             cores = [STYLE_CONFIG["ACCENT_COLOR"], '#E0E0E0']

        fig = Figure(facecolor=STYLE_CONFIG["BG_COLOR"])
        ax = fig.add_subplot(111)

        ax.pie(valores, colors=cores, startangle=90, counterclock=False, 
               wedgeprops={'width': 0.4, 'edgecolor': STYLE_CONFIG["BG_COLOR"]})
        
        ax.text(0, 0, f"{percentual:.0f}%", 
                ha='center', va='center', 
                fontweight='bold', 
                fontsize=16, 
                color=STYLE_CONFIG["FG_COLOR"])

        fig.tight_layout()

        self.canvas_pizza = FigureCanvasTkAgg(fig, master=self.frame_pizza)
        self.canvas_pizza.draw()
        self.canvas_pizza.get_tk_widget().pack(fill='both', expand=True)

        self.label_pizza_info.config(text=f"{total_lidos} de {meta} livros lidos")

    def _desenhar_grafico_barras(self):
        self._clear_frame(self.frame_barras)
        
        dados_meses = self.controller.get_dados_grafico_barras()
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

        fig = Figure(facecolor=STYLE_CONFIG["BG_COLOR"])
        ax = fig.add_subplot(111)
        
        ax.set_facecolor(STYLE_CONFIG["BG_COLOR"])
        ax.bar(meses_nomes, dados_meses, color=STYLE_CONFIG["ACCENT_COLOR"])
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(STYLE_CONFIG["FG_COLOR"])
        ax.spines['bottom'].set_color(STYLE_CONFIG["FG_COLOR"])

        ax.tick_params(colors=STYLE_CONFIG["FG_COLOR"], which='both')
        ax.yaxis.label.set_color(STYLE_CONFIG["FG_COLOR"])
        ax.xaxis.label.set_color(STYLE_CONFIG["FG_COLOR"])
        
        max_val = max(dados_meses) if dados_meses else 0
        ax.set_yticks(range(0, max(1, max_val + 2)))
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

        fig.tight_layout()

        self.canvas_barras = FigureCanvasTkAgg(fig, master=self.frame_barras)
        self.canvas_barras.draw()
        self.canvas_barras.get_tk_widget().pack(fill='both', expand=True)