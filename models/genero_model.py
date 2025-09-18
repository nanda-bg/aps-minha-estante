from .base_model import BaseModel
from entities.genero import Genero
from config import GENEROS_JSON_PATH

class GeneroModel(BaseModel):
    def __init__(self):
        super().__init__(GENEROS_JSON_PATH, Genero)

    def find_or_create_by_name(self, name):
        """ Procura um gênero pelo nome. Se não existir, cria um novo gênero. """
        name = name.strip()
        for genero in self.data:
            if genero.nome.lower() == name.lower():
                return genero
        
        new_id = self._get_next_id()
        new_genero = Genero(id=new_id, nome=name)
        self.data.append(new_genero)
        self._save()
        return new_genero