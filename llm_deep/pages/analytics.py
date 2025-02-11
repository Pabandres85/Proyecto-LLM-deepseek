import streamlit as st
import pandas as pd
import os
import base64
import datetime

def main():
    st.title("Dashboard Chatbot de Servicio al Cliente")

    # Ruta hacia tu archivo CSV de interacciones
    log_file_path = os.path.join("log", "chat_log.csv")

    # Verificacion 
    if not os.path.exists(log_file_path):
        st.warning("No hay registro de interacciones (chat_log.csv) todavía.")
        return

    # Cargar datos en un DataFrame
    df = pd.read_csv(log_file_path)

    # Verificar que las columnas clave existan
    required_columns = ["Fecha y Hora", "Empresa", "Usuario", "Chatbot", "Feedback"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        st.error(f"Faltan las columnas requeridas en el CSV: {missing_cols}")
        return

    # Convertir la columna "Fecha y Hora" a datetime
    df["Fecha y Hora"] = pd.to_datetime(df["Fecha y Hora"], errors="coerce")
    # Eliminar filas con fechas inválidas
    df = df.dropna(subset=["Fecha y Hora"])

    # -----------------------------------------------------
    # FILTROS
    # -----------------------------------------------------
    # Filtro por rango de fechas
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

    # Filtro por empresa (multiselect, por si quieres ver varias a la vez)
    st.subheader("Filtrar por empresa")
    empresas_unicas = df["Empresa"].unique().tolist()
    selected_empresas = st.multiselect("Selecciona una o varias empresas",
                                       options=empresas_unicas,
                                       default=empresas_unicas)

    # Aplicar filtros
    mask_fecha = (df["Fecha y Hora"].dt.date >= start_date) & \
                 (df["Fecha y Hora"].dt.date <= end_date)
    mask_empresa = df["Empresa"].isin(selected_empresas)
    df_filtered = df[mask_fecha & mask_empresa]

    st.write(f"Total interacciones en el rango y empresas seleccionadas: {len(df_filtered)}")

    # Mostrar la tabla filtrada (opcional: con scroll horizontal)
    with st.expander("Ver datos filtrados"):
        st.dataframe(df_filtered, use_container_width=True)

    # -----------------------------------------------------
    # GRÁFICO DE FEEDBACK
    # -----------------------------------------------------
    st.subheader("Estadísticas de feedback")
    if not df_filtered.empty:
        feedback_counts = df_filtered["Feedback"].value_counts()
        st.bar_chart(feedback_counts)
    else:
        st.info("No hay datos que mostrar con los filtros actuales.")

    # Feedback por empresa
    st.subheader("Feedback por empresa")
    if not df_filtered.empty:
        # Podemos agrupar y contar
        feedback_by_company = df_filtered.groupby(["Empresa", "Feedback"]).size().unstack(fill_value=0)
        st.write(feedback_by_company)

        # Mostrar un gráfico de barras apiladas:
        st.bar_chart(feedback_by_company)
    else:
        st.info("No hay datos para mostrar feedback por empresa.")

    # -----------------------------------------------------
    # GRÁFICO DE USO EN EL TIEMPO
    # -----------------------------------------------------
    st.subheader("Interacciones a lo largo del tiempo")
    if not df_filtered.empty:
        # Agrupamos por fecha (sin hora) y contamos
        daily_counts = df_filtered.groupby(df_filtered["Fecha y Hora"].dt.date).size()
        daily_counts.index = pd.to_datetime(daily_counts.index)  # Convertir a datetime para graficar
        daily_counts = daily_counts.sort_index()
        st.line_chart(daily_counts)
    else:
        st.info("No hay datos para graficar en el tiempo con los filtros actuales.")

    # -----------------------------------------------------
    # DESCARGAR CSV FILTRADO
    # -----------------------------------------------------
    def download_csv(dataframe):
        csv_data = dataframe.to_csv(index=False)
        b64 = base64.b64encode(csv_data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="interacciones_filtradas.csv">Descargar CSV Filtrado</a>'
        return href

    if not df_filtered.empty:
        st.subheader("Descargar datos filtrados")
        st.markdown(download_csv(df_filtered), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
