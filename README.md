# 🤖 Chatbot de Servicio al Cliente con IA

Este es un chatbot inteligente diseñado para **adaptarse a cualquier empresa** y ofrecer un servicio al cliente personalizado. Permite a los usuarios seleccionar una empresa previamente registrada y obtener respuestas automáticas basadas en la información de dicha empresa.

---

## 🚀 Funcionalidades

- 📌 **Selección de Empresa**: Escoge la empresa desde la interfaz para adaptar el chatbot a su contexto.
- 🏢 **Gestión de Empresas**: Agregar y administrar empresas dentro de la plataforma.
- 📊 **Análisis de Datos**: Módulo de analítica para evaluar el rendimiento de las interacciones.
- 💬 **Chatbot Adaptativo**: Se ajusta dinámicamente a la empresa seleccionada.
- 🎨 **Modo Oscuro**: Interfaz moderna y adaptable a diferentes entornos.

---

## 📌 Interfaz
- 📌 **Pagina principal**
![Interfaz del Chatbot](images/interfacePagina.png)
- 📌 **Pagina Agregar Empresa**
![Interfaz del Chatbot](images/agregarEmpresa.png)
- 📌 **Pagina Mantenimiento de Empresas Agregadas**
![Interfaz del Chatbot](images/admonEmpresas.png)
- 📌 **Pagina Analitica**
![Interfaz del Chatbot](images/analitica.png)

---

## ⚙️ Modelo de IA y Servidor Local

El chatbot utiliza un **modelo de lenguaje alojado localmente**, cargado en **LM Studio** como un servidor API.  

### **Detalles del modelo:**
- **Modelo:** `deepseek-coder-v2-lite-instruct`
- **Fuente:** Descargado de **Hugging Face**.
- **Cuantización:** `Q3_K_L` (optimizado para rendimiento en local).
- **Servidor API:** Ejecutado en **LM Studio** 

El chatbot envía consultas al **servidor local**, el cual procesa las solicitudes y devuelve respuestas basadas en la información de la empresa seleccionada.

---

## 🛠️ Tecnologías Utilizadas

- **Python** 🐍 - Lenguaje de programación principal.
- **Streamlit** 📊 - Framework para construir la interfaz gráfica de usuario.
- **NLTK / SpaCy** 🧠 - Procesamiento del lenguaje natural (si se usa IA avanzada).
- **WordCloud** ☁️ - Generación de nubes de palabras para análisis de textos.
- **Plotly** 📈 - Gráficos interactivos para analítica.

---

## 📂 Estructura del Proyecto

📦 proyecto_chatbot_ia
├── 📂 pages/                # Módulos de la aplicación
│   ├── add_company.py       # Módulo para agregar empresas
│   ├── analytics.py         # Análisis de datos de las interacciones
│   ├── manage_companies.py  # Administración de empresas
│
├── app.py                   # Punto de entrada de la aplicación (selección de empresa y chatbot)
│
├── requirements.txt         # Dependencias del proyecto
├── .gitignore               # Archivos a ignorar en Git
├── README.md                # Documentación del proyecto
│
├── 📂 data/                 # Base de datos de empresas e interacciones
│   ├── company_data.json    # Información de empresas
│   ├── chat_log.csv         # Historial de conversación
│
├── 📂 log/                  # Logs del sistema


---

## 🔧 Instalación y Configuración

### 📌 **1. Clonar el repositorio**
```sh
git clone https://github.com/Pabandres85/Proyecto-LLM-deepseek
cd Proyecto-LLM-deepseek

```
### 📌 **2. Crear y activar un entorno virtual**

Ejecuta el siguiente comando según tu sistema operativo:

```sh
python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate     # En Windows
```

### 📌 **3. Instalar las dependencias.**
```sh
pip install -r requirements.txt 
```
### 📌 **4. Ejecutar la aplicación**
```sh
streamlit run app.py
```
Esto abrirá la aplicación en el navegador.

---

## 🏗️ Cómo Funciona

1. **Selecciona una empresa** desde la lista desplegable en la interfaz.
2. **El chatbot se adapta** automáticamente a la empresa seleccionada.
3. **Puedes gestionar empresas** en la sección de administración.
4. **Consulta el análisis de datos** para evaluar el rendimiento del chatbot.

---

## 📌 Mejoras Futuras

- 🔹 **Integración con API de CRM** para mejorar la gestión de clientes.
- 🔹 **Soporte para múltiples idiomas**.
- 🔹 **Implementación de modelos de IA más avanzados**.

---

## 👨‍💻 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar el chatbot, abre un **issue** o envía un **pull request**.

📩 **Contacto**: pabandres
