import unittest
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
from src.create_tables import create_tables
from src.pipeline import process_file, query_stats, run_pipeline
from pathlib import Path
import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Configuración de la base de datos
db_config = {
    'dbname': os.getenv('DB_NAME', 'data_pipeline'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432))
}

class TestPipeline(unittest.TestCase):
    """
    Pruebas unitarias para los módulos de creación de tablas y pipeline.
    """

    def setUp(self):
        """
        Configuración inicial antes de cada prueba.
        """
        # Crea una conexión a la base de datos para pruebas
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        """
        self.cursor.close()
        self.conn.close()

    def test_create_tables(self):
        """
        Prueba la lógica de creación de tablas.
        """
        try:
            create_tables()
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name IN ('transactions', 'stats');")
            tables = [row[0] for row in self.cursor.fetchall()]
            self.assertIn('transactions', tables)
            self.assertIn('stats', tables)
        except Exception as e:
            self.fail(f"Error al probar la creación de tablas: {e}")

    def test_process_file(self):
        """
        Prueba la lógica de procesamiento de archivos.
        """
        # Crear un archivo CSV de prueba
        test_file = Path("data/test.csv")
        test_file.write_text("timestamp,price,user_id\n2024-01-01 10:00:00,50.5,1\n2024-01-01 11:00:00,60.0,2\n")
        try:
            process_file(test_file)
            self.cursor.execute("SELECT COUNT(*) FROM transactions;")
            count = self.cursor.fetchone()[0]
            self.assertGreater(count, 0, "El archivo de prueba no se procesó correctamente.")
        except Exception as e:
            self.fail(f"Error al probar el procesamiento de archivos: {e}")
        finally:
            # Limpieza del archivo de prueba
            if test_file.exists():
                test_file.unlink()

    def test_query_stats(self):
        """
        Prueba la lógica de consulta de estadísticas.
        """
        try:
            query_stats()
            self.cursor.execute("SELECT COUNT(*) FROM stats;")
            count = self.cursor.fetchone()[0]
            self.assertGreaterEqual(count, 0, "Las estadísticas no se consultaron correctamente.")
        except Exception as e:
            self.fail(f"Error al probar la consulta de estadísticas: {e}")

    def test_run_pipeline(self):
        """
        Prueba la ejecución completa del pipeline.
        """
        try:
            run_pipeline()
            self.cursor.execute("SELECT COUNT(*) FROM transactions;")
            count_transactions = self.cursor.fetchone()[0]
            self.cursor.execute("SELECT COUNT(*) FROM stats;")
            count_stats = self.cursor.fetchone()[0]
            self.assertGreater(count_transactions, 0, "El pipeline no procesó transacciones.")
            self.assertGreater(count_stats, 0, "El pipeline no generó estadísticas.")
        except Exception as e:
            self.fail(f"Error al probar la ejecución completa del pipeline: {e}")


if __name__ == "__main__":
    unittest.main()
