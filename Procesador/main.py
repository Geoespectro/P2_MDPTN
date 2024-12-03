import os
import json
import logging
import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import matplotlib
import glob
import imageio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from PIL import Image

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.helpers import GetCroppedImage, GetPlotObject, GetCalibratedImage, LoadDictionary, AddImageFoot, AddLogo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/conf/SMN_dict.conf")
confData = LoadDictionary(json_file_path)
workdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), confData['workdir'])
inboxdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), confData['inbox'])
gif_path = os.path.join(workdir, 'conae.gif')

if not os.path.exists(workdir):
    os.makedirs(workdir)
if not os.path.exists(inboxdir):
    os.makedirs(inboxdir)

logging.info(f"Directorio de trabajo: {workdir}")
logging.info(f"Directorio de entrada: {inboxdir}")

T_U = -53  # Umbral de temperatura de brillo
num_images_initial = 6  # Número de imágenes para acumulado inicial
num_images_max = 144  # Número de imágenes para 24 horas

# Inicialización de matrices globales
accum_data = None
image_queue = []



def actualizar_gif(imagenes, gif_path):
    """
    Actualiza el GIF con una lista de imágenes y una duración específica entre cuadros usando Pillow.

    :param imagenes: Lista de rutas a las imágenes.
    :param gif_path: Ruta del archivo GIF de salida.
    """
    # Leer la duración desde el archivo de configuración o fijar un valor predeterminado
    frame_duration = confData.get('gif_frame_duration', 1.0)  # Valor predeterminado: 1.0 segundos si no está definido
    frame_duration_ms = int(frame_duration * 1000)  # Convertir segundos a milisegundos

    logging.info(f"Configurando duración por cuadro en {frame_duration} segundos.")

    try:
        # Cargar todas las imágenes usando PIL
        frames = [Image.open(imagen) for imagen in imagenes]

        if frames:
            # Crear el GIF usando PIL, especificando la duración entre cuadros
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=frame_duration_ms,  # Duración en milisegundos
                loop=0  # Repetir infinitamente
            )
            logging.info(f"GIF generado correctamente: {gif_path}")
        else:
            logging.warning("No se encontraron imágenes para generar el GIF.")
    except Exception as e:
        logging.error(f"Error al generar el GIF: {e}")



def inicializar_acumulado():
    global accum_data, image_queue

    files = sorted(glob.glob(os.path.join(inboxdir, '*.nc')))[:num_images_initial]

    if not files:
        logging.warning("No se encontraron archivos iniciales para procesar.")
        return

    for image_file in files:
        logging.info(f'Procesando archivo inicial {image_file}')
        netCDFread = Dataset(image_file, 'r')
        region = 'ARG'
        if region == 'SuA_ARG':
            extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
        elif region == 'SuA':
            extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
        elif region == 'ARG':
            extent = [confData['argentina_lon_W'], confData['argentina_lon_E'], confData['argentina_lat_S'], confData['argentina_lat_N']]
        else:
            logging.error('Debe seleccionar una de las siguientes áreas: SuA_ARG, SuA, ARG, custom!')
            return

        img_extent, img_indexes = GetCroppedImage(netCDFread, 
                                    extent[0] + confData['delta_lon_W_for_graph'],
                                    extent[1],
                                    extent[2] + confData['delta_lat_S_for_graph'],
                                    extent[3] + confData['delta_lat_N_for_graph'])

        imagedata = netCDFread.variables['Rad'][img_indexes[2]:img_indexes[3], img_indexes[0]:img_indexes[1]][::1,::1]
        image_cal, _ = GetCalibratedImage(netCDFread, imagedata)
        del imagedata

        new_data = np.where(image_cal < T_U, 1, 0)

        if accum_data is None:
            accum_data = np.zeros_like(new_data)
        
        accum_data += new_data
        image_queue.append(new_data)
        logging.info(f"Archivo {image_file} procesado y acumulado inicial actualizado.")

