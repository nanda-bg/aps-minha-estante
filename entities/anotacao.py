class Anotacao:
    def __init__(self, id, livro_id, texto, data_criacao):
        self.__id = id
        self.__livro_id = livro_id
        self.__texto = texto
        self.__data_criacao = data_criacao

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_livro_id(self):
        return self.__livro_id

    def set_livro_id(self, value):
        self.__livro_id = value

    def get_texto(self):
        return self.__texto

    def set_texto(self, value):
        self.__texto = value

    def get_data_criacao(self):
        return self.__data_criacao

    def set_data_criacao(self, value):
        self.__data_criacao = value

    def to_dict(self):
        """ Converte a instância de Anotacao em um dicionário para facilitar na hora de salvar em JSON. """
        return {
            "id": self.get_id(),
            "livro_id": self.get_livro_id(),
            "texto": self.get_texto(),
            "data_criacao": self.get_data_criacao()
        }
