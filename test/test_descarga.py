import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import shutil  # Importar shutil para eliminar carpetas y su contenido
import s3fs
import datetime

# Asegurar que el proyecto raíz esté en el PYTHONPATH para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar los módulos necesarios
from descarga.helpers import getRemotePath, writeJson, readJson


class TestDescarga(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial antes de las pruebas."""
        cls.s3_bucket = "s3://noaa-goes16/"
        cls.product = "ABI-L1b-RadF"
        cls.test_date = datetime.datetime(2024, 11, 26, 23, 0)  # Fecha de prueba
        cls.temp_path = "test_temp/"
        cls.final_path = "test_images/"
        cls.test_json = "test_db.json"

        # Crear carpetas necesarias
        os.makedirs(cls.temp_path, exist_ok=True)
        os.makedirs(cls.final_path, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Limpieza después de las pruebas."""
        # Eliminar todos los archivos y carpetas creados durante las pruebas
        if os.path.exists(cls.temp_path):
            shutil.rmtree(cls.temp_path)  # Elimina la carpeta y su contenido
        if os.path.exists(cls.final_path):
            shutil.rmtree(cls.final_path)  # Elimina la carpeta y su contenido
        if os.path.exists(cls.test_json):
            os.remove(cls.test_json)  # Elimina el archivo JSON

    def test_connection_s3(self):
        """Prueba de conexión al bucket S3."""
        fs = s3fs.S3FileSystem(anon=True)  # Conexión anónima al repositorio S3
        try:
            files = fs.ls(self.s3_bucket)  # Listar archivos en el bucket
            print("\033[92m✓ Conexión exitosa al repositorio S3\033[0m")
        except Exception as e:
            self.fail(f"\033[91m✗ Fallo al conectar con el repositorio S3: {str(e)}\033[0m")


if __name__ == "__main__":
    print("\nEjecutando pruebas para la lógica de descarga...\n")
    unittest.main(verbosity=2)



