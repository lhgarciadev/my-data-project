import psycopg2

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'data_pipeline',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}

# Sentencias SQL para crear las tablas con restricciones de unicidad
create_transactions_table = """
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    price NUMERIC,
    user_id INTEGER,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_transaction UNIQUE (timestamp, price, user_id)
);
"""

create_stats_table = """
CREATE TABLE IF NOT EXISTS stats (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    batch_number INTEGER,
    total_rows BIGINT,
    avg_price NUMERIC,
    min_price NUMERIC,
    max_price NUMERIC,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_stat UNIQUE (file_name, batch_number)
);
"""

def create_tables():
    """
    Crea las tablas necesarias en la base de datos.
    """
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_transactions_table)
                print("Tabla 'transactions' creada con éxito.")
                cursor.execute(create_stats_table)
                print("Tabla 'stats' creada con éxito.")
                conn.commit()
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
