class Proceso:
    """
    Clase que modela un proceso del sistema para la simulación Round Robin.
    Incluye atributos de control de estados, ráfaga, quantum, prioridad y métricas.
    """
    def __init__(self, pid, nombre, usuario, descripcion, prioridad, quantum, estado="Listo", t_llegada=0):
        self.pid = pid  # Identificador del proceso
        self.nombre = nombre  # Nombre del proceso
        self.usuario = usuario  # Usuario propietario
        self.descripcion = descripcion  # Descripción textual
        self.prioridad = prioridad  # 0 = expulsivo, 1 = no expulsivo
        self.quantum = quantum  # Quantum asignado
        self.estado = estado  # Estado actual (Listo, Ejecución, Terminado)
        self.t_llegada = t_llegada  # Tiempo de llegada al sistema
        self.rafaga = len(descripcion) * quantum  # Tiempo total de ráfaga
        self.rafaga_restante = self.rafaga  # Ráfaga restante
        self.t_final = 0  # Tiempo de finalización
        self.turnaround = 0  # Turnaround (T. finalización - T. llegada)
        self.historial = []  # Historial de cambios de estado

    def ejecutar_quantum(self):
        """
        Ejecuta un quantum del proceso, reduciendo la ráfaga restante.
        Devuelve la cantidad de tiempo ejecutado.
        """
        if self.rafaga_restante > 0:
            ejecutado = min(self.quantum, self.rafaga_restante)
            self.rafaga_restante -= ejecutado
            self.historial.append((self.estado, ejecutado))
            return ejecutado
        return 0

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del proceso y lo registra en el historial.
        """
        self.estado = nuevo_estado
        self.historial.append((nuevo_estado, 0))

    def terminado(self):
        """
        Indica si el proceso ha terminado (ráfaga restante <= 0).
        """
        return self.rafaga_restante <= 0

    def to_dict(self):
        """
        Convierte el proceso a un diccionario para serialización o visualización.
        """
        return {
            "pid": self.pid,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "quantum": self.quantum,
            "estado": self.estado,
            "t_llegada": self.t_llegada,
            "rafaga": self.rafaga,
            "rafaga_restante": self.rafaga_restante,
            "t_final": self.t_final,
            "turnaround": self.turnaround
        } 