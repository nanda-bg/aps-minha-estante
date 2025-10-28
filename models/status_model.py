from .base_model import BaseModel
from entities.status import Status
from config import STATUS_JSON_PATH, STATUS_MAP

class StatusModel(BaseModel):
    def __init__(self):
        super().__init__(STATUS_JSON_PATH, Status)
        if not self.data:
            self._initialize_status()

    def _initialize_status(self):
        """ Inicializa os status padrão se o arquivo JSON estiver vazio. """
        for id, nome in STATUS_MAP.items():
            self.data.append(Status(id=id, nome=nome))
        self._save()

    def get_by_name(self, name):
        """ Retorna o status com o nome especificado, ou None se não encontrado. """
        for status in self.data:
            if status.get_nome().lower() == name.lower():
                return status
        return None