from datetime import datetime
import time
from .base_model import BaseModel
from entities.anotacao import Anotacao
from config import ANOTACOES_JSON_PATH

class AnotacaoModel(BaseModel):
    def __init__(self):
        super().__init__(ANOTACOES_JSON_PATH, Anotacao)

    def get_anotacoes_por_livro(self, livro_id):
        """ Retorna todas as anotações de um livro específico. """
        return [anotacao for anotacao in self.data if anotacao.get_livro_id() == livro_id]

    def adicionar_anotacao(self, livro_id, texto):
        """ Adiciona uma nova anotação para um livro. """
        novo_id = int(time.time() * 1000)
        data_criacao = datetime.now().isoformat()
        
        nova_anotacao = Anotacao(
            id=novo_id,
            livro_id=livro_id,
            texto=texto,
            data_criacao=data_criacao
        )
        
        self.data.append(nova_anotacao)
        self._save()
        return nova_anotacao

    def atualizar_anotacao(self, anotacao_id, novo_texto):
        """ Atualiza o texto de uma anotação existente. """
        anotacao = self.get_by_id(anotacao_id)
        if anotacao:
            anotacao.set_texto(novo_texto)
            self._save()
            return True
        return False

    def excluir_anotacao(self, anotacao_id):
        """ Exclui uma anotação pelo ID. """
        self.data = [anotacao for anotacao in self.data if anotacao.get_id() != anotacao_id]
        self._save()

    def excluir_anotacoes_por_livro(self, livro_id):
        """ Exclui todas as anotações de um livro específico. """
        self.data = [anotacao for anotacao in self.data if anotacao.get_livro_id() != livro_id]
        self._save()
