class LivroController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_page(self, page_name):
        """Pede para a main view mostrar uma página específica."""
        self.view.show_page(page_name)
        
    def show_edit_page(self, livro_id):
        """Pede para a main view mostrar a página de edição, passando o ID do livro."""
        self.view.show_page("EditLivroPage", livro_id)

    def get_livro_by_id(self, livro_id):
        """Pede a um livro específico do Model pelo ID."""
        return self.model.get_livro_by_id(livro_id)

    def atualizar_livro(self, livro_id, dados):
        """Passa os dados atualizados para o Model salvar."""
        self.model.atualizar_livro(livro_id, dados)    

    def mudar_status(self, livro_id, novo_status):
        """
        Recebe a requisição da view para mudar um status,
        chama o model e depois pede para a view se atualizar.
        """
        self.model.mudar_status(livro_id, novo_status)

        self.view.pages["EstantePage"].filtrar_lista()

    def get_livros(self, filtro="Todos"):
        """Busca os livros do Model para a view."""
        return self.model.get_livros_filtrados(filtro)

    def get_all_livros(self):
        """Busca todos os livros, sem filtro."""
        return self.model.livros

    def adicionar_novo_livro(self, dados):
        """Passa os dados de um novo livro para o Model e depois volta para a estante."""
        self.model.adicionar_livro(dados)
        self.show_page("EstantePage")    

    def excluir_livro(self, livro_id):
        """Pede ao Model para excluir um livro e depois retorna para a estante."""
        self.model.excluir_livro(livro_id)
        self.show_page("EstantePage")    