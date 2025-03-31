import streamlit as st
import duckdb
import pandas as pd
from docxtpl import DocxTemplate
import io

def crear_y_poblar_db():
    # Conectar (o crear) la base de datos en modo archivo
    conn = duckdb.connect('hr_database.duckdb', read_only=False)
    
    # Crear la tabla para los tipos de contrato
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tipos_contrato (
        id INTEGER PRIMARY KEY,
        descripcion VARCHAR NOT NULL UNIQUE
    );
    """)
    
    # Insertar datos en la tabla de tipos de contrato
    conn.execute("""
    INSERT INTO tipos_contrato (id, descripcion) VALUES
        (1, 'Termino Indefinido'),
        (2, 'Termino Fijo'),
        (3, 'Obra o Labor'),
        (4, 'Aprendizaje')
    ON CONFLICT DO NOTHING;
    """)
    
    # Crear la tabla para el personal de RRHH, referenciando el tipo de contrato
    conn.execute("""
    CREATE TABLE IF NOT EXISTS personal_rrhh (
        id INTEGER PRIMARY KEY,
        cedula VARCHAR(20) NOT NULL,
        nombre_completo VARCHAR(100) NOT NULL,
        fecha_ingreso DATE NOT NULL,
        fecha_retiro DATE,
        cargo VARCHAR(50) NOT NULL,
        salario DECIMAL(10,2) NOT NULL,
        proyecto VARCHAR(50),
        tipo_contrato_id INTEGER NOT NULL,
        FOREIGN KEY (tipo_contrato_id) REFERENCES tipos_contrato(id)
    );
    """)
    
    # Insertar algunos datos de ejemplo en personal_rrhh
    conn.execute("""
    INSERT INTO personal_rrhh (id, cedula, nombre_completo, fecha_ingreso, fecha_retiro, cargo, salario, proyecto, tipo_contrato_id)
    VALUES
    (1, '10000001', 'Carlos Pérez', '2023-01-10', '2023-07-10', 'Auxiliar de Logística', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto A', 1),
    (2, '10000001', 'Carlos Pérez', '2023-08-01', '2024-02-01', 'Líder de Logística', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto B', 2),
    (3, '10000002', 'María Gómez', '2023-02-15', '2024-02-15', 'Analista de Sistemas', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto B', 2),
    (4, '10000003', 'Juan Rodríguez', '2023-03-20', '2024-09-20', 'Asistente Administrativo', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto C', 3),
    (5, '10000004', 'Laura Ramírez', '2023-04-25', '2023-10-25', 'Conductor de Reparto', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto D', 1),
    (6, '10000005', 'Andrés Herrera', '2023-05-30', '2024-05-30', 'Operario de Producción', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto A', 2),
    (7, '10000006', 'Sofía Castro', '2023-06-15', '2024-12-15', 'Coordinador de Logística', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto B', 3),
    (8, '10000007', 'Felipe Ruiz', '2023-07-20', '2024-01-20', 'Ingeniero de Software', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto C', 1),
    (9, '10000008', 'Diana López', '2023-08-25', '2024-08-25', 'Gerente Administrativo', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto D', 2),
    (10, '10000009', 'Ricardo Medina', '2023-09-30', '2025-03-30', 'Conductor de Carga', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto A', 3),
    (11, '10000010', 'Valeria Sánchez', '2023-10-05', '2024-04-05', 'Operario de Ensamblaje', ROUND(RANDOM() * (5000000 - 1400000) + 1400000, -3), 'Proyecto B', 1)
    ON CONFLICT DO NOTHING;
    """)
    
    conn.close()
    st.success("Base de datos creada y poblada correctamente.")

# Página 1: Generación de Consultas
def pagina_consultas():
    st.title("Consulta a la Base de Datos HR con DuckDB")
    
    if st.button("Crear y poblar Base de Datos"):
        crear_y_poblar_db()
        
    # Conectar a la base de datos DuckDB
    conn = duckdb.connect('hr_database.duckdb')
    
    # Conectar a la base de datos DuckDB
    #conn = duckdb.connect('hr_database.duckdb')
    
    # Área para ingresar la consulta SQL
    query_input = st.text_area("Ingresa tu consulta SQL:")
    
    if st.button("Ejecutar Query"):
        if not query_input.strip():
            st.warning("Por favor ingresa una consulta SQL válida.")
        else:
            try:
                # Ejecuta la consulta y obtiene los resultados como DataFrame
                resultado_query = conn.execute(query_input).fetch_df()
                st.write("Resultados:")
                st.dataframe(resultado_query)
            except Exception as e:
                st.error(f"Error al ejecutar la consulta: {e}")
    
    conn.close()

# Página 2: Generación de Word Automatizado
def pagina_generacion_word():
    st.title("Generación de Word Automatizado")
    
    if st.button("Crear y poblar Base de Datos"):
        crear_y_poblar_db()
        
    # Conectar a la base de datos DuckDB
    conn = duckdb.connect('hr_database.duckdb')
    
    # Controles de filtrado: cédula y nombre
    cedula_filter = st.text_input("Ingrese la cédula:")
    nombre_filter = st.text_input("Ingrese el nombre:")
    
    if st.button("Generar Word"):
        # Construir la consulta SQL en función de los filtros ingresados
        query = """
        SELECT pr.id,
        pr.cedula,
        pr.nombre_completo,
        pr.fecha_ingreso,
        pr.fecha_retiro,
        pr.cargo,
        pr.salario,
        pr.proyecto,
        tc.descripcion AS tipo_contrato
        FROM personal_rrhh pr
        INNER JOIN tipos_contrato tc ON pr.tipo_contrato_id = tc.id
        WHERE 1=1
        """
        if cedula_filter.strip():
            query += f" AND pr.cedula = '{cedula_filter.strip()}'"
        if nombre_filter.strip():
            query += f" AND pr.nombre_completo ILIKE '%{nombre_filter.strip()}%'"
        
        try:
            # Ejecutar la consulta y obtener los datos en un DataFrame
            df = conn.execute(query).fetch_df()
            
            if df.empty:
                st.warning("No se encontraron registros con esos filtros.")
            else:
                # Extraer la información común (asumiendo que cédula y nombre son iguales en todos los registros)
                info_comun = df.iloc[0][['cedula', 'nombre_completo']].to_dict()
                
                # Crear el diccionario de contexto:
                # 'registros' contendrá la lista de registros (por ejemplo, los vínculos laborales)
                # 'cedula' y 'nombre_completo' se envían de forma separada para mostrarlos una única vez en la plantilla.
                context = {
                    "registros": df.to_dict(orient="records"),
                    "cedula": info_comun.get("cedula", ""),
                    "nombre_completo": info_comun.get("nombre_completo", "")
                }
                
                st.markdown("## Información completa de los Registros:")
                st.dataframe(df)
                
                # Cargar la plantilla de Word y renderizarla con el contexto
                # En la plantilla, muestra {{ cedula }} y {{ nombre_completo }} fuera del bloque de iteración
                # Y usa un bloque {% for item in registros %} para mostrar el resto de la información.
                doc = DocxTemplate("templates/plantillaEjemplo.docx")
                doc.render(context)
                
                # Guardar el documento en un buffer en memoria
                import io
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                
                st.success("Documento generado exitosamente.")
                
                st.download_button(
                    label="Descargar Documento",
                    data=buffer,
                    file_name="documentoAutomatizado.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"Error al generar el documento: {e}")
    
    conn.close()
    
# Función principal que gestiona la navegación entre páginas
def main():
    st.sidebar.title("Menú de Páginas - Aplicación Web")
    pagina_seleccionada = st.sidebar.selectbox("Selecciona una página", 
                                               ["Generación de Consultas", "Generación de Word Automatizado"])
    
    if pagina_seleccionada == "Generación de Consultas":
        pagina_consultas()
    elif pagina_seleccionada == "Generación de Word Automatizado":
        pagina_generacion_word()

if __name__ == "__main__":
    main()
