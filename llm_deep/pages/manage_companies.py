import streamlit as st
import json
import os
import datetime

def main():
    st.title("Administrar Empresas")

    # Rutas de archivos JSON
    company_data_path = os.path.join("data", "company_data.json")
    backup_path = os.path.join("data", "deleted_companies.json")

    # Asegurarnos de que exista el archivo de respaldo, aunque sea vacío
    if not os.path.exists(backup_path):
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

    # Verificamos que exista el principal (company_data.json)
    if not os.path.exists(company_data_path):
        st.warning("No se encontró 'company_data.json'. Agrega primero una empresa.")
        return

    # Cargamos el JSON principal
    with open(company_data_path, "r", encoding="utf-8") as f:
        company_data = json.load(f)

    # Obtenemos la lista de empresas
    company_names = list(company_data.keys())
    if not company_names:
        st.info("No hay ninguna empresa registrada.")
        return

    # Seleccionamos la empresa
    st.subheader("Empresas Registradas")
    selected_company = st.selectbox("Selecciona una empresa a gestionar:", company_names)

    # Mostramos la info actual
    st.write("**Información actual de la empresa:**")
    st.json(company_data[selected_company])

    # Elegir acción: Editar o Eliminar
    action = st.radio("¿Qué deseas hacer con esta empresa?",
                      ["Editar", "Eliminar"], 
                      horizontal=True)

    # -----------------------------------------------------
    # EDICIÓN DE LA EMPRESA
    # -----------------------------------------------------
    if action == "Editar":
        st.write("### Editar información de la empresa:")
        current_info = company_data[selected_company]

        # Campos del formulario: descripción
        new_desc = st.text_area("Descripción", current_info.get("descripcion", ""), height=80)

        # Servicios (lista)
        st.write("Servicios (uno por línea)")
        if "servicios" in current_info:
            default_services = "\n".join(current_info["servicios"])
        else:
            default_services = ""
        new_services_input = st.text_area("", default_services, height=80)

        # Horarios
        st.write("Horarios")
        horarios = current_info.get("horarios", {})
        lun_vie = st.text_input("Lunes-Viernes", horarios.get("lunes-viernes", ""))
        sab = st.text_input("Sábado", horarios.get("sábado", ""))
        dom = st.text_input("Domingo", horarios.get("domingo", ""))

        # Contacto
        st.write("Contacto")
        contacto = current_info.get("contacto", {})
        tel = st.text_input("Teléfono", contacto.get("telefono", ""))
        email = st.text_input("Email", contacto.get("email", ""))
        direccion = st.text_input("Dirección", contacto.get("direccion", ""))

        # FAQ
        st.write("FAQ (formato pregunta::respuesta, una por línea)")
        faq_dict = current_info.get("faq", {})
        # Convertir diccionario a texto
        default_faq_text = ""
        for question, answer in faq_dict.items():
            default_faq_text += f"{question}::{answer}\n"
        new_faq_input = st.text_area("", default_faq_text.strip(), height=120)

        if st.button("Guardar Cambios"):
            # Guardar nueva info en memory
            # 1) Descripción
            current_info["descripcion"] = new_desc.strip()
            # 2) Servicios
            new_services_list = [s.strip() for s in new_services_input.splitlines() if s.strip()]
            current_info["servicios"] = new_services_list
            # 3) Horarios
            current_info["horarios"] = {
                "lunes-viernes": lun_vie.strip(),
                "sábado": sab.strip(),
                "domingo": dom.strip()
            }
            # 4) Contacto
            current_info["contacto"] = {
                "telefono": tel.strip(),
                "email": email.strip(),
                "direccion": direccion.strip()
            }
            # 5) FAQ
            updated_faq_dict = {}
            for line in new_faq_input.splitlines():
                line = line.strip()
                if "::" in line:
                    q, a = line.split("::", 1)
                    updated_faq_dict[q.strip()] = a.strip()
            current_info["faq"] = updated_faq_dict

            # Reemplazamos en el diccionario principal
            company_data[selected_company] = current_info

            # Guardamos a disco
            with open(company_data_path, "w", encoding="utf-8") as f:
                json.dump(company_data, f, ensure_ascii=False, indent=4)

            st.success(f"Se han actualizado los datos de '{selected_company}'.")

    # -----------------------------------------------------
    # ELIMINAR LA EMPRESA (CON BACKUP)
    # -----------------------------------------------------
    elif action == "Eliminar":
        st.write("### Eliminar esta empresa")
        st.info("Si confirmas, la empresa se moverá a 'deleted_companies.json' y luego se borrará del archivo principal.")
        if st.button("Eliminar ahora"):
            confirm = st.checkbox("Confirmo que deseo eliminar esta empresa de la lista.")
            if confirm:
                # 1) Cargar backup
                with open(backup_path, "r", encoding="utf-8") as bf:
                    backup_data = json.load(bf)

                # 2) Guardar empresa en backup con timestamp
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if selected_company not in backup_data:
                    backup_data[selected_company] = []
                # Cada "borrado" se guarda en la lista, con su data + fecha
                backup_data[selected_company].append({
                    "deleted_at": now_str,
                    "data": company_data[selected_company]
                })

                # 3) Guardar backup
                with open(backup_path, "w", encoding="utf-8") as bf:
                    json.dump(backup_data, bf, ensure_ascii=False, indent=4)

                # 4) Borramos del JSON principal
                del company_data[selected_company]
                with open(company_data_path, "w", encoding="utf-8") as cf:
                    json.dump(company_data, cf, ensure_ascii=False, indent=4)

                st.success(f"La empresa '{selected_company}' ha sido eliminada del archivo principal y respaldada en 'deleted_companies.json'.")
            else:
                st.warning("Debes confirmar la eliminación.")

# Para que funcione en modo multipágina, llamamos directamente a main()
main()
