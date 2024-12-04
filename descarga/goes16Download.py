import logging
import time
import json
import s3fs
import datetime
import os
import shutil
import helpers as help
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.DEBUG)

# Obtiene la ruta absoluta al directorio del script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construye la ruta absoluta al archivo de configuración
setup_file = os.path.join(script_dir, 'setup.json')

# Leo el archivo de configuración
data = help.readJson(setup_file)

# Extraigo los paths y cantidad de bandas
main_path = os.path.dirname(os.path.abspath(__file__))  # Directorio del script
image_path = os.path.join(main_path, '..', 'Procesador', 'inbox')
temp_path = os.path.join(main_path, 'temp')  # Carpeta temporal para descargas
db_path = os.path.join(main_path, data['db_path'])
log_path = os.path.join(main_path, data['log_path'])
bands = data['bands']  # Bandas a descargar
product = data['product']
timeout = data['timeout']
dates = data['dates']  # Fechas para realizar la descarga
start_hour = data.get('start_hour', '00:00')  # Hora de inicio para realizar la descarga
end_date = data.get('end_date', None)  # Fecha de fin para realizar la descarga
end_hour = data.get('end_hour', None)  # Hora de fin para realizar la descarga
max_workers = data.get('max_workers', 1)  # Número de descargas paralelas

# Verificar y crear carpetas necesarias
for path in [image_path, temp_path, db_path, log_path]:
    if not os.path.exists(path):
        os.makedirs(path)

# Configuración del archivo de logging
logger, logfile = help.createLogger(__file__, log_path)

# Configuro las credenciales anónimas para acceder al servidor de imágenes
logger.info('Configurando las credenciales de acceso al repositorio remoto')
fs = s3fs.S3FileSystem(anon=True)

# Verificar conexión a S3
while True:
    try:
        fs.ls('s3://noaa-goes16/')
        logger.info('Conexión a S3 exitosa, reanudando descargas')
        break
    except Exception as e:
        logger.error('Error en la conexión a S3: ' + str(e))
        time.sleep(60)

# Crear o leer el archivo de base de datos
db_file = os.path.join(db_path, 'download_db.json')
if not os.path.exists(db_file):
    logger.info('Creando el archivo de base de datos con los archivos descargados')
    download_db = {}
    help.writeJson(db_file, download_db)
else:
    try:
        logger.info('Leyendo la base de datos de archivos descargados')
        download_db = help.readJson(db_file)
    except json.JSONDecodeError:
        logger.error('El archivo de base de datos estaba vacío o corrupto, inicializándolo de nuevo.')
        download_db = {}
        help.writeJson(db_file, download_db)

# Obtener la última fecha y hora de la imagen descargada
def get_last_downloaded_time():
    """
    Obtiene la última fecha y hora de la imagen descargada de la base de datos.

    Returns:
        datetime.datetime o None: La última fecha y hora descargada, o None si no hay registros.
    """
    last_time = None
    for year in sorted(download_db.keys()):
        for day in sorted(download_db[year].keys()):
            for hour in sorted(download_db[year][day].keys()):
                if len(download_db[year][day][hour]) == 6:
                    last_time = datetime.datetime.strptime(f"{year}{day}{hour}", "%Y%j%H")
    return last_time

# Definir la fecha y hora inicial para la descarga
last_time = get_last_downloaded_time()
if last_time:
    logger.info(f'Continuando desde la última fecha y hora descargada: {last_time}')
else:
    logger.info('No se encontró ninguna descarga previa. Iniciando desde el principio.')

# Convertir la fecha y hora de inicio
start_datetime = datetime.datetime.strptime(f"{dates[0]} {start_hour}", "%Y-%m-%d %H:%M")

# Convertir la fecha y hora de fin si está disponible
if end_date and end_hour:
    end_datetime = datetime.datetime.strptime(f"{end_date} {end_hour}", "%Y-%m-%d %H:%M") if end_hour else datetime.datetime.strptime(f"{end_date} 23:59", "%Y-%m-%d %H:%M")
else:
    end_datetime = None

