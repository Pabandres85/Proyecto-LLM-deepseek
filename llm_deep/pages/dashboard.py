"""
Dashboard para analizar las interacciones del chatbot
"""
import streamlit as st
import pandas as pd
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Importaciones de módulos propios
from utils.config import LOG_FILE_PATH
from utils.ui import set_dark_mode

def load_interaction_data():
    """
    Carga los datos de interacciones desde el archivo CSV.
    
    Returns:
        pandas.DataFrame: DataFrame con las interacciones o None si no existe
    """
    # Verificación de la existencia del archivo
    if not os.path.exists(LOG_FILE_PATH):
        return None
        
    # Cargar datos en un DataFrame
    try:
        df = pd.read_csv(LOG_FILE_PATH)
        
        # Revisar si existen las columnas críticas
        expected_cols = ["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"]
        for col in expected_cols:
            if col not in df.columns:
                st.error(f"Falta la columna '{col}' en el CSV. Revisa la estructura.")
                return None
                
        # Convertir a datetime y limpiar
        df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"], errors="coerce")
        df = df.dropna(subset=["Fecha y Hora"])
        
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

def filter_by_date(df, start_date, end_date):
    """
    Filtra el DataFrame por rango de fechas.
    
    Args:
        df (pandas.DataFrame): DataFrame original
        start_date (datetime.date): Fecha de inicio
        end_date (datetime.date): Fecha de fin
        
    Returns:
        pandas.DataFrame: DataFrame filtrado
    """
    if df is None or df.empty:
        return df
        
    # Aplicar el filtro
    mask = (df["Fecha y Hora"].dt.date >= start_date) & \
           (df["Fecha y Hora"].dt.date <= end_date)
    return df[mask]

def show_feedback_stats(df):
    """
    Muestra estadísticas de feedback.
    
    Args:
        df (pandas.DataFrame): DataFrame filtrado
    """
    st.subheader("Estadísticas de feedback (Datos Filtrados)")
    if df is not None and not df.empty:
        feedback_counts = df["Feedback"].value_counts()
        st.bar_chart(feedback_counts)
    else:
        st.info("No hay datos para mostrar (filtrados).")

def show_company_interactions(df):
    """
    Muestra interacciones por empresa.
    
    Args:
        df (pandas.DataFrame): DataFrame filtrado
    """
    st.subheader("Interacciones por Empresa (Datos Filtrados)")
    if df is not None and not df.empty:
        empresa_counts = df["Empresa"].value_counts()
        st.bar_chart(empresa_counts)
    else:
        st.info("No hay datos para mostrar (filtrados).")

def analyze_text(df):
    """
    Analiza el texto de las consultas de usuarios.
    
    Args:
        df (pandas.DataFrame): DataFrame filtrado
    """
    st.subheader("Análisis de Texto en la columna 'Usuario'")

    if df is None or df.empty:
        st.info("No hay datos para análisis de texto con el filtro actual.")
        return

    # Unir todo el texto de la columna "Usuario"
    all_text = " ".join(str(x) for x in df["Usuario"].dropna())

    # Limpieza básica (regex): 
    # - minúsculas
    # - quitar caracteres que no sean letras/ números/ tildes
    text_clean = re.sub(r"[^\wáéíóúñA-Za-z]+", " ", all_text.lower())
    tokens = text_clean.split()

    # Stopwords en español (básicas)
    stopwords_es = {
        "de","la","que","el","en","y","a","los","del","se","las","un","por","con",
        "para","su","una","al","lo","como","más","o","pero","sus","le","ya","o",
        "sí","sobre","me","si","sin","este","entre","cuando","también","voy","tu",
        "mis","muy","no","es","son","cada","donde","haber","todos","antes","te",
        "está","estás","están","he","ha","hay","fue","fui","fueron"
    }
    tokens = [t for t in tokens if t not in stopwords_es]

    if not tokens:
        st.info("Tras la limpieza y eliminación de stopwords, no quedó nada que mostrar.")
        return

    # Contar frecuencia
    freq = Counter(tokens)
    most_common = freq.most_common(20)  # Top 20

    st.write("Top 20 palabras más frecuentes (datos filtrados):")
    df_freq = pd.DataFrame(most_common, columns=["Palabra", "Frecuencia"])
    st.table(df_freq)

    # Gráfico de barras
    st.bar_chart(data=df_freq.set_index("Palabra"))
    
    return tokens

def create_wordcloud(tokens):
    """
    Crea y muestra una nube de palabras.
    
    Args:
        tokens (list): Lista de tokens de palabras
    """
    if not tokens:
        return
        
    st.subheader("Nube de Palabras (WordCloud)")

    # Stopwords en español (básicas)
    stopwords_es = {
        "de","la","que","el","en","y","a","los","del","se","las","un","por","con",
        "para","su","una","al","lo","como","más","o","pero","sus","le","ya","o",
        "sí","sobre","me","si","sin","este","entre","cuando","también","voy","tu",
        "mis","muy","no","es","son","cada","donde","haber","todos","antes","te",
        "está","estás","están","he","ha","hay","fue","fui","fueron"
    }
    
    wc_stopwords = set(STOPWORDS)
    wc_stopwords.update(stopwords_es)
    
    wordcloud = WordCloud(
        background_color="white",
        max_words=100,
        stopwords=wc_stopwords,
        width=800,
        height=400
    ).generate(" ".join(tokens))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

def main():
    st.title("Dashboard Chatbot de Servicio al Cliente")
    
    # Opción de modo oscuro
    dark_mode = st.toggle("Modo oscuro")
    set_dark_mode(dark_mode)

    # Cargar datos
    df = load_interaction_data()
    
    if df is None:
        st.warning("No hay registro de interacciones (chat_log.csv) todavía.")
        return
        
    # Mostrar la tabla completa (opcional: en un expander)
    with st.expander("Ver tabla completa sin filtrar"):
        st.subheader("Tabla de datos (completa)")
        st.dataframe(df, use_container_width=True)

    # -------------------------------
    # FILTRO POR RANGO DE FECHAS
    # -------------------------------
    st.subheader("Filtrar por fecha")
    min_date = df["Fecha y Hora"].min().date()
    max_date = df["Fecha y Hora"].max().date()

    start_date, end_date = st.date_input(
        "Selecciona rango de fechas",
        (min_date, max_date)
    )
    
    if start_date > end_date:
        st.error("La fecha de inicio es mayor que la de fin.")
        return

    # Filtrar datos
    filtered_df = filter_by_date(df, start_date, end_date)
    st.write(f"Total interacciones en el rango: {len(filtered_df)}")

    # Mostrar la tabla filtrada en un expander
    with st.expander("Ver datos filtrados"):
        st.dataframe(filtered_df, use_container_width=True)

    # Mostrar estadísticas
    show_feedback_stats(filtered_df)
    show_company_interactions(filtered_df)
    
    # Análisis de texto
    tokens = analyze_text(filtered_df)
    
    # WordCloud
    if tokens:
        create_wordcloud(tokens)

# Llamamos la función principal
if __name__ == "__main__":
    main()
