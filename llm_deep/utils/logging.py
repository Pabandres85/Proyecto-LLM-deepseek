"""
Funciones para el registro de logs.
"""
import os
import csv
from datetime import datetime
from utils.config import LOG_FILE_PATH

def log_interaction(user_query, bot_response, company, feedback, timestamp=None):
    """
    Registra una interacción en el archivo CSV de logs.
    
    Args:
        user_query (str): Consulta del usuario
        bot_response (str): Respuesta del chatbot
        company (str): Nombre de la empresa
        feedback (str): Feedback del usuario
        timestamp (str, optional): Marca de tiempo. Si es None, se genera automáticamente.
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    log_exists = os.path.exists(LOG_FILE_PATH)
    
    with open(LOG_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"])
        writer.writerow([timestamp, company, user_query, bot_response, feedback])