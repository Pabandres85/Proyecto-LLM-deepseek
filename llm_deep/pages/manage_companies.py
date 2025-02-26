"""
Página para administrar empresas existentes (editar o eliminar).
"""
import streamlit as st
import json
import os
import datetime

# Importaciones de módulos propios
from utils.config import COMPANY_DATA_PATH, DATA_DIR
from utils.ui import set_dark_mode
from services.data_service import load_company_data, get_company_names

def get_backup_path():
    """
    Obtiene la ruta al archivo de respaldo de empresas eliminadas.
    
    Returns:
        str: Ruta al archivo de respaldo
    """
    return os.path.join(DATA_DIR, "deleted_companies.json")

def ensure_backup_file_exists():
    """
    Asegura que el archivo de respaldo exista, creándolo si es necesario.
    """
    backup_path = get_backup_path()
    if not os.path.exists(backup_path):
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

def display_company_info(company_info):
    """
    Muestra la información actual de la empresa.
    
    Args:
        company_info (dict): Información de la empresa
    """
    st.write("**Información actual de la empresa:**")
    st.json(company_info)

def edit_company_form(company_info):
    """
    Formulario para editar la información de una empresa.
    
    Args:
        company_info (dict): Información actual de la empresa
        
    Returns:
        dict: Información actualizada de la empresa
    """
    # Copia para no modificar el original directamente
    updated_info = company_info.copy()
    
    # Campos del formulario: descripción
    new_desc = st.text_area("Descripción", company_info.get("descripcion", ""), height=80)
    updated_info["descripcion"] = new_desc.strip()
    
    # Servicios (lista)
    st.write("Servicios (uno por línea)")
    if "servicios" in company_info:
        default_services = "\n".join(company_info["servicios"])
    else:
        default_services = ""
    new_services_input = st.text_area("", default_services, height=80)
    new_services_list = [s.strip() for s in new_services_input.splitlines() if s.strip()]
    updated_info["servicios"] = new_services_list
    
    # Horarios
    st.write("Horarios")
    horarios = company_info.get("horarios", {})
    lun_vie = st.text_input("Lunes-Viernes", horarios.get("lunes-viernes", ""))
    sab = st.text_input("Sábado", horarios.get("sábado", ""))
    dom = st.text_input("Domingo", horarios.get("domingo", ""))
    updated_info["horarios"] = {
        "lunes-viernes": lun_vie.strip(),
        "sábado": sab.strip(),
        "domingo": dom.strip()
    }
    
    # Contacto
    st.write("Contacto")
    contacto = company_info.get("contacto", {})
    tel = st.text_input("Teléfono", contacto.get("telefono", ""))
    email = st.text_input("Email", contacto.get("email", ""))
    direccion = st.text_input("Dirección", contacto.get("direccion", ""))
    updated_info["contacto"] = {
        "telefono": tel.strip(),
        "email": email.strip(),
        "direccion": direccion.strip()
    }
    
    # FAQ
    st.write("FAQ (formato pregunta::respuesta, una por línea)")
    faq_dict = company_info.get("faq", {})
    # Convertir diccionario a texto
    default_faq_text = ""
    for question, answer in faq_dict.items():
        default_faq_text += f"{question}::{answer}\n"
    new_faq_input = st.text_area("", default_faq_text.strip(), height=120)
    
    # Procesamiento de FAQ
    updated_faq_dict = {}
    for line in new_faq_input.splitlines():
        line = line.strip()
        if "::" in line:
            q, a = line.split("::", 1)
            updated_faq_dict[q.strip()] = a.strip()
    updated_info["faq"] = updated_faq_dict
    
    return updated_info

def save_company_data(company_data):
    """
    Guarda los datos de las empresas en el archivo JSON.
    
    Args:
        company_data (dict): Datos de todas las empresas
    """
    with open(COMPANY_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(company_data, f, ensure_ascii=False, indent=4)

def delete_company(company_name, company_data):
    """
    Elimina una empresa y la guarda en el archivo de respaldo.
    
    Args:
        company_name (str): Nombre de la empresa a eliminar
        company_data (dict): Datos de todas las empresas
        
    Returns:
        bool: True si se eliminó exitosamente, False de lo contrario
    """
    if company_name not in company_data:
        return False
        
    # 1) Cargar backup
    backup_path = get_backup_path()
    with open(backup_path, "r", encoding="utf-8") as bf:
        backup_data = json.load(bf)

    # 2) Guardar empresa en backup con timestamp
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if company_name not in backup_data:
        backup_data[company_name] = []
    # Cada "borrado" se guarda en la lista, con su data + fecha
    backup_data[company_name].append({
        "deleted_at": now_str,
        "data": company_data[company_name]
    })

    # 3) Guardar backup
    with open(backup_path, "w", encoding="utf-8") as bf:
        json.dump(backup_data, bf, ensure_ascii=False, indent=4)

    # 4) Borramos del JSON principal
    del company_data[company_name]
    save_company_data(company_data)
    
    return True

def main():
    st.title("Administrar Empresas")
    
    # Opción de modo oscuro
    dark_mode = st.toggle("Modo oscuro")
    set_dark_mode(dark_mode)
    
    # Asegurarse de que exista el archivo de respaldo
    ensure_backup_file_exists()

    # Verificamos que exista el principal (company_data.json)
    if not os.path.exists(COMPANY_DATA_PATH):
        st.warning("No se encontró 'company_data.json'. Agrega primero una empresa.")
        return

    # Cargamos el JSON principal
    company_data = load_company_data()

    # Obtenemos la lista de empresas
    company_names = get_company_names()
    if not company_names or company_names == ["Empresa Genérica"]:
        st.info("No hay ninguna empresa registrada.")
        return

    # Seleccionamos la empresa
    st.subheader("Empresas Registradas")
    selected_company = st.selectbox("Selecciona una empresa a gestionar:", company_names)

    # Mostramos la info actual
    display_company_info(company_data[selected_company])

    # Elegir acción: Editar o Eliminar
    action = st.radio("¿Qué deseas hacer con esta empresa?",
                      ["Editar", "Eliminar"], 
                      horizontal=True)

    # -----------------------------------------------------
    # EDICIÓN DE LA EMPRESA
    # -----------------------------------------------------
    if action == "Editar":
        st.write("### Editar información de la empresa:")
        
        # Formulario de edición
        updated_info = edit_company_form(company_data[selected_company])
        
        if st.button("Guardar Cambios"):
            # Actualizar información en el diccionario
            company_data[selected_company] = updated_info
            
            # Guardar a disco
            save_company_data(company_data)
            
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
                if delete_company(selected_company, company_data):
                    st.success(f"La empresa '{selected_company}' ha sido eliminada del archivo principal y respaldada en 'deleted_companies.json'.")
                else:
                    st.error(f"No se pudo eliminar la empresa '{selected_company}'.")
            else:
                st.warning("Debes confirmar la eliminación.")

# Para que funcione en modo multipágina
if __name__ == "__main__":
    main()