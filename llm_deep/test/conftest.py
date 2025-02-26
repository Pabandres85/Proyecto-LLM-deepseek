"""
Fixtures y configuraciones compartidas para las pruebas.
"""
import os
import tempfile
import pytest
import json
import pandas as pd

@pytest.fixture
def temp_dir():
    """
    Crea un directorio temporal para pruebas.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Guardar directorio temporal original
        orig_temp = tmpdirname
        yield tmpdirname
        # No es necesario hacer limpieza ya que tempfile lo hace automáticamente

@pytest.fixture
def sample_company_data():
    """
    Fixture que proporciona datos de ejemplo para empresas.
    """
    return {
        "Empresa de Prueba": {
            "descripcion": "Esta es una empresa de prueba",
            "servicios": ["Servicio 1", "Servicio 2"],
            "horarios": {
                "lunes-viernes": "9:00 AM - 6:00 PM",
                "sábado": "10:00 AM - 2:00 PM",
                "domingo": "Cerrado"
            },
            "contacto": {
                "telefono": "+57 123 456 7890",
                "email": "contacto@empresaprueba.com",
                "direccion": "Calle 123 #45-67, Ciudad"
            },
            "faq": {
                "¿Pregunta 1?": "Respuesta 1",
                "¿Pregunta 2?": "Respuesta 2"
            }
        }
    }

@pytest.fixture
def temp_company_data_file(temp_dir, sample_company_data):
    """
    Crea un archivo temporal de datos de empresas.
    """
    file_path = os.path.join(temp_dir, "company_data.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_company_data, f, ensure_ascii=False, indent=4)
    return file_path

@pytest.fixture
def sample_chat_log():
    """
    Fixture que proporciona datos de ejemplo para el historial de chat.
    """
    return [
        {
            "Fecha y Hora": "2024-02-20 10:30:45",
            "Empresa": "Empresa de Prueba",
            "Usuario": "¿Cuáles son los horarios de atención?",
            "Chatbot": "Los horarios de atención son de lunes a viernes de 9:00 AM a 6:00 PM, sábados de 10:00 AM a 2:00 PM y domingos cerrado.",
            "Feedback": "👍 Sí"
        },
        {
            "Fecha y Hora": "2024-02-20 11:15:22",
            "Empresa": "Empresa de Prueba",
            "Usuario": "¿Tienen servicio a domicilio?",
            "Chatbot": "Sí, ofrecemos servicio a domicilio. Puede solicitar más información al teléfono +57 123 456 7890.",
            "Feedback": "👍 Sí"
        }
    ]

@pytest.fixture
def temp_chat_log_file(temp_dir, sample_chat_log):
    """
    Crea un archivo temporal CSV con datos de chat.
    """
    file_path = os.path.join(temp_dir, "chat_log.csv")
    df = pd.DataFrame(sample_chat_log)
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def mock_streamlit():
    """
    Fixture para simular funciones de Streamlit.
    """
    import sys
    import mock
    
    # Crear un módulo 'streamlit' simulado
    mock_st = mock.MagicMock()
    
    # Simulación de session_state como un diccionario
    mock_st.session_state = {}
    
    # Agregar el módulo al sys.modules
    sys.modules['streamlit'] = mock_st
    
    yield mock_st
    
    # Limpiar después de la prueba
    if 'streamlit' in sys.modules:
        del sys.modules['streamlit']