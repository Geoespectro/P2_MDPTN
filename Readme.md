
# 🌐 MDPTN v0.1 - Proyecto de Descarga y Procesamiento de Datos Satelitales GOES-16 para Mapas de Permanencia de Topes Nubosos

**MDPTN v0.1** es un sistema diseñado para automatizar la descarga y el procesamiento de datos satelitales **GOES-16**, facilitando la generación de mapas de permanencia de topes nubosos. Ideal para usuarios y desarrolladores enfocados en análisis climático, teledetección y meteorología.
---

## 📖 Descripción General

El proyecto consta de dos módulos principales:
1. **📥 Descarga de Datos**: Utiliza `goes16Download.py` para descargar imágenes desde el servidor S3 de NOAA.
2. **⚙️ Procesamiento de Datos**: Genera productos visuales a partir de las imágenes descargadas mediante `main.py`, incluyendo una matriz de acumulación y visualizaciones dinámicas.

---

## 📂 Estructura del Proyecto

```plaintext
.
├── descarga
│   ├── goes16Download.py       # Script principal para descargar imágenes GOES-16
│   ├── helpers.py              # Funciones auxiliares para la descarga
│   └── setup.json              # Configuración de la descarga
├── docs
│   ├── descarga_doc.md         # Documentación del módulo de descarga
│   ├── docs_test               # Documentación de pruebas unitarias
│   │   ├── test_descarga.md    # Pruebas del módulo de descarga
│   │   └── test_procesador.md  # Pruebas del módulo de procesamiento
│   ├── procesador_doc.md       # Documentación del módulo de procesamiento
│   └── run_all_doc.md          # Documentación del script lanzador
├── Procesador
│   ├── data                    # Configuraciones y datos auxiliares (shapefiles, etc.)
│   │   ├── conf                # Configuración de parámetros del procesamiento
│   │   │   └── SMN_dict.conf   # Archivo de configuración principal
│   │   ├── grids               # Archivos de coordenadas
│   │   │   ├── g16_lats_8km.txt
│   │   │   └── g16_lons_8km.txt
│   │   ├── logo                # Recursos gráficos
│   │   │   └── logo.png
│   │   └── shp                 # Shapefiles para la generación de mapas
│   │       ├── limite_internacional2
│   │       ├── limite_interprovincial2
│   │       └── shapefiles
│   │           └── natural_earth/physical
│   ├── inbox                   # Directorio de entrada para las imágenes descargadas
│   ├── main.py                 # Script principal para el procesamiento
│   ├── src                     # Código auxiliar para el procesamiento
│   │   └── helpers.py          # Funciones auxiliares del módulo de procesamiento
│   └── workdir                 # Resultados del procesamiento
├── test
│   ├── test_descarga.py        # Pruebas unitarias del módulo de descarga
│   └── test_procesador.py      # Pruebas unitarias del módulo de procesamiento
├── Readme.md                   # Este archivo
├── requirements.txt            # Dependencias del proyecto
├── run_all.py                  # Script lanzador para ejecutar descarga y procesamiento
```

---

## 🛠️ Requisitos del Proyecto

### Requisitos del Sistema:
- **Python 3.8+**

### Bibliotecas de Python necesarias:
- `boto3`, `s3fs`, `numpy`, `netCDF4`, `matplotlib`, `cartopy`, `watchdog`, `imageio`

Instala las dependencias ejecutando:
```bash
pip install -r requirements.txt
```

---

## 🚀 Instrucciones de Uso

### 1️⃣ Configuración Inicial
- Edita `descarga/setup.json` para definir parámetros como:
  - Fecha de inicio
  - Bandas a descargar
  - Rutas de almacenamiento
- Ajusta las configuraciones de visualización en `Procesador/data/conf/SMN_dict.conf`.

### 2️⃣ Ejecución del Proyecto
Ejecuta el script principal:
```bash
python run_all.py
```
Esto iniciará simultáneamente los módulos de descarga y procesamiento.

---

## 📊 Detalles del Procesamiento

El módulo de procesamiento realiza:
- **Inicialización del Acumulado**: Genera una matriz inicial a partir de las imágenes en `inbox/` que cuantifica la permanencia de nubes.
- **Procesamiento Continuo**: Actualiza la matriz de acumulación con cada nueva imagen detectada en el directorio de entrada.
- **Visualización**: Genera representaciones en PNG y GIF que muestran la evolución de la cobertura nubosa, destacando el tiempo de permanencia.

---

## ✨ Mejoras Futuras

Propuestas para futuras versiones:
- **⚡ Optimización**: Paralelismo en el procesamiento para mayor velocidad.
- **🔄 Resiliencia**: Almacenamiento incremental del acumulado.
- **📊 Dashboards**: Visualización interactiva de los resultados.

---

## 👫 Contribuir

¡Colabora con este proyecto! Sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -m 'Descripción del cambio'`).
4. Envía los cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## 📝 Licencia

Este proyecto está abierto a la colaboración.

---

## 📩 Contacto

Para dudas o sugerencias:
- **Juan Carlos Quinteros**, **Pedro Rivolta**

¡Gracias por utilizar **MDPTN v0.1**! Créditos a GOES-16 y los repositorios de AWS.





