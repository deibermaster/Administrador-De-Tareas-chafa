import psutil
import json
import os

# Obtiene los n procesos más activos según el criterio (CPU o memoria)
def obtener_procesos(n, criterio):
    """
    Obtiene los n procesos con mayor consumo según el criterio especificado.
    
    Args:
        n (int): Número de procesos a obtener
        criterio (str): 'cpu' o 'memoria'
    
    Returns:
        list: Lista de diccionarios con información de los procesos
    """
    procesos = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        try:
            info = p.info
            # Selecciona el valor según el criterio
            if criterio == 'cpu':
                valor = info['cpu_percent'] if info['cpu_percent'] is not None else 0
            else:
                valor = info['memory_info'].rss if info['memory_info'] is not None else 0
            procesos.append((valor, info))
        except:
            continue
    
    # Ordena los procesos por el valor seleccionado (descendente)
    procesos.sort(key=lambda x: x[0], reverse=True)
    seleccionados = procesos[:n]
    resultado = []
    
    for i, (_, info) in enumerate(seleccionados):
        username = info['username'] if info['username'] is not None else ''
        # Prioridad: 0 = expulsivo, 1 = no expulsivo
        prioridad = 0 if username and 'system' not in username.lower() else 1
        resultado.append({
            "catalogo": i,
            "nombre_catalogo": f"proc_{i}",
            "pid": info['pid'],
            "nombre": info['name'],
            "usuario": username,
            "descripcion": f"Descripción del proceso {info['name']}",
            "prioridad": prioridad
        })
    return resultado

# Guarda la lista de procesos en un archivo JSON
def guardar_procesos(procesos, archivo):
    """
    Guarda la lista de procesos en un archivo JSON.
    
    Args:
        procesos (list): Lista de procesos a guardar
        archivo (str): Ruta del archivo donde guardar
    """
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    with open(archivo, 'w') as f:
        json.dump(procesos, f, indent=4)

# Crea un archivo de texto con la descripción del proceso
def crear_archivo_descripcion(proceso):
    """
    Crea un archivo de texto con la descripción del proceso.
    
    Args:
        proceso (dict): Información del proceso
    """
    nombre_archivo = f"data/descripcion_{proceso['nombre_catalogo']}.txt"
    with open(nombre_archivo, 'w') as f:
        f.write(proceso['descripcion']) 