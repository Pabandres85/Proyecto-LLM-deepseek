import streamlit as st
import requests
import datetime
from PIL import Image
import os
import json
import csv
import time
from markdown import markdown

# -------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -------------------------------------------------------------
st.set_page_config(page_title="Chat UAO - Especialización IA", 
                   page_icon="🤖", layout="wide")

# -------------------------------------------------------------
# INICIALIZACIÓN DE VARIABLES EN session_state
# -------------------------------------------------------------
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Guardado del historial de chat por empresa
if "chat_history_dict" not in st.session_state:
    st.session_state["chat_history_dict"] = {}

if "last_company" not in st.session_state:
    st.session_state["last_company"] = None

# -------------------------------------------------------------
# RUTA Y FUNCIÓN PARA REGISTRAR INTERACCIONES (CSV)
# -------------------------------------------------------------
log_directory = "log"
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, "chat_log.csv")

def log_interaction(user_query, bot_response, company, feedback, timestamp):
    log_exists = os.path.exists(log_file_path)
    with open(log_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not log_exists:
            writer.writerow(["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"])
        writer.writerow([timestamp, company, user_query, bot_response, feedback])

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
        time.sleep(1)

    # Llamada a la API
    url = "http://172.29.64.1:1234/v1/chat/completions"
    payload = {
        "model": "deepspeek-r1-distill-qwen-7b",
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
        "temperature": st.session_state.get("temperature", 0.5),
        "max_tokens": 1000
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        assistant_reply = response_json["choices"][0]["message"]["content"]
    except Exception:
        assistant_reply = "Ocurrió un error procesando tu solicitud. Intenta de nuevo."

    # Agregar al historial
    st.session_state["chat_history_dict"][selected_company].append((mensaje, assistant_reply))

    # Limpiar el campo input
    st.session_state["user_input"] = ""

# -------------------------------------------------------------
# CARGAR DATOS DE EMPRESAS
# -------------------------------------------------------------
company_data_path = "data/company_data.json"
if os.path.exists(company_data_path):
    with open(company_data_path, "r", encoding="utf-8") as f:
        company_data = json.load(f)
else:
    company_data = {}

company_names = list(company_data.keys()) if company_data else ["Empresa Genérica"]
selected_company = st.selectbox("Selecciona una empresa", company_names)

# Si la empresa cambia, crear (o limpiar) el historial correspondiente
if selected_company != st.session_state["last_company"]:
    st.session_state["last_company"] = selected_company
    if selected_company not in st.session_state["chat_history_dict"]:
        st.session_state["chat_history_dict"][selected_company] = []

st.session_state["selected_company"] = selected_company
st.session_state["company_info"] = company_data.get(selected_company, "Información no disponible.")

# -------------------------------------------------------------
# CABECERA (LOGO, TÍTULO, ETC.)
# -------------------------------------------------------------
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

image_path = "images/UAO-LOGO-NUEVO.png"
if os.path.exists(image_path):
    header_image = Image.open(image_path)
    header_image = header_image.resize((120, int(header_image.height*(120/header_image.width))))
    header_col1.image(header_image)

title_html = f"""
    <h1 style='text-align: center; color: #4CAF50;'>Chatbot de Servicio al Cliente - {selected_company}</h1>
    <h3 style='text-align: center; color: #555;'>IA para responder preguntas de clientes en {selected_company}</h3>
    <hr>
"""
header_col2.markdown(title_html, unsafe_allow_html=True)

chatbot_image_path = "images/CHATBOT.png"
if os.path.exists(chatbot_image_path):
    chatbot_image = Image.open(chatbot_image_path)
    chatbot_image = chatbot_image.resize((120, int(chatbot_image.height*(120/chatbot_image.width))))
    header_col3.image(chatbot_image)

# -------------------------------------------------------------
# MODO OSCURO
# -------------------------------------------------------------
dark_mode = st.toggle("Modo oscuro")
if dark_mode:
    st.markdown("""
        <style>
            body {background-color: #121212; color: white;}
            .stApp {background-color: #121212;}
        </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# MOSTRAR HISTORIAL DE CONVERSACIÓN
# -------------------------------------------------------------
st.subheader("Historial de conversación")

# Botón para limpiar el historial de la empresa actual
if st.button("Borrar historial de esta empresa"):
    st.session_state["chat_history_dict"][selected_company] = []

chat_container = st.container()

# Asegurar de que haya una lista para la empresa actual
if selected_company not in st.session_state["chat_history_dict"]:
    st.session_state["chat_history_dict"][selected_company] = []

for i, (user_msg, bot_reply) in enumerate(st.session_state["chat_history_dict"][selected_company]):
    # Convertir en HTML (markdown -> HTML) para permitir viñetas, negritas, etc.
    user_html = markdown(user_msg)
    bot_html = markdown(bot_reply)

    # Mostrar mensaje de usuario con estilo
    chat_container.markdown(
        f"""
        <div style='background-color: #333; padding: 10px; border-radius: 10px; margin-bottom: 5px;'>
            <b>Tú:</b><br/>{user_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Mostrar respuesta del chatbot con estilo + markdown interpretado
    chat_container.markdown(
        f"""
        <div style='background-color: #444; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <b>Chatbot:</b><br/>{bot_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Feedback
    feedback_radio_key = f"feedback_radio_{selected_company}_{i}"
    feedback_btn_key = f"feedback_btn_{selected_company}_{i}"
    feedback = chat_container.radio(
        f"¿Te fue útil esta respuesta? (Mensaje #{i+1})",
        ["👍 Sí", "👎 No"], 
        horizontal=True, 
        key=feedback_radio_key
    )
    if chat_container.button(f"Enviar Feedback (Mensaje #{i+1})", key=feedback_btn_key):
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
