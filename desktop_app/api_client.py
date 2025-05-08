import requests
import json

class APIClient:
    """
    Cliente para comunicarse con el backend web mediante peticiones HTTP.
    Permite enviar procesos y obtener resultados de simulación.
    """
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def enviar_procesos(self, procesos):
        """
        Envía la lista de procesos al servidor web.
        
        Args:
            procesos (list): Lista de procesos a enviar
            
        Returns:
            requests.Response: Respuesta del servidor
        """
        url = f"{self.base_url}/api/procesos"
        try:
            response = requests.post(url, json=procesos)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar procesos: {e}")
            return None

    def obtener_resultados_simulacion(self, th=100, quantum=2):
        """
        Obtiene los resultados de la simulación del servidor.
        
        Args:
            th (int): Tiempo de hardware
            quantum (int): Quantum para Round Robin
            
        Returns:
            dict: Resultados de la simulación
        """
        url = f"{self.base_url}/api/simular"
        try:
            response = requests.get(url, params={"th": th, "quantum": quantum})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener resultados: {e}")
            return None 