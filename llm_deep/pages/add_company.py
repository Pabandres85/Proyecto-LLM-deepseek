import streamlit as st
import json
import os

def main():
    st.title("Agregar nueva empresa al Chatbot")

    # Ruta al JSON
    company_data_path = os.path.join("data", "company_data.json")

    # Formulario para recoger datos de la empresa
    st.subheader("Datos básicos")
    company_name = st.text_input("Nombre de la empresa (ej: Viajes Felices)")

    description = st.text_area("Descripción", 
        "Breve texto describiendo la empresa...")

    st.subheader("Servicios")
    services_input = st.text_area("Lista de servicios (uno por línea)",
        "Reservación de vuelos y hoteles\nTours guiados\nAlquiler de autos")

    st.subheader("Horarios")
    horario_lun_vie = st.text_input("Lunes-Viernes", "9:00 AM - 6:00 PM")
    horario_sabado = st.text_input("Sábado", "10:00 AM - 2:00 PM")
    horario_domingo = st.text_input("Domingo", "Cerrado")

    st.subheader("Contacto")
    telefono = st.text_input("Teléfono", "+57 312 345 6789")
    email = st.text_input("Email", "contacto@viajesfelices.com")
    direccion = st.text_input("Dirección", "Calle 45 #12-34, Bogotá, Colombia")

    st.subheader("FAQ (Preguntas Frecuentes)")
    st.markdown("Formato: una pregunta por línea, luego ‘::’ y la respuesta. Ejemplo:\n\n```\n¿Ofrecen descuentos para grupos?::Sí, tenemos paquetes especiales...\n¿Cuáles son los destinos más populares?::Nuestros destinos más populares...\n```")
    faq_input = st.text_area("Preguntas y respuestas", 
        "¿Ofrecen descuentos para grupos?::Sí, tenemos paquetes especiales...\n¿Cuáles son los destinos más populares?::Nuestros destinos más populares...")

    if st.button("Guardar"):
        # 1. Leemos el JSON actual (si existe)
        if os.path.exists(company_data_path):
            with open(company_data_path, "r", encoding="utf-8") as f:
                company_data = json.load(f)
        else:
            company_data = {}

        # 2. Transformar las entradas del formulario
        services_list = [s.strip() for s in services_input.splitlines() if s.strip()]

        # FAQ: lo convertimos en un diccionario
        faq_dict = {}
        for line in faq_input.splitlines():
            line = line.strip()
            if "::" in line:
                question, answer = line.split("::", 1)
                faq_dict[question.strip()] = answer.strip()

        # Crear la estructura
        new_company_info = {
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

        # 3. Agregar al diccionario
        company_data[company_name] = new_company_info

        # 4. Escribimos de nuevo el JSON con indentación
        with open(company_data_path, "w", encoding="utf-8") as f:
            json.dump(company_data, f, ensure_ascii=False, indent=4)

        st.success(f"La empresa '{company_name}' se agregó correctamente.")

if __name__ == "__main__":
    main()
