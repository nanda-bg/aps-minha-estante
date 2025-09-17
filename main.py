import os
from models.livro_model import LivroModel
from views.main_view import MainView
from controllers.livro_controller import LivroController

class App:
    def __init__(self):
        model = LivroModel()
        
        view = MainView()
        
        controller = LivroController(model, view)

        view.set_controller(controller)
        
        view.start()

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    app = App()