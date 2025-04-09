# Aplicación Web de Base de Datos RRHH y Generación Automatizada de Reportes

📌 Descripción General
Esta aplicación en Streamlit integra una base de datos DuckDB para gestionar información de Recursos Humanos y generar reportes automatizados en formato Word. Los usuarios pueden ejecutar consultas SQL directamente desde la interfaz y filtrar registros de empleados para la creación de documentos personalizados.

🚀 Características
* **Gestión de Base de Datos:** Creación y población de una base de datos RRHH con registros estructurados.
* **Ejecución de Consultas SQL:** Consulta de información en tiempo real con DuckDB dentro de la aplicación web.
* **Generación Automática de Documentos Word:** Exportación de reportes personalizados con datos de empleados según filtros como cédula y nombre.

🛠 Tecnologías Utilizadas
* Streamlit (Interfaz Web)
* DuckDB (Base de Datos SQL)
* Pandas (Procesamiento de Datos)
* DocxTemplate (Generación de Documentos Word)

📂 Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd <carpeta-del-proyecto>
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
streamlit run app.py
```

🏗 Cómo Funciona
Inicialización de Base de Datos: Población de la base de datos DuckDB con información de empleados.

Ejecución de Consultas: Los usuarios ingresan consultas SQL y obtienen resultados al instante.

Generación de Reportes: Filtra información de empleados y exporta documentos Word personalizados.

📜 Uso
Abre la aplicación y navega desde la barra lateral.

Selecciona "Ejecución de Consultas SQL" para realizar búsquedas en la base de datos.

Selecciona "Generación de Documentos Word" para consultar y descargar reportes personalizados.

📧 Contribuciones y Contacto
Cualquier sugerencia o mejora es bienvenida. ¡Las contribuciones de código están abiertas!
