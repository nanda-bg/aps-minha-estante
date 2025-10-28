class Livro:
    def __init__(self, id, titulo, autor, genero, ano, status, caminho_imagem, data_leitura=None):
        self.__id = id
        self.__titulo = titulo
        self.__autor = autor
        self.__genero = genero
        self.__ano = ano
        self.__status = status
        self.__caminho_imagem = caminho_imagem
        self.__data_leitura = data_leitura

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_titulo(self):
        return self.__titulo

    def set_titulo(self, value):
        self.__titulo = value

    def get_autor(self):
        return self.__autor

    def set_autor(self, value):
        self.__autor = value

    def get_genero(self):
        return self.__genero

    def set_genero(self, value):
        self.__genero = value

    def get_ano(self):
        return self.__ano

    def set_ano(self, value):
        self.__ano = value

    def get_status(self):
        return self.__status

    def set_status(self, value):
        self.__status = value

    def get_caminho_imagem(self):
        return self.__caminho_imagem

    def set_caminho_imagem(self, value):
        self.__caminho_imagem = value

    def get_data_leitura(self):
        return self.__data_leitura

    def set_data_leitura(self, value):
        self.__data_leitura = value

    def to_dict(self):
        """ Converte a instância de Livro em um dicionário para facilitar na hora de salvar em JSON. """

        return {
            "id": self.get_id(),
            "titulo": self.get_titulo(),
            "autor_id": self.get_autor().get_id() if self.get_autor() else None,
            "genero_id": self.get_genero().get_id() if self.get_genero() else None,
            "ano": self.get_ano(),
            "status_id": self.get_status().get_id() if self.get_status() else None,
            "caminho_imagem": self.get_caminho_imagem(),
            "data_leitura": self.get_data_leitura()
        }