import threading
import time
import os

class ProcessSimulator(threading.Thread):
    """
    Simula la actividad de un proceso escribiendo su descripción carácter por carácter en un archivo,
    respetando el quantum (en milisegundos). Permite pausar y reanudar la simulación.
    """
    def __init__(self, nombre_archivo, descripcion, quantum_ms, pausa_event=None):
        super().__init__()
        self.nombre_archivo = nombre_archivo  # Archivo donde se escribe la descripción
        self.descripcion = descripcion        # Texto a escribir
        self.quantum_ms = quantum_ms          # Quantum en milisegundos
        self.pausa_event = pausa_event or threading.Event()  # Evento para pausar
        self._stop_event = threading.Event()  # Evento para detener

    def run(self):
        """
        Ejecuta la simulación: escribe la descripción carácter a carácter, esperando quantum_ms entre cada uno.
        Si se llama a stop(), termina la simulación. Si se llama a pausar(), se detiene hasta reanudar().
        """
        with open(self.nombre_archivo, 'w', encoding='utf-8') as f:
            for char in self.descripcion:
                if self._stop_event.is_set():
                    break
                while self.pausa_event.is_set():
                    time.sleep(0.1)  # Espera mientras está pausado
                f.write(char)
                f.flush()
                time.sleep(self.quantum_ms / 1000.0)  # Espera el quantum

    def stop(self):
        """Detiene la simulación."""
        self._stop_event.set()

    def pausar(self):
        """Pausa la simulación."""
        self.pausa_event.set()

    def reanudar(self):
        """Reanuda la simulación si estaba pausada."""
        self.pausa_event.clear() 