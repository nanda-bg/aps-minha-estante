import json
import os

class BaseModel:
    def __init__(self, filepath, entity_class):
        self.filepath = filepath
        self.entity_class = entity_class
        self.data = self._load()

    def _load(self):
        """ Carrega os dados do arquivo JSON e retorna uma lista de instâncias da entidade. """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                items = json.load(f)
                return [self.entity_class(**item) for item in items]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self):
        """ Salva a lista de instâncias da entidade no arquivo JSON. """
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([item.to_dict() for item in self.data], f, indent=2, ensure_ascii=False)

    def get_all(self):
        """ Retorna todos os itens carregados. """
        return self.data

    def get_by_id(self, item_id):
        """ Retorna o item com o ID especificado, ou None se não encontrado. """
        for item in self.data:
            if item.get_id() == item_id:
                return item
        return None

    def _get_next_id(self):
        """ Retorna o próximo ID disponível. """
        if not self.data:
            return 1
        return max(item.get_id() for item in self.data) + 1