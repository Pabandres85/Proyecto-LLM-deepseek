"""
Componentes de UI reutilizables para la aplicación Streamlit.
"""
import streamlit as st
from PIL import Image
import os
from markdown import markdown
from utils.config import UAO_LOGO_PATH, CHATBOT_IMAGE_PATH

def render_header(company_name):
    """
    Renderiza el encabezado de la aplicación con logo y título.
    
    Args:
        company_name (str): Nombre de la empresa seleccionada
    """
    header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

    # Logo UAO
    if os.path.exists(UAO_LOGO_PATH):
        header_image = Image.open(UAO_LOGO_PATH)
        header_image = header_image.resize((120, int(header_image.height*(120/header_image.width))))
        header_col1.image(header_image)

    # Título centrado
    title_html = f"""
        <h1 style='text-align: center; color: #4CAF50;'>Chatbot de Servicio al Cliente - {company_name}</h1>
        <h3 style='text-align: center; color: #555;'>IA para responder preguntas de clientes en {company_name}</h3>
        <hr>
    """
    header_col2.markdown(title_html, unsafe_allow_html=True)

    # Logo Chatbot
    if os.path.exists(CHATBOT_IMAGE_PATH):
        chatbot_image = Image.open(CHATBOT_IMAGE_PATH)
        chatbot_image = chatbot_image.resize((120, int(chatbot_image.height*(120/chatbot_image.width))))
        header_col3.image(chatbot_image)

def set_dark_mode(enabled=False):
    """
    Establece el modo oscuro para la aplicación.
    
    Args:
        enabled (bool): Si es True, activa el modo oscuro
    """
    if enabled:
        st.markdown("""
            <style>
                body {background-color: #121212; color: white;}
                .stApp {background-color: #121212;}
            </style>
        """, unsafe_allow_html=True)

def render_message(user_msg, bot_reply, msg_index, selected_company):
    """
    Renderiza un par mensaje-respuesta en el historial de chat.
    
    Args:
        user_msg (str): Mensaje del usuario
        bot_reply (str): Respuesta del chatbot
        msg_index (int): Índice del mensaje en el historial
        selected_company (str): Empresa seleccionada
        
    Returns:
        str: Feedback seleccionado, si se envió
    """
    # Convertir en HTML (markdown -> HTML) para permitir viñetas, negritas, etc.
    user_html = markdown(user_msg)
    bot_html = markdown(bot_reply)

    # Mostrar mensaje de usuario con estilo
    st.markdown(
        f"""
        <div style='background-color: #333; padding: 10px; border-radius: 10px; margin-bottom: 5px;'>
            <b>Tú:</b><br/>{user_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Mostrar respuesta del chatbot con estilo + markdown interpretado
    st.markdown(
        f"""
        <div style='background-color: #444; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <b>Chatbot:</b><br/>{bot_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Feedback
    feedback_radio_key = f"feedback_radio_{selected_company}_{msg_index}"
    feedback_btn_key = f"feedback_btn_{selected_company}_{msg_index}"
    
    feedback = st.radio(
        f"¿Te fue útil esta respuesta? (Mensaje #{msg_index+1})",
        ["👍 Sí", "👎 No"], 
        horizontal=True, 
        key=feedback_radio_key
    )
    
    feedback_sent = False
    if st.button(f"Enviar Feedback (Mensaje #{msg_index+1})", key=feedback_btn_key):
        feedback_sent = True
        
    return feedback if feedback_sent else None