"""
Configuraciones globales para la aplicación.
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "log")
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Asegurar que existan directorios necesarios
os.makedirs(LOG_DIR, exist_ok=True)

# Archivos
LOG_FILE_PATH = os.path.join(LOG_DIR, "chat_log.csv")
COMPANY_DATA_PATH = os.path.join(DATA_DIR, "company_data.json")

# Configuración de API
API_URL = "http://172.29.64.1:1234/v1/chat/completions"
API_MODEL = "deepspeek-r1-distill-qwen-7b"
API_MAX_TOKENS = 1000

# UI
PAGE_TITLE = "Chat UAO - Especialización IA"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# Paths de imágenes
UAO_LOGO_PATH = os.path.join(IMAGES_DIR, "UAO-LOGO-NUEVO.png")
CHATBOT_IMAGE_PATH = os.path.join(IMAGES_DIR, "CHATBOT.png")