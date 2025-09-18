class Autor:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def to_dict(self):
        """ Converte a instância de Autor em um dicionário para facilitar na hora de salvar em JSON. """
        return {"id": self.id, "nome": self.nome}