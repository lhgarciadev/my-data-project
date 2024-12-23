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

5. **Configurar la base de datos**:
   - Asegúrate de que la base de datos `data_pipeline` exista en PostgreSQL.
   - Verifica que las credenciales en el archivo `src/create_tables.py` y `src/pipeline.py` sean correctas:
     ```python
     db_config = {
         'dbname': 'data_pipeline',  # Nombre de la base de datos
         'user': 'postgres',         # Usuario de la base de datos
         'password': 'password',     # Contraseña del usuario
         'host': 'localhost',        # Dirección del servidor
         'port': 5432                # Puerto del servidor
     }
     ```

6. **Colocar los datos en la carpeta correcta**:
   - Si no existe, crea una carpeta llamada `data` dentro del proyecto.
   - Copia los archivos CSV que quieres procesar (incluyendo `validation.csv`) en la carpeta `data/`.

## **Ejecución**

**Ejecutar el script principal**:
   - Ejecuta el archivo `main.py`, que creará las tablas necesarias y procesará los archivos CSV:
     ```bash
     python main.py
     ```

## **Validación de resultados**

1. **Mensajes cuando se encuentran valores faltantes**:
   - Si hay valores faltantes, el pipeline imprimirá un mensaje como:
     ```plaintext
     Advertencia: Se encontraron 3 valores faltantes en el batch 1 del archivo 2012-1.csv.
     ```

2. **Estadísticas procesadas**:
   - Cuando se procesan registros nuevos, se imprimen estadísticas como:
     ```plaintext
     Estadísticas procesadas para el batch 3: total_rows=5, avg_price=47.50, min_price=14.00, max_price=87.00
     ```

3. **Estadísticas globales**:
   - Al final del pipeline, las estadísticas globales se imprimen así:
     ```plaintext
     Total Filas: 30, Promedio Precio: 50.50, Precio Mínimo: 10.00, Precio Máximo: 100.00
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

2. **No se crean las tablas**:
   - Asegúrate de que la base de datos `data_pipeline` exista y el usuario tenga permisos para crear tablas.
