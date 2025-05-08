# Laboratorio de Monitoreo de Procesos

Este proyecto consiste en una aplicación de monitoreo de procesos que incluye tanto una interfaz web como una aplicación de escritorio. Permite monitorear y analizar procesos del sistema en tiempo real, con visualizaciones interactivas y almacenamiento de datos.

## Estructura del Proyecto

```
.
├── web_app/               # Aplicación web
│   ├── app.py            # Punto de entrada de la aplicación web
│   ├── simulador.py      # Simulador de procesos
│   ├── proceso.py        # Clase de proceso
│   ├── storage/          # Almacenamiento de datos
│   └── templates/        # Plantillas HTML
│
├── desktop_app/          # Aplicación de escritorio
│   ├── main.py           # Punto de entrada de la aplicación
│   ├── api_client.py     # Cliente API
│   ├── api_server.py     # Servidor API
│   ├── process_thread.py # Hilo de procesamiento
│   ├── utils.py          # Utilidades
│   ├── data/            # Datos de la aplicación
│   └── gui/             # Interfaz gráfica
│
└── requirements.txt      # Dependencias del proyecto
```

## Requisitos del Sistema

### Requisitos Mínimos
- Python 3.8 o superior
- 4GB de RAM
- 1GB de espacio en disco
- Conexión a Internet (para actualizaciones y características en línea)

### Dependencias
Las siguientes dependencias se instalarán automáticamente:
- psutil==5.9.8 (Monitoreo de procesos del sistema)
- Flask==3.0.2 (Servidor web)
- requests==2.31.0 (Cliente HTTP)
- PyQt5==5.15.10 (Interfaz gráfica)
- plotly==5.18.0 (Visualizaciones)

## Instalación Detallada

### 1. Preparación del Entorno

#### Windows
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
.venv\Scripts\activate

# Actualizar pip
python -m pip install --upgrade pip
```

#### Linux/Mac
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Actualizar pip
python -m pip install --upgrade pip
```

### 2. Instalación de Dependencias
```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### 3. Verificación de la Instalación
```bash
# Verificar que Flask está instalado
python -c "import flask; print(flask.__version__)"

# Verificar que PyQt5 está instalado
python -c "import PyQt5; print(PyQt5.QtCore.QT_VERSION_STR)"
```

## Guía de Uso Detallada

### Servidor API

#### 1. Iniciar el Servidor API
```bash
# Navegar al directorio de la aplicación de escritorio
cd desktop_app

# Iniciar el servidor API
python api_server.py
```

El servidor API se iniciará en `http://localhost:5001` por defecto.

#### 2. Endpoints del Servidor API
- `GET /api/status`: Verificar estado del servidor
- `GET /api/processes`: Obtener lista de procesos
- `GET /api/processes/<pid>`: Obtener detalles de un proceso específico
- `POST /api/processes/<pid>/kill`: Terminar un proceso
- `GET /api/stats`: Obtener estadísticas del sistema

#### 3. Configuración del Servidor
El servidor API puede configurarse modificando las siguientes variables en `api_server.py`:
```python
HOST = 'localhost'  # Cambiar para permitir conexiones remotas
PORT = 5001        # Cambiar si el puerto está en uso
DEBUG = False      # Activar para desarrollo
```

#### 4. Integración con la Aplicación de Escritorio
La aplicación de escritorio se conecta automáticamente al servidor API local. Si necesitas cambiar la configuración:
1. Abrir `desktop_app/api_client.py`
2. Modificar la URL base:
```python
BASE_URL = 'http://localhost:5001'  # Cambiar si el servidor está en otro puerto
```

### Aplicación Web

#### 1. Iniciar el Servidor
```bash
cd web_app
python app.py
```

El servidor se iniciará en `http://localhost:5000`

#### 2. Características de la Interfaz Web
- **Dashboard Principal**: Muestra una visión general de los procesos activos
- **Gráficos en Tiempo Real**: Visualización de uso de CPU y memoria
- **Lista de Procesos**: Tabla detallada con todos los procesos
- **Filtros y Búsqueda**: Permite filtrar procesos por nombre, PID o uso de recursos

#### 3. Endpoints de la API
- `GET /api/processes`: Lista todos los procesos
- `GET /api/processes/<pid>`: Información detallada de un proceso
- `GET /api/stats`: Estadísticas del sistema
- `POST /api/processes/<pid>/kill`: Termina un proceso

### Aplicación de Escritorio

#### 1. Iniciar la Aplicación
```bash
cd desktop_app
python main.py
```

#### 2. Características de la Interfaz de Escritorio
- **Ventana Principal**: Muestra procesos y estadísticas
- **Gráficos Interactivos**: Visualizaciones actualizadas en tiempo real
- **Panel de Control**: Controles para filtrar y gestionar procesos
- **Exportación de Datos**: Guardar estadísticas en CSV o JSON

## Solución de Problemas Comunes

### 1. Errores de Instalación

#### Error: "Microsoft Visual C++ 14.0 or greater is required"
```bash
# Solución: Instalar Visual C++ Build Tools
# Descargar e instalar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### Error: "Could not find a version that satisfies the requirement"
```bash
# Solución: Actualizar pip y setuptools
python -m pip install --upgrade pip setuptools wheel
```

### 2. Errores de Ejecución

#### Error: "Address already in use"
```bash
# Solución: Cambiar el puerto en app.py
# Editar la línea: app.run(port=5001)  # Cambiar a otro puerto
```

#### Error: "ModuleNotFoundError: No module named 'X'"
```bash
# Solución: Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### 3. Problemas de Rendimiento

#### La aplicación está lenta
- Cerrar otros programas que consuman muchos recursos
- Reducir la frecuencia de actualización en la configuración
- Limpiar el caché de datos en la carpeta `storage/`

#### Errores de memoria
- Aumentar el límite de memoria en la configuración
- Reducir el número de procesos monitoreados
- Reiniciar la aplicación periódicamente

### 4. Problemas con el Servidor API

#### Error: "Connection refused"
```bash
# Verificar que el servidor API está corriendo
python desktop_app/api_server.py

# Verificar que no hay otro proceso usando el puerto
# Windows:
netstat -ano | findstr :5001
# Linux/Mac:
lsof -i :5001
```

#### Error: "API Server not responding"
- Verificar que el servidor API está corriendo
- Comprobar la configuración de la URL en `api_client.py`
- Verificar que no hay firewall bloqueando la conexión

#### Error: "Port already in use"
```bash
# Cambiar el puerto en api_server.py
PORT = 5002  # Usar un puerto diferente
```

## Mantenimiento

### Limpieza de Datos
```bash
# Limpiar datos antiguos
cd web_app
python -c "from storage import cleanup; cleanup()"
```

### Actualización
```bash
# Actualizar dependencias
pip install -r requirements.txt --upgrade
```

### Respaldo
```bash
# Hacer backup de los datos
cd web_app/storage
tar -czf backup_$(date +%Y%m%d).tar.gz *
```

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Soporte

Para reportar problemas o solicitar ayuda:
1. Revisar la sección de Solución de Problemas
2. Buscar en los issues existentes
3. Crear un nuevo issue con:
   - Descripción detallada del problema
   - Pasos para reproducir
   - Logs de error
   - Versión del sistema y dependencias 