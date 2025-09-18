class Genero:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    def to_dict(self):
        """ Converte a instância de Genero em um dicionário para facilitar na hora de salvar em JSON. """
        return {"id": self.id, "nome": self.nome}