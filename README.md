# Laboratorio de Monitoreo de Procesos

Este proyecto consiste en una aplicación de monitoreo de procesos que incluye tanto una interfaz web como una aplicación de escritorio.

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

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`:
  - psutil==5.9.8
  - Flask==3.0.2
  - requests==2.31.0
  - PyQt5==5.15.10
  - plotly==5.18.0

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv .venv
```

2. Activar el entorno virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Componentes Principales

### Aplicación Web (web_app)

- **app.py**: Servidor web Flask que proporciona una interfaz web para monitorear procesos
- **simulador.py**: Simula procesos del sistema para pruebas
- **proceso.py**: Implementa la lógica de gestión de procesos

### Aplicación de Escritorio (desktop_app)

- **main.py**: Punto de entrada de la aplicación de escritorio
- **api_client.py**: Cliente para comunicarse con la API
- **api_server.py**: Servidor API local
- **process_thread.py**: Manejo de procesos en segundo plano
- **utils.py**: Funciones de utilidad
- **gui/**: Componentes de la interfaz gráfica

## Uso

### Aplicación Web

1. Iniciar el servidor web:
```bash
cd web_app
python app.py
```

2. Acceder a la interfaz web en `http://localhost:5000`

### Aplicación de Escritorio

1. Iniciar la aplicación:
```bash
cd desktop_app
python main.py
```

## Características

- Monitoreo de procesos del sistema en tiempo real
- Visualización de estadísticas de procesos
- Interfaz web y de escritorio
- API REST para integración con otros sistemas
- Gráficos y visualizaciones de datos
- Almacenamiento persistente de datos

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request 