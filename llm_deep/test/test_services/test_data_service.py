"""
Pruebas para el módulo services/data_service.py
"""
import os
import pytest
import json
from unittest.mock import patch

# La siguiente línea se usará para simular importaciones
# cuando el módulo real no esté disponible durante las pruebas
pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")

def test_load_company_data(temp_company_data_file):
    """
    Prueba la función load_company_data
    """
    # Importamos el módulo con un path simulado
    with patch('utils.config.COMPANY_DATA_PATH', temp_company_data_file):
        from services.data_service import load_company_data
        
        # Ejecutar la función
        result = load_company_data()
        
        # Verificar que cargó los datos correctamente
        assert isinstance(result, dict)
        assert "Empresa de Prueba" in result
        assert result["Empresa de Prueba"]["descripcion"] == "Esta es una empresa de prueba"
        assert len(result["Empresa de Prueba"]["servicios"]) == 2

def test_save_company_data(temp_dir):
    """
    Prueba la función save_company_data
    """
    # Crear un archivo temporal para guardar
    temp_file = os.path.join(temp_dir, "test_save.json")
    
    # Datos de prueba
    test_data = {
        "Nueva Empresa": {
            "descripcion": "Descripción de prueba",
            "servicios": ["Servicio A"]
        }
    }
    
    # Importamos el módulo con un path simulado
    with patch('utils.config.COMPANY_DATA_PATH', temp_file):
        from services.data_service import save_company_data
        
        # Ejecutar la función
        save_company_data(test_data)
        
        # Verificar que se guardó correctamente
        assert os.path.exists(temp_file)
        
        # Leer el archivo y verificar contenido
        with open(temp_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            
        assert "Nueva Empresa" in saved_data
        assert saved_data["Nueva Empresa"]["descripcion"] == "Descripción de prueba"

def test_get_company_names(temp_company_data_file):
    """
    Prueba la función get_company_names
    """
    with patch('utils.config.COMPANY_DATA_PATH', temp_company_data_file):
        from services.data_service import get_company_names
        
        # Ejecutar la función
        result = get_company_names()
        
        # Verificar resultado
        assert isinstance(result, list)
        assert "Empresa de Prueba" in result
        assert len(result) == 1

def test_get_company_names_empty():
    """
    Prueba la función get_company_names cuando no hay datos
    """
    # Simular que no existe el archivo
    with patch('services.data_service.load_company_data', return_value={}):
        from services.data_service import get_company_names
        
        # Ejecutar la función
        result = get_company_names()
        
        # Verificar resultado por defecto
        assert isinstance(result, list)
        assert "Empresa Genérica" in result
        assert len(result) == 1

def test_get_company_info(temp_company_data_file):
    """
    Prueba la función get_company_info
    """
    with patch('utils.config.COMPANY_DATA_PATH', temp_company_data_file):
        from services.data_service import get_company_info
        
        # Ejecutar la función para una empresa existente
        result = get_company_info("Empresa de Prueba")
        
        # Verificar información
        assert isinstance(result, dict)
        assert result["descripcion"] == "Esta es una empresa de prueba"
        
        # Probar con una empresa que no existe
        not_found = get_company_info("Empresa Inexistente")
        assert not_found == "Información no disponible."

def test_company_exists(temp_company_data_file):
    """
    Prueba la función company_exists
    """
    with patch('utils.config.COMPANY_DATA_PATH', temp_company_data_file):
        from services.data_service import company_exists
        
        # Verificar empresa existente
        assert company_exists("Empresa de Prueba") is True
        
        # Verificar empresa inexistente
        assert company_exists("Empresa Inexistente") is False