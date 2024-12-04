# Guía Explicativa del Módulo de Procesamiento de Imágenes Satelitales GOES-16

## 1. Descripción General del Proceso de Procesamiento

El módulo `main.py` tiene como objetivo principal el procesamiento de datos satelitales provenientes del satélite GOES-16. Este módulo está diseñado para leer archivos netCDF de radiancia de la banda 13 del sensor ABI y procesar las imágenes para obtener un mapa de permanencia de topes de nubes. Además, genera visualizaciones en forma de imágenes y GIFs que permiten observar la acumulación y evolución de las nubes sobre el área de interés. La lógica del módulo se estructura en varios pasos, desde la configuración inicial hasta la generación de las salidas visuales.

La estructura del procesamiento consiste en los siguientes pasos:

1. **Configuración Inicial**: Se leen los parámetros necesarios desde un archivo de configuración para definir los directorios de trabajo, las áreas geográficas y otros parámetros relevantes.
2. **Inicialización del Acumulado**: Se procesan las primeras imágenes encontradas para crear un acumulado inicial que permitirá analizar la permanencia de topes de nubes.
3. **Procesamiento Continuo**: Cada vez que se recibe una nueva imagen, esta se procesa, se añade al acumulado y se actualizan las visualizaciones generadas.
4. **Generación de Resultados**: Se generan archivos de imagen (PNG) y un GIF que muestra la evolución de las condiciones atmosféricas.

## 2. Explicación Detallada de Cada Parte del Código

### 2.1. Configuración Inicial

- **Archivo de Configuración (`SMN_dict.conf`)**: Contiene los parámetros necesarios para el proceso, como la extensión de las áreas geográficas (Argentina, Sudamérica), la resolución de las imágenes, y las rutas de los directorios utilizados.
- **Directorios de Trabajo**: Se configuran los directorios de entrada (`inboxdir`) y de trabajo (`workdir`) donde se almacenan los resultados del procesamiento, tales como las matrices de acumulación y las imágenes generadas.
- **Logger**: Se inicializa el `logger` para registrar eventos relevantes durante el proceso, facilitando el monitoreo y depuración.

### 2.2. Inicialización del Acumulado

- **Acumulado Inicial**: Se seleccionan las primeras seis imágenes encontradas en el directorio de entrada (`inboxdir`). Estas imágenes se utilizan para inicializar la matriz de acumulación (`accum_data`). Cada píxel de las imágenes es comparado con un umbral de temperatura de brillo (`T_U`), y los valores que cumplen con la condición se añaden al acumulado.
- **Definición del Área Geográfica**: Dependiendo de la región configurada (‘ARG’, ‘SuA’, etc.), se determinan los índices correspondientes a la sección de la imagen que se va a procesar. La función `GetCroppedImage` se utiliza para recortar la imagen al área deseada.
- **Calibración de la Imagen**: Se convierte la radiancia de la imagen en temperatura utilizando la función `GetCalibratedImage`.

### 2.3. Procesamiento Continuo

- **Manejo de Nuevas Imágenes**: Cada vez que se detecta una nueva imagen en el directorio de entrada, el proceso de acumulación se actualiza. Si la cola de imágenes alcanza el máximo definido de 144 imágenes (equivalente a 24 horas de datos, ya que cada imagen corresponde a 10 minutos), la más antigua es eliminada y se resta de la matriz de acumulación.
- **Calibración y Acumulación**: Al igual que en la inicialización, la nueva imagen se calibra y se acumula si cumple con el umbral de temperatura.
- **Almacenamiento del Acumulado**: La matriz de acumulación se guarda en el archivo `accum.npy` cada vez que se actualiza, lo que permite retomar el proceso en caso de interrupción.

### 2.4. Generación de Resultados

- **Visualización de la Acumulación**: Se genera una imagen en formato PNG que muestra la cantidad de horas en las que se han mantenido topes de nubes fríos sobre cada píxel. La imagen se crea utilizando la biblioteca `matplotlib` y la función `GetPlotObject`, que se encarga de preparar el objeto de trama y dibujar los límites geográficos.
- **Escala de Colores**: Se utiliza una escala de colores con valores que van desde el blanco (cero horas de permanencia) hasta el rojo oscuro (más de 24 horas de permanencia).
- **Generación del GIF**: Las imágenes generadas se combinan en un GIF que se actualiza continuamente, permitiendo visualizar la evolución de las condiciones atmosféricas en el área de estudio.

## 3. Componentes Auxiliares del Procesador

### 3.1. Archivo `helpers.py`

El archivo `helpers.py` contiene funciones auxiliares que son fundamentales para el procesamiento de las imágenes. Entre estas funciones se encuentran:

- **`GetCroppedImage`**: Recorta las imágenes netCDF para obtener la región de interés según los parámetros configurados.
- **`GetPlotObject`**: Crea el objeto de la trama que se utiliza para graficar las imágenes, configurando los límites geográficos, líneas de costa, y límites provinciales y nacionales.
- **`GetCalibratedImage`**: Convierte los valores de radiancia a temperatura de brillo, permitiendo diferenciar entre áreas con nubes frías y áreas despejadas.
- **`AddImageFoot` y `AddLogo`**: Agregan un pie de imagen y un logotipo a las visualizaciones generadas para incluir información relevante como la fecha y el origen de los datos.

## 4. Camino de la Información en el Proceso de Procesamiento
1. **Inicio**: El script se inicia y se lee la configuración desde `SMN_dict.conf`.
2. **Inicialización del Acumulado**: Se procesan las primeras seis imágenes disponibles para generar la matriz de acumulación inicial.
3. **Procesamiento Continuo**: A medida que se reciben nuevas imágenes, estas se acumulan, se recalculan las matrices de permanencia, y se generan nuevas visualizaciones.
4. **Generación de Resultados**: Se guardan las imágenes PNG y se actualiza el GIF que muestra la evolución de las nubes en el área de interés.

## 5. Áreas en las que se podria mejorar el codigo
- **Modularización**: Dividir algunas funciones del archivo `main.py` en funciones más pequeñas y reutilizables podría facilitar el mantenimiento del código.
- **Paralelismo en el Procesamiento**: Al igual que en el módulo de descarga, se podría implementar procesamiento paralelo para acelerar el cálculo del acumulado cuando se tienen muchas imágenes disponibles.
- **Almacenamiento Incremental del Acumulado**: Implementar una manera más eficiente de almacenar y actualizar el acumulado podría reducir el uso de memoria y mejorar la robustez del proceso.


