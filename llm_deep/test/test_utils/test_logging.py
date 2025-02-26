"""
Pruebas para el módulo utils/logging.py
"""
import os
import csv
import pytest
from unittest.mock import patch

def test_log_interaction(temp_dir):
    """
    Prueba la función de registro de interacciones
    """
    # Definir el archivo de log temporal
    log_file = os.path.join(temp_dir, "test_log.csv")
    
    # Importar con el path simulado
    with patch('utils.config.LOG_FILE_PATH', log_file):
        from utils.logging import log_interaction
        
        # Ejecutar la función
        log_interaction(
            user_query="¿Cómo puedo contactarlos?",
            bot_response="Puedes llamarnos al 123-456-7890.",
            company="Empresa Test",
            feedback="👍 Sí",
            timestamp="2024-02-25 15:30:00"
        )
        
        # Verificar que se creó el archivo
        assert os.path.exists(log_file)
        
        # Verificar el contenido del archivo
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Debe tener la cabecera y una fila de datos
            assert len(rows) == 2
            # Verificar la cabecera
            assert rows[0] == ["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"]
            # Verificar los datos
            assert rows[1][0] == "2024-02-25 15:30:00"
            assert rows[1][1] == "Empresa Test"
            assert rows[1][2] == "¿Cómo puedo contactarlos?"
            assert rows[1][3] == "Puedes llamarnos al 123-456-7890."
            assert rows[1][4] == "👍 Sí"

def test_log_interaction_append(temp_dir):
    """
    Prueba que la función añada registros a un archivo existente
    """
    # Definir el archivo de log temporal
    log_file = os.path.join(temp_dir, "test_log.csv")
    
    # Crear un archivo CSV inicial
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"])
        writer.writerow(["2024-02-25 14:00:00", "Empresa A", "Pregunta 1", "Respuesta 1", "👍 Sí"])
    
    # Importar con el path simulado
    with patch('utils.config.LOG_FILE_PATH', log_file):
        from utils.logging import log_interaction
        
        # Ejecutar la función para añadir un nuevo registro
        log_interaction(
            user_query="Pregunta 2",
            bot_response="Respuesta 2",
            company="Empresa B",
            feedback="👎 No",
            timestamp="2024-02-25 15:00:00"
        )
        
        # Verificar el contenido actualizado
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Ahora debe tener la cabecera y dos filas de datos
            assert len(rows) == 3
            # Verificar el nuevo registro
            assert rows[2][0] == "2024-02-25 15:00:00"
            assert rows[2][1] == "Empresa B"
            assert rows[2][2] == "Pregunta 2"
            assert rows[2][3] == "Respuesta 2"
            assert rows[2][4] == "👎 No"

def test_log_interaction_auto_timestamp(temp_dir):
    """
    Prueba que la función genere automáticamente un timestamp si no se proporciona
    """
    # Definir el archivo de log temporal
    log_file = os.path.join(temp_dir, "test_log.csv")
    
    # Importar con el path simulado
    with patch('utils.config.LOG_FILE_PATH', log_file):
        from utils.logging import log_interaction
        import datetime
        
        # Mock para datetime.now()
        fixed_datetime = datetime.datetime(2024, 2, 25, 16, 30, 0)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = fixed_datetime
            mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
            
            # Ejecutar la función sin timestamp
            log_interaction(
                user_query="Pregunta automática",
                bot_response="Respuesta automática",
                company="Empresa Auto",
                feedback="👍 Sí"
            )
        
        # Verificar el contenido
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            # Verificar que usó el timestamp generado
            expected_timestamp = "2024-02-25 16:30:00"
            assert rows[1][0] == expected_timestamp