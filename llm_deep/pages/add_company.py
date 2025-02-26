"""
Página para agregar nuevas empresas al sistema.
"""
import streamlit as st
import json
import os

# Importaciones de módulos propios
from utils.config import COMPANY_DATA_PATH
from utils.ui import set_dark_mode
from services.data_service import load_company_data, save_company_data

def parse_faq_input(faq_input):
    """
    Convierte el texto de preguntas frecuentes en un diccionario.
    
    Args:
        faq_input (str): Texto con formato pregunta::respuesta
        
    Returns:
        dict: Diccionario con las preguntas y respuestas
    """
    faq_dict = {}
    for line in faq_input.splitlines():
        line = line.strip()
        if "::" in line:
            question, answer = line.split("::", 1)
            faq_dict[question.strip()] = answer.strip()
    return faq_dict

def parse_services_input(services_input):
    """
    Convierte el texto de servicios en una lista.
    
    Args:
        services_input (str): Texto con un servicio por línea
        
    Returns:
        list: Lista de servicios
    """
    return [s.strip() for s in services_input.splitlines() if s.strip()]

def create_company_structure(
    company_name, 
    description, 
    services_input, 
    horario_lun_vie, 
    horario_sabado, 
    horario_domingo, 
    telefono, 
    email, 
    direccion, 
    faq_input
):
    """
    Crea la estructura de datos para una nueva empresa.
    
    Args:
        company_name (str): Nombre de la empresa
        description (str): Descripción 
        services_input (str): Texto con servicios (uno por línea)
        horario_lun_vie (str): Horario de lunes a viernes
        horario_sabado (str): Horario de sábado
        horario_domingo (str): Horario de domingo
        telefono (str): Teléfono de contacto
        email (str): Email de contacto
        direccion (str): Dirección
        faq_input (str): Texto con preguntas y respuestas
        
    Returns:
        dict: Estructura con los datos de la empresa
    """
    # Transformar las entradas del formulario
    services_list = parse_services_input(services_input)
    faq_dict = parse_faq_input(faq_input)
    
    # Crear la estructura
    return {
        "descripcion": description.strip(),
        "servicios": services_list,
        "horarios": {
            "lunes-viernes": horario_lun_vie.strip(),
            "sábado": horario_sabado.strip(),
            "domingo": horario_domingo.strip()
        },
        "contacto": {
            "telefono": telefono.strip(),
            "email": email.strip(),
            "direccion": direccion.strip()
        },
        "faq": faq_dict
    }

def main():
    st.title("Agregar nueva empresa al Chatbot")
    
    # Opción de modo oscuro
    dark_mode = st.toggle("Modo oscuro")
    set_dark_mode(dark_mode)
    
    # Formulario para recoger datos de la empresa
    st.subheader("Datos básicos")
    company_name = st.text_input("Nombre de la empresa (ej: Viajes Felices)")
    description = st.text_area(
        "Descripción",
        "Breve texto describiendo la empresa..."
    )
    
    st.subheader("Servicios")
    services_input = st.text_area(
        "Lista de servicios (uno por línea)",
        "Reservación de vuelos y hoteles\nTours guiados\nAlquiler de autos"
    )
    
    st.subheader("Horarios")
    horario_lun_vie = st.text_input("Lunes-Viernes", "9:00 AM - 6:00 PM")
    horario_sabado = st.text_input("Sábado", "10:00 AM - 2:00 PM")
    horario_domingo = st.text_input("Domingo", "Cerrado")
    
    st.subheader("Contacto")
    telefono = st.text_input("Teléfono", "+57 312 345 6789")
    email = st.text_input("Email", "contacto@viajesfelices.com")
    direccion = st.text_input("Dirección", "Calle 45 #12-34, Bogotá, Colombia")
    
    st.subheader("FAQ (Preguntas Frecuentes)")
    st.markdown("""
        Formato: una pregunta por línea, luego '::' y la respuesta. Ejemplo:
        
        ```
        ¿Ofrecen descuentos para grupos?::Sí, tenemos paquetes especiales...
        ¿Cuáles son los destinos más populares?::Nuestros destinos más populares...
        ```
    """)
    
    faq_input = st.text_area(
        "Preguntas y respuestas",
        "¿Ofrecen descuentos para grupos?::Sí, tenemos paquetes especiales...\n¿Cuáles son los destinos más populares?::Nuestros destinos más populares..."
    )
    
    if st.button("Guardar"):
        # Validación simple
        if not company_name.strip():
            st.error("El nombre de la empresa es obligatorio.")
            return
            
        # 1. Leemos el JSON actual (si existe)
        company_data = load_company_data()
        
        # 2. Verificar si la empresa ya existe
        if company_name in company_data:
            st.warning(f"La empresa '{company_name}' ya existe. Por favor, usa un nombre diferente o edita la existente.")
            return
            
        # 3. Crear la estructura de la nueva empresa
        new_company_info = create_company_structure(
            company_name, 
            description, 
            services_input, 
            horario_lun_vie, 
            horario_sabado, 
            horario_domingo, 
            telefono, 
            email, 
            direccion, 
            faq_input
        )
        
        # 4. Agregar al diccionario
        company_data[company_name] = new_company_info
        
        # 5. Guardar los datos
        os.makedirs(os.path.dirname(COMPANY_DATA_PATH), exist_ok=True)
        save_company_data(company_data)
        
        st.success(f"La empresa '{company_name}' se agregó correctamente.")

if __name__ == "__main__":
    main()