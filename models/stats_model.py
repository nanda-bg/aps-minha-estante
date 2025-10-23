import json
import os
from config import STATS_JSON_PATH

class StatsModel:
    def __init__(self):
        self.stats_data = self._load()

    def _load(self):
        """ Carrega a meta. """
        try:
            with open(STATS_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"meta_anual": 12}

    def save(self):
        """ Salva os dados da meta no JSON. """
        os.makedirs(os.path.dirname(STATS_JSON_PATH), exist_ok=True)
        with open(STATS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.stats_data, f, indent=2, ensure_ascii=False)

    def get_meta_anual(self):
        """ Retorna a meta de leitura anual. """
        return self.stats_data.get("meta_anual", 12)

    def salvar_meta_anual(self, meta):
        """ Salva uma nova meta de leitura anual. """
        try:
            self.stats_data["meta_anual"] = int(meta)
            self.save()
            return True
        except ValueError:
            return False