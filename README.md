# **Pipeline de procesamiento de datos**

Este proyecto implementa un pipeline para procesar archivos CSV en micro-batches, almacenar los datos en una base de datos PostgreSQL y calcular estadísticas incrementales.

## **Requisitos previos**

Antes de ejecutar el pipeline, asegúrate de cumplir con los siguientes requisitos:

1. **Instalar PostgreSQL**:
   - Asegúrate de tener PostgreSQL instalado en tu máquina y accesible desde la línea de comandos.
   - Crea una base de datos llamada `data_pipeline`.

2. **Clonar el repositorio**:
   - Clona este repositorio en tu máquina local:
     ```bash
     git clone https://github.com/lhgarciadev/my-data-project.git
     cd my-data-project
     ```

3. **Crear un entorno virtual**:
   - Crea un entorno virtual dentro de la carpeta del proyecto:
     ```bash
     python -m venv venv
     source venv/bin/activate  # En Windows: .\venv\Scripts\activate
     ```

4. **Instalar las dependencias**:
   - Instala las dependencias listadas en `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

## **Configuración**

1. **Editar la configuración de la base de datos**:
   - Abre los archivos `src/create_tables.py` y `src/pipeline.py`.
   - Actualiza la variable `db_config` con los datos de tu base de datos PostgreSQL:
     ```python
     db_config = {
         'dbname': 'data_pipeline',  # Nombre de la base de datos
         'user': 'postgres',         # Usuario de la base de datos
         'password': 'password',     # Contraseña del usuario
         'host': 'localhost',        # Dirección del servidor
         'port': 5432                # Puerto del servidor
     }
     ```

2. **Colocar los datos en la carpeta correcta**:
   - Si no existe, crea una carpeta llamada `data` dentro del proyecto.
   - Copia los archivos CSV que quieres procesar (incluyendo `validation.csv`) en la carpeta `data/`.

## **Ejecución**

Sigue estos pasos para ejecutar el pipeline:

1. **Crear las tablas**:
   - Ejecuta el script principal para crear las tablas necesarias en la base de datos:
     ```bash
     python main.py
     ```

2. **Procesar los archivos**:
   - El pipeline procesará automáticamente todos los archivos en la carpeta `data/` en orden alfabético. También incluirá el archivo `validation.csv`.

3. **Verificar las estadísticas**:
   - Durante la ejecución, el pipeline imprimirá estadísticas incrementales para cada batch procesado.
   - Al final del proceso, mostrará las estadísticas globales acumuladas después de procesar `validation.csv`.

## **Validación de resultados**

1. **Estadísticas en tiempo de ejecución**:
   - Se imprimen las estadísticas actuales para cada batch en el siguiente formato:
     ```
     Estadísticas procesadas para el batch 1: total_rows=5, avg_price=47.5, min_price=14.0, max_price=87.0
     ```

2. **Estadísticas acumuladas**:
   - Después de procesar `validation.csv`, se imprimen las estadísticas acumuladas:
     ```
     Estadísticas globales después de procesar validation.csv:
     total_rows=30, avg_price=50.5, min_price=10.0, max_price=100.0
     ```

3. **Advertencias por valores faltantes**:
   - Si hay valores faltantes, se mostrará un mensaje como este:
     ```
     Advertencia: Se encontraron 3 valores faltantes en el batch 2 del archivo 2012-1.csv.
     ```

## **Detalles técnicos**

1. **Micro-batches**:
   - Los archivos CSV se procesan en bloques de 5 filas para optimizar el uso de memoria.

2. **Base de datos**:
   - Los datos se almacenan en las tablas `transactions` y `stats` en PostgreSQL.
   - Las estadísticas incluyen el recuento total de filas, el promedio, el valor mínimo y máximo de la columna `price`.

3. **Manejo de valores faltantes**:
   - Los valores faltantes se detectan y registran, pero no se eliminan ni reemplazan.

## **Problemas comunes**

1. **Error de conexión a la base de datos**:
   - Verifica que los datos de `db_config` sean correctos.
   - Asegúrate de que el servicio PostgreSQL esté en ejecución.

2. **Error `can't adapt type 'numpy.int64'`**:
   - Este error se resolvió convirtiendo los datos a tipos nativos de Python antes de insertarlos en la base de datos, debido a los valores faltantes en los archivos CSV.

3. **No se crean las tablas**:
   - Asegúrate de que la base de datos `data_pipeline` exista y el usuario tenga permisos para crear tablas.