def update_accumulation(new_image_path):
    global accum_data, image_queue

    logging.info(f'Procesando nueva imagen {new_image_path}')
    netCDFread = Dataset(new_image_path, 'r')

    region = 'ARG'
    if region == 'SuA_ARG':
        extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
    elif region == 'SuA':
        extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
    elif region == 'ARG':
        extent = [confData['argentina_lon_W'], confData['argentina_lon_E'], confData['argentina_lat_S'], confData['argentina_lat_N']]
    else:
        logging.error('Debe seleccionar una de las siguientes áreas: SuA_ARG, SuA, ARG, custom!')
        return

    img_extent, img_indexes = GetCroppedImage(netCDFread, 
                                extent[0] + confData['delta_lon_W_for_graph'],
                                extent[1],
                                extent[2] + confData['delta_lat_S_for_graph'],
                                extent[3] + confData['delta_lat_N_for_graph'])

    imagedata = netCDFread.variables['Rad'][img_indexes[2]:img_indexes[3], img_indexes[0]:img_indexes[1]][::1,::1]
    image_cal, _ = GetCalibratedImage(netCDFread, imagedata)
    del imagedata

    new_data = np.where(image_cal < T_U, 1, 0)

    if len(image_queue) >= num_images_max:
        oldest_data = image_queue.pop(0)
        accum_data -= oldest_data

    accum_data += new_data
    image_queue.append(new_data)

    # Guardar el nuevo acumulado
    np.save(os.path.join(workdir, 'accum.npy'), accum_data)

    # Crear y guardar la imagen actualizada
    accum_hours = accum_data * (10 / 60.0)  # Cada imagen representa 10 minutos

    crs = ccrs.Geostationary(central_longitude=netCDFread.variables['goes_imager_projection'].longitude_of_projection_origin, satellite_height=netCDFread.variables['goes_imager_projection'].perspective_point_height)

    fig = plt.figure(clear=True)
    fig.set_size_inches(np.shape(accum_hours)[1] / confData['figure_resolution_dpi'], np.shape(accum_hours)[0] / confData['figure_resolution_dpi'])
    ax = GetPlotObject(confData, extent)

    # Fondo blanco
    ax.set_facecolor('white')

    # Ajustar la escala de colores para 24 horas
    cmap = matplotlib.colors.ListedColormap(['white', 'lightblue', 'blue', 'green', 'yellow', 'orange', 'red', 'darkred'])
    bounds = [0, 2, 4, 6, 8, 12, 16, 20, 24]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    img = ax.imshow(accum_hours, transform=crs, extent=img_extent, origin='upper', cmap=cmap, norm=norm, aspect='auto')
    cbar = plt.colorbar(img, ax=ax, fraction=0.02, pad=0.04, boundaries=bounds, ticks=bounds)
    cbar.set_label('Horas de permanencia')

    # Obtener la fecha y hora del archivo NetCDF
    timestamp = netCDFread.time_coverage_start
    # Ajustar el formato de fecha y hora para eliminar las fracciones de segundo
    if '.' in timestamp:
        timestamp = timestamp.split('.')[0] + 'Z'
    formatted_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y-%H:%Mhs')
    title = f"Mapa de permanencia de topes de nubes {formatted_timestamp}"
    AddImageFoot(ax, title, size=8.0)
    AddLogo(ax)

    output_path = os.path.join(workdir, f"permanencia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    plt.savefig(output_path, dpi=confData['figure_resolution_dpi'])
    logging.info(f"Imagen guardada en {output_path}")

    imagenes_existentes = sorted(glob.glob(os.path.join(workdir, '*.png')))
    actualizar_gif(imagenes_existentes, gif_path)


class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.nc'):
            logging.info("Esperando nueva imagen para la generación del mapa.")
            update_accumulation(event.src_path)
            logging.info("Generando mapa.")
            logging.info("Mapa generado. Esperando nueva imagen para la generación del mapa.")

if __name__ == "__main__":
    logging.info("Inicio del procesamiento de archivos.")
    inicializar_acumulado()
    observer = Observer()
    event_handler = NewImageHandler()
    observer.schedule(event_handler, inboxdir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    logging.info("Procesamiento de archivos completado.")





