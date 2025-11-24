import os
from models.livro_model import LivroModel
from models.autor_model import AutorModel
from models.genero_model import GeneroModel
from models.status_model import StatusModel
from models.stats_model import StatsModel
from models.anotacao_model import AnotacaoModel
from models.avaliacao_model import AvaliacaoModel
from views.main_view import MainView
from controllers.livro_controller import LivroController

class App:
    def __init__(self):
        autor_model = AutorModel()
        genero_model = GeneroModel()
        status_model = StatusModel()
        livro_model = LivroModel(autor_model, genero_model, status_model)
        stats_model = StatsModel()
        anotacao_model = AnotacaoModel()
        avaliacao_model = AvaliacaoModel()

        models = {
            "livro": livro_model,
            "autor": autor_model,
            "genero": genero_model,
            "status": status_model,
            "stats": stats_model,
            "anotacao": anotacao_model,
            "avaliacao": avaliacao_model
        }
        
        view = MainView()
        
        controller = LivroController(models, view)

        view.set_controller(controller)
        
        view.start()

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    app = App()