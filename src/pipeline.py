import psycopg2
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'data_pipeline',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}

BATCH_SIZE = 5  # Tamaño del batch

def process_file(file_path):
    """
    Procesa un archivo CSV en batches, verifica valores faltantes y actualiza la base de datos con las estadísticas.
    """
    batch_iter = pd.read_csv(file_path, parse_dates=["timestamp"], chunksize=BATCH_SIZE)

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                for batch_idx, batch_df in enumerate(batch_iter, start=1):
                    # Identificar valores faltantes
                    missing_values = batch_df.isnull().sum().sum()
                    if missing_values > 0:
                        print(f"Advertencia: Se encontraron {missing_values} valores faltantes en el batch {batch_idx} del archivo {file_path.name}.")

                    # Convertir tipos de datos a formatos nativos de Python
                    batch_df = batch_df.astype({
                        'timestamp': 'datetime64[ns]',
                        'price': float,
                        'user_id': int
                    })

                    # Insertar registros nuevos en transactions
                    new_records_count = 0
                    for _, row in batch_df.iterrows():
                        cursor.execute(
                            """
                            SELECT 1 FROM transactions
                            WHERE timestamp = %s AND price = %s AND user_id = %s
                            """,
                            (row['timestamp'], row['price'], row['user_id'])
                        )
                        if cursor.fetchone():
                            continue

                        cursor.execute(
                            """
                            INSERT INTO transactions (timestamp, price, user_id, load_date)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (row['timestamp'], row['price'], row['user_id'], datetime.now())
                        )
                        new_records_count += 1

                    # Si no hay registros nuevos, omitir estadísticas
                    if new_records_count == 0:
                        print(f"No se encontraron registros nuevos en el batch {batch_idx} del archivo {file_path.name}.")
                        continue

                    # Calcular estadísticas incrementales
                    total_rows = len(batch_df)
                    avg_price = float(batch_df["price"].mean())
                    min_price = float(batch_df["price"].min())
                    max_price = float(batch_df["price"].max())

                    # Insertar estadísticas en stats
                    cursor.execute(
                        """
                        INSERT INTO stats (file_name, batch_number, total_rows, avg_price, min_price, max_price, load_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (file_path.name, batch_idx, total_rows, avg_price, min_price, max_price, datetime.now())
                    )
                    print(f"Estadísticas procesadas para el batch {batch_idx}: total_rows={total_rows}, avg_price={avg_price:.2f}, min_price={min_price}, max_price={max_price}")

                conn.commit()
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")

def query_stats():
    """
    Consulta las estadísticas globales en la base de datos y las imprime.
    """
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Consulta de estadísticas acumuladas
                cursor.execute("""
                    SELECT SUM(total_rows), AVG(avg_price), MIN(min_price), MAX(max_price)
                    FROM stats
                """)
                result = cursor.fetchone()
                print(f"Total Filas: {result[0]}, Promedio Precio: {result[1]:.2f}, Precio Mínimo: {result[2]}, Precio Máximo: {result[3]}")
    except Exception as e:
        print(f"Error al consultar estadísticas: {e}")

def run_pipeline():
    """
    Procesa todos los archivos CSV en la carpeta data.
    """
    data_dir = Path(__file__).parent.parent / "data"
    files = sorted(f for f in data_dir.iterdir() if f.suffix == ".csv" and "validation" not in f.name)

    for file in files:
        print(f"Procesando archivo: {file.name}")
        process_file(file)

    # Consultar estadísticas después de procesar los archivos principales
    print("Estadísticas globales después de procesar los archivos principales:")
    query_stats()

    # Procesar archivo de validación
    print("Procesando archivo de validación...")
    process_file(data_dir / "validation.csv")

    # Consultar estadísticas después de procesar validation.csv
    print("Estadísticas globales después de procesar validation.csv:")
    query_stats()
