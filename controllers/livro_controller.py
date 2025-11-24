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
            livro = self.get_livro_by_id(livro_id)
            if livro and livro.get_status() and livro.get_status().get_id() == 3 and novo_status.get_id() != 3:
                self.models['anotacao'].excluir_anotacoes_por_livro(livro_id)
                self.models['avaliacao'].excluir_avaliacao_por_livro(livro_id)
            
            self.models['livro'].mudar_status(livro_id, novo_status)
            self.view.pages["EstantePage"].filtrar_lista()

    def excluir_livro(self, livro_id):
        """ Exclui o livro com o ID especificado. """

        self.models['anotacao'].excluir_anotacoes_por_livro(livro_id)
        self.models['avaliacao'].excluir_avaliacao_por_livro(livro_id)
        
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

    def get_anotacoes_por_livro(self, livro_id):
        """ Retorna todas as anotações de um livro. """
        return self.models['anotacao'].get_anotacoes_por_livro(livro_id)

    def adicionar_anotacao(self, livro_id, texto):
        """ Adiciona uma nova anotação para um livro. """
        livro = self.get_livro_by_id(livro_id)
        if livro and livro.get_status() and livro.get_status().get_id() == 3:
            return self.models['anotacao'].adicionar_anotacao(livro_id, texto)
        return None

    def atualizar_anotacao(self, anotacao_id, novo_texto):
        """ Atualiza o texto de uma anotação. """
        return self.models['anotacao'].atualizar_anotacao(anotacao_id, novo_texto)

    def excluir_anotacao(self, anotacao_id):
        """ Exclui uma anotação. """
        self.models['anotacao'].excluir_anotacao(anotacao_id)

    def get_avaliacao_por_livro(self, livro_id):
        """ Retorna a avaliação de um livro. """
        return self.models['avaliacao'].get_avaliacao_por_livro(livro_id)

    def adicionar_ou_atualizar_avaliacao(self, livro_id, nota):
        """ Adiciona ou atualiza a avaliação de um livro. """
        livro = self.get_livro_by_id(livro_id)
        if livro and livro.get_status() and livro.get_status().get_id() == 3:
            return self.models['avaliacao'].adicionar_ou_atualizar_avaliacao(livro_id, nota)
        return False

    def excluir_avaliacao(self, livro_id):
        """ Exclui a avaliação de um livro. """
        self.models['avaliacao'].excluir_avaliacao(livro_id)
    
    def show_anotacoes_page(self, livro_id):
        """ Mostra a página de anotações para o livro especificado. """
        self.view.show_page("AnotacoesPage", livro_id)
    
    def get_recomendacoes(self, livro_id, max_recomendacoes=5):
        """ Retorna livros recomendados com base no gênero do livro atual. """
        livro_atual = self.get_livro_by_id(livro_id)
        if not livro_atual:
            return []
        
        genero_atual = livro_atual.get_genero()
        todos_livros = self.models['livro'].get_all()
        
        recomendacoes = [
            livro for livro in todos_livros 
            if livro.get_genero() and livro.get_genero().get_id() == genero_atual.get_id() 
            and livro.get_id() != livro_id
        ]
        
        return recomendacoes[:max_recomendacoes]