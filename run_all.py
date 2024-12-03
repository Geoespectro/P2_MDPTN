import subprocess
import concurrent.futures
import time
import os

# Función para ejecutar el script de descarga
def ejecutar_descarga():
    """
    Ejecuta el script de descarga 'goes16Download.py' utilizando subprocess.
    
    Si ocurre un error durante la ejecución, se imprime un mensaje de error.
    """
    try:
        subprocess.run(['python', 'descarga/goes16Download.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error durante la descarga: {e}")

# Función para verificar si hay suficientes imágenes en la carpeta de entrada
def hay_imagenes_suficientes(inbox_path, num_requerido):
    """
    Verifica si hay suficientes imágenes en la carpeta de entrada para comenzar el procesamiento.
    
    :param inbox_path: Ruta a la carpeta de entrada.
    :param num_requerido: Número requerido de imágenes para iniciar el procesamiento.
    :return: Booleano indicando si hay suficientes imágenes.
    """
    archivos = [f for f in os.listdir(inbox_path) if f.endswith('.nc')]
    return len(archivos) >= num_requerido

# Función para ejecutar el script de procesamiento
def ejecutar_procesamiento():
    """
    Ejecuta el script de procesamiento 'main.py' utilizando subprocess.
    
    Si ocurre un error durante la ejecución, se imprime un mensaje de error.
    """
    try:
        subprocess.run(['python', 'Procesador/main.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    """
    Punto de entrada principal del script. Ejecuta la descarga y el procesamiento de imágenes concurrentemente.
    """
    inbox_path = os.path.join('Procesador', 'inbox')
    num_imagenes_requeridas = 6  # Cambia a 6 para pruebas rápidas

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Ejecutar la descarga concurrentemente
        future_descarga = executor.submit(ejecutar_descarga)
        
        # Verificar continuamente si hay suficientes imágenes para procesar
        while not hay_imagenes_suficientes(inbox_path, num_imagenes_requeridas):
            print("Esperando a que haya suficientes imágenes en la carpeta de entrada...")
            time.sleep(30)  # Verificar cada 30 segundos

        # Una vez que hay suficientes imágenes, ejecutar el procesamiento
        print("Suficientes imágenes encontradas, iniciando el procesamiento.")
        future_procesamiento = executor.submit(ejecutar_procesamiento)
        
        # Esperar a que ambas tareas se completen
        concurrent.futures.wait([future_descarga, future_procesamiento])




















