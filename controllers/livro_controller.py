from datetime import datetime


class LivroController:
    def __init__(self, models, view):
        self.models = models
        self.view = view

    def show_page(self, page_name):
        """ Mostra a página especificada. """
        self.view.show_page(page_name)
        
    def show_edit_page(self, livro_id):
        """ Mostra a página de edição para o livro especificado. """
        self.view.show_page("EditLivroPage", livro_id)

    def get_livro_by_id(self, livro_id):
        """ Retorna o livro com o ID especificado. """
        return self.models['livro'].get_livro_by_id(livro_id)

    def get_livros(self, filtro="Todos"):
        """ Retorna a lista de livros que pode ser filtrada por status. """
        todos_livros = self.models['livro'].get_all()
        if filtro == "Todos":
            return todos_livros
        return [livro for livro in todos_livros if livro.get_status() and livro.get_status().get_nome() == filtro]

    def adicionar_novo_livro(self, dados):
        """ Adiciona um novo livro com os dados fornecidos. """
        autor = self.models['autor'].find_or_create_by_name(dados['autor'])
        genero = self.models['genero'].find_or_create_by_name(dados['genero'])
        status = self.models['status'].get_by_name(dados['status_nome'])
        
        dados_completos = dados.copy()
        dados_completos['autor'] = autor
        dados_completos['genero'] = genero
        dados_completos['status'] = status
        
        self.models['livro'].adicionar_livro(dados_completos)
        self.show_page("EstantePage")

    def buscar_e_salvar_capa(self, titulo):
        return self.models['livro'].buscar_e_salvar_capa(titulo)

    def atualizar_livro(self, livro_id, dados):
        """ Atualiza o livro com o ID especificado usando os dados fornecidos. """
        autor = self.models['autor'].find_or_create_by_name(dados['autor'])
        genero = self.models['genero'].find_or_create_by_name(dados['genero'])
        status = self.models['status'].get_by_name(dados['status_nome'])
        
        dados_completos = dados.copy()
        dados_completos['autor'] = autor
        dados_completos['genero'] = genero
        dados_completos['status'] = status
        
        self.models['livro'].atualizar_livro(livro_id, dados_completos)

    def mudar_status(self, livro_id, novo_status_nome):
        """ Muda o status do livro com o ID especificado. """
        novo_status = self.models['status'].get_by_name(novo_status_nome)
        if novo_status:
            self.models['livro'].mudar_status(livro_id, novo_status)
            self.view.pages["EstantePage"].filtrar_lista()

    def excluir_livro(self, livro_id):
        """ Exclui o livro com o ID especificado. """
        self.models['livro'].excluir_livro(livro_id)
        self.show_page("EstantePage")


    def get_meta_anual(self):
            """ Pede a meta anual ao StatsModel. """
            return self.models['stats'].get_meta_anual()

    def salvar_meta_anual(self, meta):
        """ Salva uma nova meta anual. """
        self.models['stats'].salvar_meta_anual(meta)

    def get_dados_grafico_barras(self):
        """ Pede os dados de livros lidos por mês para o ano atual. """
        ano_atual = datetime.now().year
        return self.models['livro'].get_livros_lidos_por_mes(ano_atual)

    def get_dados_grafico_pizza(self):
        """ Retorna o total de livros lidos e a meta para o ano atual. """
        ano_atual = datetime.now().year
        total_lidos = self.models['livro'].get_total_lidos_ano(ano_atual)
        meta = self.models['stats'].get_meta_anual()
        return total_lidos, meta