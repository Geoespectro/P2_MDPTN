# Documentación del Test del Procesador

Este documento describe cómo funciona el script de pruebas unitarias para el procesador, detallando cada una de las pruebas realizadas y los pasos que sigue el script para garantizar la correcta configuración del entorno de pruebas.

## Estructura del Test
El script de prueba utiliza la biblioteca `unittest` para definir un conjunto de pruebas que verifican la infraestructura y el comportamiento básico del procesador. El script consta de las siguientes funciones principales:

### 1. `setUp()`
Esta función se ejecuta antes de cada prueba y se encarga de configurar el entorno necesario. En particular, realiza los siguientes pasos:
- **Creación de directorios temporales**: Crea los directorios `test_inbox` y `test_workdir` si no existen.
- **Creación de archivos de prueba**: Crea tres archivos NetCDF de prueba (`test_file_0.nc`, `test_file_1.nc`, `test_file_2.nc`) en el directorio `test_inbox`.
- **Creación de archivo de configuración**: Genera un archivo de configuración simulado (`test_SNM_dict.conf`) con parámetros necesarios para las pruebas.

### 2. `tearDown()`
Esta función se ejecuta después de cada prueba y se encarga de limpiar el entorno de prueba, eliminando todos los archivos y directorios temporales creados en `setUp()`. Esto asegura que cada prueba se ejecute en un entorno limpio y sin interferencias de pruebas anteriores.

- **Eliminación de archivos NetCDF**: Borra los archivos `.nc` creados en `test_inbox`.
- **Eliminación de archivos generados**: Borra cualquier archivo generado en `test_workdir`.
- **Eliminación de directorios y archivo de configuración**: Elimina los directorios `test_inbox` y `test_workdir`, así como el archivo de configuración (`test_SNM_dict.conf`).

## Pruebas Definidas

### 1. `test_inicializar_acumulado()`
Esta prueba verifica que la inicialización del acumulado se realice correctamente:
- **Verificación de archivos NetCDF**: Comprueba que en el directorio `test_inbox` existan exactamente tres archivos `.nc` después de la configuración del entorno. Esto asegura que los archivos necesarios para el procesamiento estén disponibles.

### 2. `test_creacion_directorios()`
Esta prueba verifica la creación correcta de los directorios temporales:
- **Verificación de directorios**: Comprueba que los directorios `test_inbox` y `test_workdir` existan. Esto es esencial para garantizar que el entorno de trabajo esté bien preparado antes de ejecutar el procesador.

### 3. `test_configuracion_cargada()`
Esta prueba verifica que el archivo de configuración se haya creado y cargado correctamente:
- **Verificación de la configuración**: Comprueba que el archivo de configuración (`test_SNM_dict.conf`) contenga la clave `"km_per_degree"` y que su valor sea correcto (`111.32`). Esta prueba asegura que los parámetros necesarios para el procesamiento estén disponibles y correctamente definidos.

## Cómo Ejecutar el Test
Para ejecutar el script de prueba, simplemente utiliza Python para correr el archivo `.py` que contiene los tests. Puedes hacerlo con el siguiente comando:

```bash
/home/juan/anaconda3/envs/Goes/bin/python "ruta/a/tu/archivo_de_prueba.py"
```

El resultado indicará cuántas pruebas se ejecutaron y si pasaron todas correctamente.

## Resultados Esperados
Si todos los componentes del entorno están bien configurados, el resultado debería mostrar que las tres pruebas (`test_inicializar_acumulado`, `test_creacion_directorios`, `test_configuracion_cargada`) se ejecutaron correctamente sin errores.

```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

Este resultado indica que:
- Los archivos NetCDF se crearon correctamente.
- Los directorios temporales existen como se esperaba.
- El archivo de configuración se cargó correctamente y contiene los parámetros necesarios.

## Conclusión
El script de prueba está diseñado para garantizar que el entorno del procesador esté bien preparado antes de realizar el procesamiento real de los datos. Esto incluye verificar la existencia de archivos, la creación de directorios y la correcta carga de la configuración. Este enfoque ayuda a evitar errores en las etapas iniciales del procesamiento y asegura que el procesador pueda trabajar con la infraestructura adecuada.



