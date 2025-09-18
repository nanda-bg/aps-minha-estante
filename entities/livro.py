class Livro:
    def __init__(self, id, titulo, autor, genero, ano, status, caminho_imagem, data_leitura=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.ano = ano
        self.status = status
        self.caminho_imagem = caminho_imagem
        self.data_leitura = data_leitura

    def to_dict(self):
        """ Converte a instância de Livro em um dicionário para facilitar na hora de salvar em JSON. """

        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor_id": self.autor.id,
            "genero_id": self.genero.id,
            "ano": self.ano,
            "status_id": self.status.id,
            "caminho_imagem": self.caminho_imagem,
            "data_leitura": self.data_leitura
        }