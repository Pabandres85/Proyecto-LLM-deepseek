"""
Pruebas para el módulo models/chat_history.py
"""
import pytest
from unittest.mock import patch

def test_chat_history_initialize(mock_streamlit):
    """
    Prueba la inicialización del historial de chat
    """
    from models.chat_history import ChatHistory
    
    # Ejecutar la función de inicialización
    ChatHistory.initialize()
    
    # Verificar que se hayan creado las claves en session_state
    assert "chat_history_dict" in mock_streamlit.session_state
    assert "last_company" in mock_streamlit.session_state
    assert mock_streamlit.session_state["chat_history_dict"] == {}
    assert mock_streamlit.session_state["last_company"] is None

def test_get_company_history(mock_streamlit):
    """
    Prueba la obtención del historial de una empresa
    """
    from models.chat_history import ChatHistory
    
    # Inicializar
    mock_streamlit.session_state["chat_history_dict"] = {}
    
    # Obtener historial de una empresa que no existe aún
    history = ChatHistory.get_company_history("Empresa Nueva")
    
    # Verificar que se haya creado el historial vacío
    assert "Empresa Nueva" in mock_streamlit.session_state["chat_history_dict"]
    assert mock_streamlit.session_state["chat_history_dict"]["Empresa Nueva"] == []
    assert history == []
    
    # Probar con una empresa que ya tiene historial
    mock_streamlit.session_state["chat_history_dict"]["Empresa Existente"] = [
        ("Hola", "¿En qué puedo ayudarte?")
    ]
    
    history2 = ChatHistory.get_company_history("Empresa Existente")
    assert len(history2) == 1
    assert history2[0][0] == "Hola"

def test_add_message(mock_streamlit):
    """
    Prueba la adición de mensajes al historial
    """
    from models.chat_history import ChatHistory
    
    # Inicializar
    mock_streamlit.session_state["chat_history_dict"] = {}
    
    # Agregar mensaje a una empresa nueva
    ChatHistory.add_message("Empresa Test", "¿Horarios?", "De 9am a 6pm")
    
    # Verificar que se haya agregado correctamente
    assert "Empresa Test" in mock_streamlit.session_state["chat_history_dict"]
    assert len(mock_streamlit.session_state["chat_history_dict"]["Empresa Test"]) == 1
    assert mock_streamlit.session_state["chat_history_dict"]["Empresa Test"][0] == ("¿Horarios?", "De 9am a 6pm")
    
    # Agregar otro mensaje a la misma empresa
    ChatHistory.add_message("Empresa Test", "Gracias", "De nada")
    
    # Verificar que ahora hay dos mensajes
    assert len(mock_streamlit.session_state["chat_history_dict"]["Empresa Test"]) == 2
    assert mock_streamlit.session_state["chat_history_dict"]["Empresa Test"][1] == ("Gracias", "De nada")

def test_clear_history(mock_streamlit):
    """
    Prueba la limpieza del historial
    """
    from models.chat_history import ChatHistory
    
    # Configurar un historial existente
    mock_streamlit.session_state["chat_history_dict"] = {
        "Empresa A": [("Mensaje 1", "Respuesta 1"), ("Mensaje 2", "Respuesta 2")],
        "Empresa B": [("Otro mensaje", "Otra respuesta")]
    }
    
    # Limpiar el historial de Empresa A
    ChatHistory.clear_history("Empresa A")
    
    # Verificar que se haya limpiado solo Empresa A
    assert mock_streamlit.session_state["chat_history_dict"]["Empresa A"] == []
    assert len(mock_streamlit.session_state["chat_history_dict"]["Empresa B"]) == 1

def test_handle_company_change(mock_streamlit):
    """
    Prueba el manejo de cambio de empresa
    """
    from models.chat_history import ChatHistory
    
    # Configurar estado inicial
    mock_streamlit.session_state["chat_history_dict"] = {
        "Empresa Anterior": [("Mensaje", "Respuesta")]
    }
    mock_streamlit.session_state["last_company"] = "Empresa Anterior"
    
    # Cambiar a una nueva empresa
    ChatHistory.handle_company_change("Nueva Empresa")
    
    # Verificar que se actualizó la última empresa
    assert mock_streamlit.session_state["last_company"] == "Nueva Empresa"
    # Y que se creó un historial vacío para la nueva empresa
    assert "Nueva Empresa" in mock_streamlit.session_state["chat_history_dict"]
    assert mock_streamlit.session_state["chat_history_dict"]["Nueva Empresa"] == []
    
    # Verificar que no pasa nada si "cambiamos" a la misma empresa actual
    mock_streamlit.session_state["chat_history_dict"]["Nueva Empresa"] = [("Prueba", "Respuesta prueba")]
    ChatHistory.handle_company_change("Nueva Empresa")
    # El historial debe mantenerse igual
    assert mock_streamlit.session_state["chat_history_dict"]["Nueva Empresa"] == [("Prueba", "Respuesta prueba")]