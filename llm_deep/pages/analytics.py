import streamlit as st
import pandas as pd
import os
import re
from collections import Counter

# Para WordCloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def main():
    st.title("Dashboard Chatbot de Servicio al Cliente")

    # Ruta hacia tu archivo CSV de interacciones
    log_file_path = os.path.join("log", "chat_log.csv")

    # Verificación de la existencia del archivo
    if not os.path.exists(log_file_path):
        st.warning("No hay registro de interacciones (chat_log.csv) todavía.")
        return

    # Cargar datos en un DataFrame
    df = pd.read_csv(log_file_path)

    # Revisar si existen las columnas críticas
    expected_cols = ["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"]
    for col in expected_cols:
        if col not in df.columns:
            st.error(f"Falta la columna '{col}' en el CSV. Revisa la estructura.")
            return

    # Mostrar la tabla completa (opcional: en un expander)
    with st.expander("Ver tabla completa sin filtrar"):
        st.subheader("Tabla de datos (completa)")
        st.dataframe(df, use_container_width=True)

    # Convertir a datetime y limpiar
    df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"], errors="coerce")
    df = df.dropna(subset=["Fecha y Hora"])

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

    # Aplicar el filtro
    mask = (df["Fecha y Hora"].dt.date >= start_date) & \
           (df["Fecha y Hora"].dt.date <= end_date)
    filtered_df = df[mask]
    st.write(f"Total interacciones en el rango: {len(filtered_df)}")

    # Mostrar la tabla filtrada en un expander
    with st.expander("Ver datos filtrados"):
        st.dataframe(filtered_df, use_container_width=True)

    # -------------------------------
    # ESTADÍSTICAS DE FEEDBACK
    # -------------------------------
    st.subheader("Estadísticas de feedback (Datos Filtrados)")
    if not filtered_df.empty:
        feedback_counts = filtered_df["Feedback"].value_counts()
        st.bar_chart(feedback_counts)
    else:
        st.info("No hay datos para mostrar (filtrados).")

    # -------------------------------
    # INTERACCIONES POR EMPRESA
    # -------------------------------
    st.subheader("Interacciones por Empresa (Datos Filtrados)")
    if not filtered_df.empty:
        empresa_counts = filtered_df["Empresa"].value_counts()
        st.bar_chart(empresa_counts)
    else:
        st.info("No hay datos para mostrar (filtrados).")

    # -------------------------------
    # ANÁLISIS DE TEXTO (PALABRAS FRECUENTES) EN "Usuario"
    # -------------------------------
    st.subheader("Análisis de Texto en la columna 'Usuario'")

    if filtered_df.empty:
        st.info("No hay datos para análisis de texto con el filtro actual.")
        return

    # Unir todo el texto de la columna "Usuario"
    all_text = " ".join(str(x) for x in filtered_df["Usuario"].dropna())

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

    # -------------------------------
    # WORDCLOUD
    # -------------------------------
    st.subheader("Nube de Palabras (WordCloud)")

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

# Llamamos la función principal
if __name__ == "__main__":
    main()
