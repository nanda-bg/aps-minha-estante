import os

DATA_DIR = 'data'
LIVROS_JSON_PATH = os.path.join(DATA_DIR, 'livros.json')
AUTORES_JSON_PATH = os.path.join(DATA_DIR, 'autores.json')
GENEROS_JSON_PATH = os.path.join(DATA_DIR, 'generos.json')
STATUS_JSON_PATH = os.path.join(DATA_DIR, 'status.json')
STATS_JSON_PATH = os.path.join(DATA_DIR, 'stats.json')
ANOTACOES_JSON_PATH = os.path.join(DATA_DIR, 'anotacoes.json')
AVALIACOES_JSON_PATH = os.path.join(DATA_DIR, 'avaliacoes.json')
IMAGES_DIR = 'images'

STATUS_MAP = {
    1: "Quero Ler",
    2: "Lendo",
    3: "Lido"
}
STATUS_NAME_TO_ID = {name: id for id, name in STATUS_MAP.items()}
STATUS_OPCOES = list(STATUS_MAP.values())

STYLE_CONFIG = {
    "BG_COLOR": "#F5F5DC",
    "COMPONENT_BG": "#FDF5E6",
    "HEADER_BG": "#F0EAD6",
    "FG_COLOR": "#704214",
    "ACCENT_COLOR": "#556B2F",
    "DELETE_COLOR": "#A83232",
    "FONT_TITLE": ("Georgia", 20, "bold"),
    "FONT_HEADING": ("Georgia", 11, "bold"),
    "FONT_NORMAL": ("Georgia", 10),
    "FONT_CARD_TITLE": ("Georgia", 11, "bold"),
}