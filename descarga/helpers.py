import json
import datetime
import logging
import time

def writeJson(filepath, dictionary):
    """
    Escribe un diccionario en un archivo JSON.

    Args:
        filepath (str): La ruta del archivo donde se guardará el JSON.
        dictionary (dict): El diccionario que se escribirá en el archivo JSON.

    Returns:
        None
    """
    with open(filepath, 'w') as fp:
        json.dump(dictionary, fp)

def readJson(filepath):
    """
    Lee un archivo JSON y devuelve su contenido como un diccionario.

    Args:
        filepath (str): La ruta del archivo JSON a leer.

    Returns:
        dict: El contenido del archivo JSON.
    """
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    return data

def getRemotePath(rootPath, product, datetimeIn):
    """
    Genera una ruta remota basada en la fecha y hora proporcionadas.

    Args:
        rootPath (str): La ruta raíz del archivo remoto.
        product (str): El nombre del producto que se está descargando.
        datetimeIn (datetime.datetime): La fecha y hora usadas para construir la ruta.

    Returns:
        tuple: Una tupla que contiene la ruta generada (str), el año (str), el día del año (str), y la hora (str).
    """
    year = str(datetimeIn.year)
    day_of_year = datetimeIn.strftime('%j')
    hour = datetimeIn.strftime('%H')

    outPath = rootPath + product + '/' + year + '/' + day_of_year + '/' + hour + '/'

    return outPath, year, day_of_year, hour

def createLogger(attachedFile, logPath):
    """
    Crea un logger para registrar eventos en un archivo de registro.

    Args:
        attachedFile (str): Nombre del archivo o módulo asociado con el logger.
        logPath (str): Ruta donde se guardará el archivo de registro.

    Returns:
        tuple: Una tupla que contiene el logger (logging.Logger) y el manejador del archivo de registro (logging.FileHandler).
    """
    logger = logging.getLogger(attachedFile)
    logger.setLevel(logging.DEBUG)
    log_name = datetime.date.today().strftime('%Y%m%d_%H%M%S') + '_logfile.log'
    logfile_name = logPath + log_name
    logfile = logging.FileHandler(logfile_name)
    logfile.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)

    return logger, logfile