# Definir la función de descarga de archivos
def download_file(f, temp_path, final_path, year, day, hour):
    """
    Descarga un archivo desde el repositorio remoto a una ubicación temporal y luego lo mueve a la ubicación final.

    Args:
        f (str): La ruta del archivo remoto a descargar.
        temp_path (str): La ruta temporal donde se almacenará el archivo durante la descarga.
        final_path (str): La ruta final donde se almacenará el archivo después de la descarga.
        year (str): Año de la descarga.
        day (str): Día del año de la descarga.
        hour (str): Hora de la descarga.

    Returns:
        None
    """
    image_name = f.split('/')[-1]
    if not image_name or len(image_name.strip()) == 0:
        logger.error('Nombre de archivo inválido para descargar. Omitiendo...')
        return
    
    band_number = int(image_name.split('_')[1].split('M6C')[-1])
    if band_number in bands:
        if f not in download_db.get(year, {}).get(day, {}).get(hour, []):
            logger.info(f'Descargando archivo para {hour}:00 ' + image_name)
            print(f'Descargando archivo: {image_name}')
            temp_file_path = os.path.join(temp_path, image_name)
            final_file_path = os.path.join(final_path, image_name)
            try:
                fs.get(f, temp_file_path)
            except Exception as e:
                logger.error(f'Error al descargar el archivo {image_name}: {str(e)}')
                return
            
            # Verificación de integridad
            if os.path.getsize(temp_file_path) > 0:
                shutil.move(temp_file_path, final_file_path)
                if year not in download_db:
                    download_db[year] = {}
                if day not in download_db[year]:
                    download_db[year][day] = {}
                if hour not in download_db[year][day]:
                    download_db[year][day][hour] = []
                download_db[year][day][hour].append(f)
                # Guardar el archivo JSON inmediatamente después de cada descarga
                help.writeJson(db_file, download_db)
            else:
                logger.error('Archivo descargado incompleto: ' + image_name)
                os.remove(temp_file_path)

# Bucle principal para cada fecha y hora
current_datetime = last_time + datetime.timedelta(hours=1) if last_time else start_datetime
retry_timeout = timeout
max_retries = 5  # Número máximo de intentos antes de aumentar el tiempo de espera
retry_count = 0
max_wait_time = 1800  # Máximo tiempo de espera después de varios intentos fallidos (30 minutos)

while True:
    # Verificar si se ha alcanzado la fecha y hora de fin
    if end_datetime and current_datetime > end_datetime:
        logger.info('Se ha alcanzado la fecha y hora de fin. Proceso de descarga completado.')
        print('Proceso de descarga completado.')
        break
    else:
        logger.info('Descarga iniciada en modo continuo. Manteniéndose en espera para descargas futuras.')
        print('Manteniéndose en espera para futuras descargas.')
    
    year, day, hour = current_datetime.strftime("%Y"), current_datetime.strftime("%j"), current_datetime.strftime("%H")
    remotePath, year, day, hour = help.getRemotePath('s3://noaa-goes16/', product, current_datetime)

    if year not in download_db:
        download_db[year] = {}
    if day not in download_db[year]:
        download_db[year][day] = {}
    if hour not in download_db[year][day]:
        download_db[year][day][hour] = []

    elapsed_time = 0
    while len(download_db[year][day][hour]) < 6:
        try:
            logger.info(f'Obteniendo lista de archivos del repositorio remoto para la fecha {current_datetime.strftime("%Y-%m-%d")}, hora {hour}')
            currentFileList = list(fs.ls(remotePath, refresh=True))
            expected_files = [f for f in currentFileList if f.split('/')[-1].startswith(f"OR_ABI-L1b-RadF-M6C13_G16_s{year}{day}{hour}")]
            logger.info(f'Se encontraron {len(expected_files)} archivos disponibles en el repositorio para la hora {hour}')

            if len(expected_files) != 0:
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [executor.submit(download_file, f, temp_path, image_path, year, day, hour) for f in expected_files]
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            logger.error('Error durante la descarga de un archivo: ' + str(e))
                            print(f'Error durante la descarga de un archivo: ' + str(e))

                if len(download_db[year][day][hour]) == 6:
                    logger.info('Todas las imágenes para la hora {} han sido descargadas.'.format(hour))
                    retry_count = 0  # Reiniciar el contador de intentos
                    break
                else:
                    logger.info('Esperando la próxima imagen a ser descargada. Manteniéndose en espera para descargar la próxima imagen disponible.')
            else:
                logger.info(f'Aún no hay archivos en el remoto para descargar para la hora {hour} del día {current_datetime.strftime("%Y-%m-%d")}, esperando la próxima imagen.')
                print(f'Aún no hay archivos en el remoto para descargar para la hora {hour} del día {current_datetime.strftime("%Y-%m-%d")}, esperando la próxima imagen.')
                retry_count += 1
                if retry_count >= max_retries:
                    logger.warning(f'Se alcanzó el número máximo de intentos ({max_retries}) sin éxito. Aumentando el tiempo de espera y continuando.')
                    time.sleep(min(retry_timeout * 2, max_wait_time))
                    retry_count = 0
                    continue
            
            help.writeJson(db_file, download_db)
            time.sleep(timeout)
            elapsed_time += timeout

            if elapsed_time > 600:
                logger.warning(f'Se alcanzó el tiempo máximo de espera para la hora {hour}, pero aún no se descargaron todas las imágenes. Continuando en espera...')
                elapsed_time = 0

        except Exception as e:
            logger.error('Error inesperado durante la descarga: ' + str(e))
            print(f'Error inesperado durante la descarga: {str(e)}')

    current_datetime += datetime.timedelta(hours=1)

print("\n" + "="*40 + "\nDESCARGA COMPLETADA\n" + "="*40)



