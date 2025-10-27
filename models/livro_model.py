import json
import os
import time
import shutil
from datetime import datetime
from config import LIVROS_JSON_PATH, IMAGES_DIR
from entities.livro import Livro
import requests

class LivroModel:
    def __init__(self, autor_model, genero_model, status_model):
        self.autor_model = autor_model
        self.genero_model = genero_model
        self.status_model = status_model
        self.livros = self._load()

    def _load(self):
        """ Carrega os livros do arquivo JSON, associando autores, gêneros e status. """
        try:
            with open(LIVROS_JSON_PATH, 'r', encoding='utf-8') as f:
                livros_data = json.load(f)
            
            livros_hydrated = []
            for data in livros_data:
                autor = self.autor_model.get_by_id(data['autor_id'])
                genero = self.genero_model.get_by_id(data['genero_id'])
                status = self.status_model.get_by_id(data['status_id'])
                if autor and genero and status:
                    livros_hydrated.append(Livro(
                        id=data['id'],
                        titulo=data['titulo'],
                        autor=autor,
                        genero=genero,
                        ano=data['ano'],
                        status=status,
                        caminho_imagem=data['caminho_imagem'],
                        data_leitura=data.get('data_leitura')
                    ))
            return livros_hydrated
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        """ Salva a lista de livros no arquivo JSON. """
        os.makedirs(os.path.dirname(LIVROS_JSON_PATH), exist_ok=True)
        with open(LIVROS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump([livro.to_dict() for livro in self.livros], f, indent=2, ensure_ascii=False)

    def get_all(self):
        """ Retorna todos os livros. """
        return self.livros

    def get_livro_by_id(self, livro_id):
        """ Retorna o livro com o ID especificado, ou None se não encontrado. """
        for livro in self.livros:
            if livro.id == livro_id:
                return livro
        return None

    def buscar_capa_online(self, titulo):
        """Busca a URL da capa do livro pelo título usando a API do Open Library."""
        url = f"https://openlibrary.org/search.json?title={titulo}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['docs']:
                    doc = data['docs'][0]
                    if 'cover_i' in doc:
                        cover_id = doc['cover_i']
                        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            return None
        except Exception as e:
            print(f"Erro ao buscar capa online: {e}")
            return None
    def buscar_e_salvar_capa(self, titulo):
        url_capa = self.buscar_capa_online(titulo)
        if url_capa:
            try:
                novo_id = int(time.time())
                os.makedirs(IMAGES_DIR, exist_ok=True)
                response = requests.get(url_capa, stream=True)
                if response.status_code == 200:
                    extensao = ".jpg"
                    nome_final_imagem = f"book-cover-{novo_id}{extensao}"
                    caminho_destino = os.path.join(IMAGES_DIR, nome_final_imagem)
                    with open(caminho_destino, 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    return nome_final_imagem
            except Exception as e:
                print(f"Erro ao baixar capa: {e}")
        return None

    def adicionar_livro(self, dados):
        novo_id = int(time.time())
        caminho_imagem_final = ""

        # Busca a capa online primeiro (se desejar, pode remover se já faz isso na interface)
        nome_imagem = self.buscar_e_salvar_capa(dados['titulo'])
        if nome_imagem:
            caminho_imagem_final = nome_imagem

        # Se o usuário enviou uma imagem manual, ela substitui a online
        caminho_temporario = dados.get('caminho_imagem_temporario')
        if caminho_temporario:
            _, extensao = os.path.splitext(caminho_temporario)
            nome_final_imagem = f"book-cover-{novo_id}{extensao}"
            caminho_destino = os.path.join(IMAGES_DIR, nome_final_imagem)
            shutil.copy(caminho_temporario, caminho_destino)
            caminho_imagem_final = nome_final_imagem

        data_leitura = datetime.now().isoformat() if dados['status'].id == 3 else None

        novo_livro = Livro(
            id=novo_id,
            titulo=dados['titulo'],
            autor=dados['autor'],
            genero=dados['genero'],
            ano=dados['ano'],
            status=dados['status'],
            caminho_imagem=caminho_imagem_final,
            data_leitura=data_leitura
        )
        self.livros.append(novo_livro)
        self.save()

    def atualizar_livro(self, livro_id, dados_atualizados):
        """ Atualiza o livro com o ID especificado usando os dados fornecidos. """
        livro = self.get_livro_by_id(livro_id)
        if not livro:
            return

        livro.titulo = dados_atualizados.get('titulo', livro.titulo)
        livro.ano = dados_atualizados.get('ano', livro.ano)
        livro.autor = dados_atualizados.get('autor', livro.autor)
        livro.genero = dados_atualizados.get('genero', livro.genero)
        
        if 'status' in dados_atualizados:
            livro.status = dados_atualizados['status']
            if livro.status.id == 3:
                livro.data_leitura = datetime.now().isoformat()
            else:
                livro.data_leitura = None

        if 'caminho_imagem' in dados_atualizados:
            livro.caminho_imagem = dados_atualizados['caminho_imagem']
            
        self.save()

    def mudar_status(self, livro_id, novo_status):
        """ Muda o status do livro com o ID especificado. """
        livro = self.get_livro_by_id(livro_id)
        if livro:
            livro.status = novo_status
            if novo_status.id == 3:
                livro.data_leitura = datetime.now().isoformat()
            else:
                livro.data_leitura = None
            self.save()

    def excluir_livro(self, livro_id):
        """ Exclui o livro com o ID especificado e remove a imagem da capa se existir. """
        livro_para_excluir = self.get_livro_by_id(livro_id)
        if not livro_para_excluir:
            return

        caminho_imagem = livro_para_excluir.caminho_imagem
        if caminho_imagem:
            try:
                caminho_completo = os.path.join(IMAGES_DIR, caminho_imagem)
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
            except Exception as e:
                print(f"Erro ao excluir a imagem da capa: {e}")

        self.livros = [livro for livro in self.livros if livro.id != livro_id]
        self.save()