"""
Modelo para gestionar el historial de chat.
"""
import streamlit as st

class ChatHistory:
    """
    Clase para manejar el historial de chat por empresa.
    """
    
    @staticmethod
    def initialize():
        """
        Inicializa las variables de estado para el historial de chat.
        """
        if "chat_history_dict" not in st.session_state:
            st.session_state["chat_history_dict"] = {}
            
        if "last_company" not in st.session_state:
            st.session_state["last_company"] = None
    
    @staticmethod
    def get_company_history(company):
        """
        Obtiene el historial de chat para una empresa específica.
        
        Args:
            company (str): Nombre de la empresa
            
        Returns:
            list: Lista de tuplas (mensaje_usuario, respuesta_bot)
        """
        if company not in st.session_state["chat_history_dict"]:
            st.session_state["chat_history_dict"][company] = []
            
        return st.session_state["chat_history_dict"][company]
    
    @staticmethod
    def add_message(company, user_message, bot_response):
        """
        Agrega un nuevo par mensaje-respuesta al historial.
        
        Args:
            company (str): Nombre de la empresa
            user_message (str): Mensaje del usuario
            bot_response (str): Respuesta del chatbot
        """
        if company not in st.session_state["chat_history_dict"]:
            st.session_state["chat_history_dict"][company] = []
            
        st.session_state["chat_history_dict"][company].append((user_message, bot_response))
    
    @staticmethod
    def clear_history(company):
        """
        Limpia el historial para una empresa específica.
        
        Args:
            company (str): Nombre de la empresa
        """
        st.session_state["chat_history_dict"][company] = []
        
    @staticmethod
    def handle_company_change(new_company):
        """
        Maneja el cambio de empresa seleccionada.
        
        Args:
            new_company (str): Nueva empresa seleccionada
        """
        if new_company != st.session_state["last_company"]:
            st.session_state["last_company"] = new_company
            
            if new_company not in st.session_state["chat_history_dict"]:
                st.session_state["chat_history_dict"][new_company] = []