"""
Servicio para integración con el modelo de lenguaje.
"""
import requests
import time
from utils.config import API_URL, API_MODEL, API_MAX_TOKENS

def get_chatbot_response(mensaje, selected_company, company_info, temperature=0.5):
    """
    Obtiene una respuesta del chatbot a través de la API.
    
    Args:
        mensaje (str): Mensaje del usuario
        selected_company (str): Empresa seleccionada
        company_info (str): Información de la empresa
        temperature (float): Temperatura para el modelo (creatividad)
        
    Returns:
        str: Respuesta del asistente virtual
    """
    # Simular tiempo de respuesta
    time.sleep(1)
    
    # Preparar payload para la API
    payload = {
        "model": API_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": f"""\
                Eres un Asistente de Servicio al Cliente experto y amable. 
                Tu prioridad es resolver dudas de los clientes de "{selected_company}".
                Esta es la información disponible sobre la empresa: {company_info}.

                - Usa un tono cordial.
                - Ofrece respuestas claras.
                - Emplea viñetas o negritas cuando sea apropiado.
                """
            },
            {"role": "user", "content": mensaje}
        ],
        "temperature": temperature,
        "max_tokens": API_MAX_TOKENS
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error al llamar a la API: {str(e)}")
        return "Ocurrió un error procesando tu solicitud. Intenta de nuevo."