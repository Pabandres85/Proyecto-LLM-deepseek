"""
Servicio para gestionar los datos de las empresas.
"""
import json
import os
from utils.config import COMPANY_DATA_PATH

def load_company_data():
    """
    Carga los datos de las empresas desde el archivo JSON.
    
    Returns:
        dict: Datos de las empresas o un diccionario vacío si no existe
    """
    if os.path.exists(COMPANY_DATA_PATH):
        with open(COMPANY_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_company_data(company_data):
    """
    Guarda los datos de las empresas en el archivo JSON.
    
    Args:
        company_data (dict): Datos de todas las empresas
    """
    with open(COMPANY_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(company_data, f, ensure_ascii=False, indent=4)

def get_company_names():
    """
    Obtiene la lista de nombres de empresas.
    
    Returns:
        list: Lista de nombres de empresas, o una lista con 'Empresa Genérica' si no hay datos
    """
    company_data = load_company_data()
    return list(company_data.keys()) if company_data else ["Empresa Genérica"]

def get_company_info(company_name):
    """
    Obtiene la información de una empresa específica.
    
    Args:
        company_name (str): Nombre de la empresa
        
    Returns:
        str: Información de la empresa o "Información no disponible"
    """
    company_data = load_company_data()
    return company_data.get(company_name, "Información no disponible.")

def company_exists(company_name):
    """
    Verifica si una empresa ya existe.
    
    Args:
        company_name (str): Nombre de la empresa a verificar
        
    Returns:
        bool: True si la empresa existe, False de lo contrario
    """
    company_data = load_company_data()
    return company_name in company_data