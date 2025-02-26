"""
Pruebas para el módulo services/chat_service.py
"""
import pytest
from unittest.mock import patch, Mock

def test_get_chatbot_response_success():
    """
    Prueba la obtención de una respuesta exitosa del chatbot
    """
    # Importar el módulo
    from services.chat_service import get_chatbot_response
    
    # Mock para la función requests.post
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Esta es una respuesta de prueba del chatbot."
                }
            }
        ]
    }
    
    # Parche para requests.post y time.sleep
    with patch('requests.post', return_value=mock_response) as mock_post:
        with patch('time.sleep'):  # Evitar esperas en las pruebas
            # Ejecutar función
            response = get_chatbot_response(
                mensaje="¿Cómo puedo hacer un pedido?",
                selected_company="Empresa Test",
                company_info="Información de la empresa",
                temperature=0.7
            )
            
            # Verificar la respuesta
            assert response == "Esta es una respuesta de prueba del chatbot."
            
            # Verificar que requests.post fue llamado con los parámetros correctos
            mock_post.assert_called_once()
            # Verificar args y kwargs
            args, kwargs = mock_post.call_args
            
            # Verificar que la URL es correcta
            assert kwargs['json']['model'] == "deepspeek-r1-distill-qwen-7b"
            assert kwargs['json']['temperature'] == 0.7
            assert len(kwargs['json']['messages']) == 2
            assert kwargs['json']['messages'][0]['role'] == "system"
            assert "Empresa Test" in kwargs['json']['messages'][0]['content']
            assert kwargs['json']['messages'][1]['role'] == "user"
            assert kwargs['json']['messages'][1]['content'] == "¿Cómo puedo hacer un pedido?"

def test_get_chatbot_response_error():
    """
    Prueba el manejo de errores en la respuesta del chatbot
    """
    from services.chat_service import get_chatbot_response
    
    # Simular una excepción al llamar a la API
    with patch('requests.post', side_effect=Exception("Error de conexión")) as mock_post:
        with patch('time.sleep'):  # Evitar esperas en las pruebas
            # Ejecutar función
            response = get_chatbot_response(
                mensaje="¿Horarios?",
                selected_company="Empresa Error",
                company_info="Información",
                temperature=0.5
            )
            
            # Verificar que se devuelve el mensaje de error
            assert "Ocurrió un error procesando tu solicitud" in response
            
            # Verificar que se intentó llamar a la API
            mock_post.assert_called_once()

def test_get_chatbot_response_missing_data():
    """
    Prueba la respuesta del chatbot cuando faltan datos en la respuesta API
    """
    from services.chat_service import get_chatbot_response
    
    # Mock con estructura incompleta
    mock_response = Mock()
    mock_response.json.return_value = {"data": "incompleta"}  # Sin 'choices'
    
    # Parche para simular respuesta incompleta
    with patch('requests.post', return_value=mock_response) as mock_post:
        with patch('time.sleep'):
            # Ejecutar función
            response = get_chatbot_response(
                mensaje="Test incompleto",
                selected_company="Empresa Test",
                company_info="Info",
                temperature=0.5
            )
            
            # Verificar que se captura la excepción
            assert "Ocurrió un error procesando tu solicitud" in response