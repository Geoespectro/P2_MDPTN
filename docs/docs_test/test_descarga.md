## **Documentación del Test de Conexión al Repositorio S3**

### **Descripción General**

El archivo `test_descarga.py` es un test automatizado diseñado para verificar que el proyecto **MDTN v0.1** pueda conectarse correctamente al bucket remoto **S3** del NOAA. Este bucket almacena los datos necesarios para las operaciones del proyecto.

---

### **Objetivo**

El objetivo principal del test es garantizar:
- Que el sistema pueda establecer una conexión anónima al bucket remoto `s3://noaa-goes16/`.
- Detectar problemas de conectividad o acceso antes de ejecutar otras operaciones dependientes del bucket.

---

### **Configuración**

#### **Entorno Requerido**
- **Lenguaje:** Python 3.7+
- **Librerías Necesarias:**
  - `unittest`: Para estructurar las pruebas.
  - `s3fs`: Para conectarse al bucket S3 de forma anónima.

#### **Estructura de Archivos**
El archivo `test_descarga.py` debe estar ubicado en la carpeta `test` dentro del proyecto. La estructura esperada del proyecto es la siguiente:

```
P1_MDTN/
├── descarga/
│   ├── helpers.py
├── test/
│   └── test_descarga.py
├── ...
```

#### **Variables Configuradas en el Test**
- **`s3_bucket`:** Dirección del bucket S3 (`s3://noaa-goes16/`).
- **`temp_path` y `final_path`:** Carpetas temporales definidas, pero no utilizadas en este test.

---

### **Descripción del Test**

#### **Nombre del Test**
`test_connection_s3`

#### **Lógica**
1. Establece una conexión al bucket S3 utilizando `s3fs.S3FileSystem` en modo anónimo (`anon=True`).
2. Intenta listar los archivos del bucket mediante `fs.ls(self.s3_bucket)`.
3. Si la conexión es exitosa, imprime:
   ```
   ✓ Conexión exitosa al repositorio S3
   ```
4. Si la conexión falla, marca el test como fallido y muestra el error.

#### **Métodos Utilizados**
- **`setUpClass`**:
  Configura las variables iniciales y prepara el entorno necesario para la prueba.
- **`tearDownClass`**:
  Limpia las carpetas temporales creadas durante la ejecución del test.
- **`test_connection_s3`**:
  Implementa la lógica principal para verificar la conectividad con el bucket.

---

### **Ejemplo de Ejecución**

#### **Comando para Ejecutar el Test**
```bash
python test/test_descarga.py
```

#### **Salida Esperada**
Si la conexión es exitosa:
```plaintext
Ejecutando pruebas para la lógica de descarga...

test_connection_s3 (__main__.TestDescarga)
Prueba de conexión al bucket S3. ... ✓ Conexión exitosa al repositorio S3
ok

----------------------------------------------------------------------
Ran 1 test in 1.331s

OK
```

Si la conexión falla:
```plaintext
Ejecutando pruebas para la lógica de descarga...

test_connection_s3 (__main__.TestDescarga)
Prueba de conexión al bucket S3. ... ✗ Fallo al conectar con el repositorio S3: [Motivo del error]

======================================================================
FAIL: test_connection_s3 (__main__.TestDescarga)
Fallo al conectar con el repositorio S3: [Motivo del error]

----------------------------------------------------------------------
Ran 1 test in 0.123s

FAILED (errors=1)
```

---

### **Casos de Uso**

Este test es útil para:
1. Verificar la conectividad al bucket remoto antes de ejecutar procesos que dependan de datos almacenados en él.
2. Detectar problemas de configuración de red o credenciales para acceso al S3.
3. Validar el estado del repositorio S3 en entornos de desarrollo, pruebas o producción.

---

### **Conclusión**

El archivo `test_descarga.py` es un test simple pero esencial para garantizar que el proyecto pueda conectarse correctamente al bucket S3. Este test minimiza el riesgo de interrupciones relacionadas con problemas de conectividad y asegura que el entorno esté configurado correctamente.

--- 

