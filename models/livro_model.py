import json
import os
import time
import shutil 
from datetime import datetime
from config import LIVROS_JSON_PATH, IMAGES_DIR, STATUS_MAP, STATUS_NAME_TO_ID

class LivroModel:
    def __init__(self):
        self.livros = self._carregar_livros()

    def _carregar_livros(self):
        """ Carrega livros e migra dados antigos (status string para status_id). """
        try:
            with open(LIVROS_JSON_PATH, 'r', encoding='utf-8') as f:
                livros_carregados = json.load(f)
            
            for livro in livros_carregados:
                if 'status' in livro and isinstance(livro['status'], str):
                    livro['status_id'] = STATUS_NAME_TO_ID.get(livro['status'].title(), 1)
                    del livro['status']
                if 'data_leitura' not in livro:
                    livro['data_leitura'] = None
            
            self.salvar_livros_no_arquivo(livros_carregados)
            return livros_carregados

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_livros(self):
        """Salva o estado atual dos livros."""
        self.salvar_livros_no_arquivo(self.livros)

    def salvar_livros_no_arquivo(self, lista_livros):
        """Salva uma lista de livros específica no arquivo JSON."""
        os.makedirs(os.path.dirname(LIVROS_JSON_PATH), exist_ok=True)
        with open(LIVROS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista_livros, f, indent=2, ensure_ascii=False)

    def get_livros_filtrados(self, filtro_nome_status="Todos"):
        """ Retorna livros filtrando pelo nome do status. """
        if filtro_nome_status == "Todos":
            return self.livros
        
        filtro_id = STATUS_NAME_TO_ID.get(filtro_nome_status)
        if filtro_id is None:
            return []
            
        return [livro for livro in self.livros if livro.get('status_id') == filtro_id]

    def mudar_status(self, livro_id, novo_status_nome):
        """ Atualiza o status de um livro e o campo data_leitura. """
        novo_status_id = STATUS_NAME_TO_ID.get(novo_status_nome)
        if novo_status_id is None: return

        for livro in self.livros:
            if livro.get('id') == livro_id:
                livro['status_id'] = novo_status_id
                if novo_status_id == 3:
                    livro['data_leitura'] = datetime.now().isoformat()
                else:
                    livro['data_leitura'] = None
                break
        self.salvar_livros()
            
    def atualizar_livro(self, livro_id, dados_atualizados):
        """ Atualiza os dados de um livro, incluindo a lógica de status. """
        nome_status = dados_atualizados.pop('status_nome', None)
        if nome_status:
            dados_atualizados['status_id'] = STATUS_NAME_TO_ID.get(nome_status)

        for livro in self.livros:
            if livro.get('id') == livro_id:
                livro.update(dados_atualizados)
                if 'status_id' in dados_atualizados:
                    if dados_atualizados['status_id'] == 3:
                        livro['data_leitura'] = datetime.now().isoformat()
                    else:
                        livro['data_leitura'] = None
                break
        self.salvar_livros()

    def get_livro_by_id(self, livro_id):
        """Retorna um livro específico pelo seu ID."""
        for livro in self.livros:
            if livro.get('id') == livro_id:
                return livro
        return None

    def adicionar_livro(self, dados_livro):
        """ Adiciona um novo livro. """
        novo_id = int(time.time())
        
        status_id = STATUS_NAME_TO_ID.get(dados_livro['status_nome'], 1)

        novo_livro = {
            "id": novo_id,
            "titulo": dados_livro['titulo'],
            "autor": dados_livro['autor'],
            "genero": dados_livro['genero'],
            "ano": dados_livro['ano'],
            "status_id": status_id,
            "caminho_imagem": "",
            "data_leitura": None
        }
        
        if status_id == 3:
            novo_livro['data_leitura'] = datetime.now().isoformat()

        caminho_temporario = dados_livro.get('caminho_imagem_temporario')
        if caminho_temporario:
            _, extensao = os.path.splitext(caminho_temporario)
            nome_final_imagem = f"book-cover-{novo_id}{extensao}"
            caminho_destino = os.path.join(IMAGES_DIR, nome_final_imagem)
            shutil.copy(caminho_temporario, caminho_destino)
            novo_livro['caminho_imagem'] = nome_final_imagem

        self.livros.append(novo_livro)
        self.salvar_livros()

    def excluir_livro(self, livro_id):
        """ Encontra um livro pelo ID, exclui sua imagem e o registro. """
        livro_para_excluir = self.get_livro_by_id(livro_id)

        if not livro_para_excluir:
            return

        caminho_imagem = livro_para_excluir.get('caminho_imagem')
        if caminho_imagem:
            try:
                caminho_completo = os.path.join(IMAGES_DIR, caminho_imagem)
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
            except Exception as e:
                print(f"Erro ao excluir a imagem da capa: {e}")

        self.livros = [livro for livro in self.livros if livro.get('id') != livro_id]
        
        self.salvar_livros()    