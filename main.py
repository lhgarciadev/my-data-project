from src.create_tables import create_tables
from src.pipeline import run_pipeline

if __name__ == "__main__":
    print("Creando tablas...")
    create_tables()

    print("\nEjecutando pipeline...")
    run_pipeline()
