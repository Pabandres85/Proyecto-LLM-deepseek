"""
Aplicación principal de Chatbot de Servicio al Cliente - Especialización IA.
"""
import streamlit as st
import datetime

# Importar módulos propios
from utils.config import PAGE_TITLE, PAGE_ICON, LAYOUT
from utils.ui import render_header, set_dark_mode, render_message
from utils.logging import log_interaction
from services.data_service import get_company_names, get_company_info
from services.chat_service import get_chatbot_response
from models.chat_history import ChatHistory

# -------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# -------------------------------------------------------------
# INICIALIZACIÓN DE VARIABLES EN session_state
# -------------------------------------------------------------
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Inicializar historial de chat
ChatHistory.initialize()

# -------------------------------------------------------------
# FUNCIÓN CALLBACK: ENVÍA EL MENSAJE AL MODELO
# -------------------------------------------------------------
def enviar_mensaje():
    selected_company = st.session_state["selected_company"]
    company_info = st.session_state["company_info"]

    mensaje = st.session_state["user_input"].strip()
    if not mensaje:
        return  # Si está vacío, no hacemos nada

    with st.spinner("El chatbot está escribiendo..."):
        # Obtener respuesta del chatbot
        temperature = st.session_state.get("temperature", 0.5)
        assistant_reply = get_chatbot_response(
            mensaje, 
            selected_company, 
            company_info, 
            temperature
        )

    # Agregar al historial
    ChatHistory.add_message(selected_company, mensaje, assistant_reply)

    # Limpiar el campo input
    st.session_state["user_input"] = ""

# -------------------------------------------------------------
# CARGAR DATOS DE EMPRESAS
# -------------------------------------------------------------
company_names = get_company_names()
selected_company = st.selectbox("Selecciona una empresa", company_names)

# Manejar cambio de empresa
ChatHistory.handle_company_change(selected_company)

# Guardar empresa y su información en el estado
st.session_state["selected_company"] = selected_company
st.session_state["company_info"] = get_company_info(selected_company)

# -------------------------------------------------------------
# CABECERA (LOGO, TÍTULO, ETC.)
# -------------------------------------------------------------
render_header(selected_company)

# -------------------------------------------------------------
# MODO OSCURO
# -------------------------------------------------------------
dark_mode = st.toggle("Modo oscuro")
set_dark_mode(dark_mode)

# -------------------------------------------------------------
# MOSTRAR HISTORIAL DE CONVERSACIÓN
# -------------------------------------------------------------
st.subheader("Historial de conversación")

# Botón para limpiar el historial de la empresa actual
if st.button("Borrar historial de esta empresa"):
    ChatHistory.clear_history(selected_company)

chat_container = st.container()

# Obtener historial para la empresa actual
chat_history = ChatHistory.get_company_history(selected_company)

# Mostrar mensajes
for i, (user_msg, bot_reply) in enumerate(chat_history):
    feedback = render_message(
        user_msg,
        bot_reply,
        i,
        selected_company
    )
    
    # Si se envió feedback, registrarlo
    if feedback:
        log_interaction(
            user_msg,
            bot_reply,
            selected_company,
            feedback,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        st.success("¡Gracias por tu feedback!")

# -------------------------------------------------------------
# ENTRADA DE TEXTO + BOTÓN DE ENVÍO (CALLBACK)
# -------------------------------------------------------------
st.subheader("Escribe tu consulta:")

st.text_input(
    "Tu mensaje aquí",
    placeholder="Ej: ¿Cuáles son los horarios de atención?",
    key="user_input"
)

temperature = st.slider("Ajuste de creatividad (Temperatura)", 0.1, 1.0, 0.5, 0.1)
st.session_state["temperature"] = temperature

st.button("Enviar", on_click=enviar_mensaje)