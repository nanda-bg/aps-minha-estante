from .base_model import BaseModel
from entities.avaliacao import Avaliacao
from config import AVALIACOES_JSON_PATH

class AvaliacaoModel(BaseModel):
    def __init__(self):
        super().__init__(AVALIACOES_JSON_PATH, Avaliacao)

    def get_avaliacao_por_livro(self, livro_id):
        """ Retorna a avaliação de um livro específico (se existir). """
        for avaliacao in self.data:
            if avaliacao.get_livro_id() == livro_id:
                return avaliacao
        return None

    def adicionar_ou_atualizar_avaliacao(self, livro_id, nota):
        """ Adiciona ou atualiza a avaliação de um livro. """
        avaliacao_existente = self.get_avaliacao_por_livro(livro_id)
        
        if avaliacao_existente:
            avaliacao_existente.set_nota(nota)
        else:
            novo_id = self._get_next_id()
            nova_avaliacao = Avaliacao(
                id=novo_id,
                livro_id=livro_id,
                nota=nota
            )
            self.data.append(nova_avaliacao)
        
        self._save()
        return True

    def excluir_avaliacao(self, livro_id):
        """ Exclui a avaliação de um livro. """
        self.data = [avaliacao for avaliacao in self.data if avaliacao.get_livro_id() != livro_id]
        self._save()

    def excluir_avaliacao_por_livro(self, livro_id):
        """ Exclui a avaliação de um livro específico. """
        self.excluir_avaliacao(livro_id)
