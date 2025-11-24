class Avaliacao:
    def __init__(self, id, livro_id, nota):
        self.__id = id
        self.__livro_id = livro_id
        self.__nota = nota

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_livro_id(self):
        return self.__livro_id

    def set_livro_id(self, value):
        self.__livro_id = value

    def get_nota(self):
        return self.__nota

    def set_nota(self, value):
        self.__nota = value

    def to_dict(self):
        """ Converte a instância de Avaliacao em um dicionário para facilitar na hora de salvar em JSON. """
        return {
            "id": self.get_id(),
            "livro_id": self.get_livro_id(),
            "nota": self.get_nota()
        }
