class Autor:
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_nome(self):
        return self.__nome

    def set_nome(self, value):
        self.__nome = value

    def to_dict(self):
        """ Converte a instância de Autor em um dicionário para facilitar na hora de salvar em JSON. """
        return {"id": self.get_id(), "nome": self.get_nome()}