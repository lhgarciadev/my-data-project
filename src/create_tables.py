import psycopg2

# Configuración de la conexión a la base de datos
db_config = {
    'dbname': 'data_pipeline',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}

# Sentencias SQL para crear las tablas
create_transactions_table = """
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    price NUMERIC,
    user_id INTEGER
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
    max_price NUMERIC
);
"""

def create_tables():
    try:
        # Conexión a la base de datos
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # Crear tabla transactions
                cursor.execute(create_transactions_table)
                print("Tabla 'transactions' creada con éxito.")
                
                # Crear tabla stats
                cursor.execute(create_stats_table)
                print("Tabla 'stats' creada con éxito.")
                
                # Confirmar cambios
                conn.commit()
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
