# Documentación del Script Lanzador `run_all.py`

## 1. Descripción General del Script

El script `run_all.py` tiene como objetivo ejecutar de manera concurrente las dos lógicas principales del proyecto: la descarga de los datos satelitales (`goes16Download.py`) y el procesamiento de estos datos (`main.py`). Para ello, utiliza la clase `ThreadPoolExecutor` de la biblioteca `concurrent.futures`, permitiendo que ambas tareas se ejecuten en paralelo, optimizando el flujo de trabajo y asegurando que el procesamiento pueda realizarse mientras se continúa con la descarga de datos.

Este script permite que el sistema de descarga y procesamiento trabaje de manera coordinada, garantizando que ambos procesos se ejecuten de forma continua sin necesidad de intervención manual, lo cual es ideal para un entorno donde la adquisición y análisis de datos se realice de manera automatizada.

## 2. Explicación Detallada de la Lógica del Código

### **2.1. Ejecución del Script de Descarga**
- **Función `ejecutar_descarga()`**:
  - Esta función ejecuta el script `goes16Download.py` utilizando `subprocess.run()`. Se utiliza `check=True` para que, si el script termina con un error, se lance una excepción (`CalledProcessError`).
  - **Manejo de Errores**: En caso de que ocurra un error durante la descarga, se imprime un mensaje indicando el fallo. El script de descarga ya tiene implementado un mecanismo que permite reanudar el proceso automáticamente si se pierde la conexión a la red, lo cual hace que la descarga sea más resiliente.

### **2.2. Ejecución del Script de Procesamiento**
- **Función `ejecutar_procesamiento()`**:
  - Ejecuta el script `main.py` del procesador en un bucle continuo, lo que permite que el procesamiento se realice repetidamente, procesando nuevos datos cuando estén disponibles.
  - Tras cada ejecución, el script espera 60 segundos antes de volver a intentar el procesamiento. Esto ayuda a garantizar que los nuevos archivos descargados tengan tiempo de ser detectados y procesados adecuadamente.
  - **Manejo de Errores**: Si ocurre un error durante el procesamiento, se captura y se imprime un mensaje indicando el problema. No obstante, el bucle continúa, lo que garantiza que se siga intentando el procesamiento en intervalos regulares.

### **2.3. Ejecución Concurrente de Descarga y Procesamiento**
- **Uso de `ThreadPoolExecutor`**:
  - Se utiliza `ThreadPoolExecutor` para ejecutar ambas funciones (`ejecutar_descarga` y `ejecutar_procesamiento`) de manera concurrente.
  - **Futuros (`future_descarga` y `future_procesamiento`)**: Cada función se ejecuta en un hilo separado. Esto permite que la descarga y el procesamiento de archivos se realicen simultáneamente, lo cual es fundamental para optimizar el flujo de trabajo y evitar cuellos de botella.
  - **Sincronización**: Se utiliza `concurrent.futures.wait()` para esperar a que ambas tareas finalicen. Debido al bucle infinito en `ejecutar_procesamiento()`, la tarea de procesamiento nunca termina, lo que significa que el script seguirá funcionando indefinidamente a menos que se interrumpa manualmente.

## 3. Camino de la Información en el Proceso
1. **Inicio**: El script `run_all.py` se inicia y llama a las funciones `ejecutar_descarga()` y `ejecutar_procesamiento()` utilizando `ThreadPoolExecutor` para ejecutarlas de manera concurrente.
2. **Descarga de Datos**: `ejecutar_descarga()` inicia la descarga de los datos satelitales utilizando el script `goes16Download.py`. Si ocurre un fallo en la conexión, el script está diseñado para reanudar la descarga cuando sea posible.
3. **Procesamiento de Datos**: `ejecutar_procesamiento()` monitorea continuamente el directorio de entrada, procesando los nuevos archivos a medida que están disponibles, y se asegura de que el procesamiento se realice en intervalos regulares de 60 segundos.
4. **Ejecución Concurrente**: Gracias a `ThreadPoolExecutor`, ambos procesos (descarga y procesamiento) se ejecutan simultáneamente, permitiendo que el flujo de trabajo sea continuo y eficiente.
5. **Terminación Manual**: El script seguirá ejecutándose indefinidamente hasta que se detenga manualmente.


## 4. Resumen y Conclusión

El script `run_all.py` es crucial para la ejecución concurrente de la descarga y el procesamiento de los datos satelitales GOES-16. Permite que ambos procesos se realicen de manera continua, asegurando la disponibilidad de datos procesados en tiempo real.