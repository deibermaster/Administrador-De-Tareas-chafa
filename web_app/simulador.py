from proceso import Proceso
import time

class SimuladorRoundRobin:
    """
    Simulador del algoritmo Round Robin para planificación de procesos.
    Gestiona colas de listos, ejecución y terminados, y calcula métricas.
    """
    def __init__(self, procesos_data, th, quantum):
        self.th = th  # Tiempo de hardware (no usado directamente, pero puede influir en la lógica)
        self.quantum = quantum  # Quantum de ejecución
        self.procesos = []  # Lista de procesos (objetos Proceso)
        self.tiempo = 0  # Tiempo global de simulación
        self.resultados = []  # Resultados finales
        self._cargar_procesos(procesos_data)

    def _cargar_procesos(self, procesos_data):
        """
        Carga los procesos desde una lista de diccionarios y los convierte en objetos Proceso.
        Asigna tiempos de llegada consecutivos.
        """
        self.procesos = []
        t_llegada = 0
        for p in procesos_data:
            proc = Proceso(
                pid=p.get('pid'),
                nombre=p.get('nombre'),
                usuario=p.get('usuario'),
                descripcion=p.get('descripcion'),
                prioridad=p.get('prioridad', 1),
                quantum=self.quantum,
                estado="Listo",
                t_llegada=t_llegada
            )
            self.procesos.append(proc)
            t_llegada += 1

    def ejecutar(self):
        """
        Ejecuta la simulación Round Robin:
        - Gestiona colas de listos, ejecución y terminados.
        - Aplica quantum, calcula ráfaga, turnaround, tiempos de llegada y finalización.
        - Maneja la expulsión de procesos según prioridad.
        Devuelve una lista de diccionarios con los resultados de cada proceso.
        """
        cola_listos = self.procesos.copy()
        cola_ejecucion = []
        cola_terminados = []
        tiempo_global = 0
        while cola_listos or cola_ejecucion:
            # Si no hay en ejecución, toma el siguiente de listos
            if not cola_ejecucion and cola_listos:
                proc = cola_listos.pop(0)
                proc.cambiar_estado("Ejecución")
                cola_ejecucion.append(proc)

            if cola_ejecucion:
                proc = cola_ejecucion.pop(0)
                ejecutado = proc.ejecutar_quantum()
                tiempo_global += ejecutado
                if proc.terminado():
                    proc.cambiar_estado("Terminado")
                    proc.t_final = tiempo_global
                    proc.turnaround = proc.t_final - proc.t_llegada
                    cola_terminados.append(proc)
                else:
                    # Si es expulsivo (prioridad 0), vuelve a listos
                    if proc.prioridad == 0:
                        proc.cambiar_estado("Listo")
                        cola_listos.append(proc)
                    else:
                        # No expulsivo, sigue en ejecución
                        proc.cambiar_estado("Ejecución")
                        cola_ejecucion.append(proc)
            else:
                # Si no hay nada en ejecución, avanza el tiempo
                tiempo_global += 1
        # Guardar resultados
        self.resultados = [p.to_dict() for p in cola_terminados]
        return self.resultados 