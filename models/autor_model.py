from .base_model import BaseModel
from entities.autor import Autor
from config import AUTORES_JSON_PATH

class AutorModel(BaseModel):
    def __init__(self):
        super().__init__(AUTORES_JSON_PATH, Autor)

    def find_or_create_by_name(self, name):
        """ Procura um autor pelo nome. Se não existir, cria um novo autor. """
        name = name.strip()
        for autor in self.data:
            if autor.nome.lower() == name.lower():
                return autor
        
        new_id = self._get_next_id()
        new_autor = Autor(id=new_id, nome=name)
        self.data.append(new_autor)
        self._save()
        return new_autor