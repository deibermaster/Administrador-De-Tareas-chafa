from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QSpinBox, QComboBox, QTableWidget,
                             QTableWidgetItem, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import obtener_procesos, guardar_procesos, crear_archivo_descripcion
from api_client import APIClient
from process_thread import ProcessSimulator

class CatalogUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Procesos")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Controles superiores
        controls_layout = QHBoxLayout()
        
        # Nombre de catálogo
        catalogo_layout = QHBoxLayout()
        catalogo_layout.addWidget(QLabel("Nombre Catálogo:"))
        self.nombre_catalogo = QLineEdit()
        self.nombre_catalogo.setPlaceholderText("Ej: Procesos_2025")
        catalogo_layout.addWidget(self.nombre_catalogo)
        controls_layout.addLayout(catalogo_layout)
        
        # Número de procesos
        num_proc_layout = QHBoxLayout()
        num_proc_layout.addWidget(QLabel("Número de procesos:"))
        self.num_procesos = QSpinBox()
        self.num_procesos.setRange(1, 20)
        self.num_procesos.setValue(5)
        num_proc_layout.addWidget(self.num_procesos)
        controls_layout.addLayout(num_proc_layout)
        
        # Criterio de selección
        criterio_layout = QHBoxLayout()
        criterio_layout.addWidget(QLabel("Criterio:"))
        self.criterio = QComboBox()
        self.criterio.addItems(["CPU", "Memoria"])
        criterio_layout.addWidget(self.criterio)
        controls_layout.addLayout(criterio_layout)
        
        # Quantum
        quantum_layout = QHBoxLayout()
        quantum_layout.addWidget(QLabel("Quantum (ms):"))
        self.quantum = QSpinBox()
        self.quantum.setRange(1, 1000)
        self.quantum.setValue(10)
        quantum_layout.addWidget(self.quantum)
        controls_layout.addLayout(quantum_layout)
        
        # Botón de actualización
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.clicked.connect(self.actualizar_procesos)
        controls_layout.addWidget(self.btn_actualizar)
        
        layout.addLayout(controls_layout)
        
        # Tabla de procesos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(7)
        self.tabla.setHorizontalHeaderLabels([
            "Catálogo", "Nombre Catálogo", "PID", "Nombre",
            "Usuario", "Descripción", "Prioridad"
        ])
        layout.addWidget(self.tabla)
        
        # Botones inferiores
        bottom_layout = QHBoxLayout()
        
        self.btn_guardar = QPushButton("Guardar JSON")
        self.btn_guardar.clicked.connect(self.guardar_json)
        bottom_layout.addWidget(self.btn_guardar)
        
        self.btn_enviar = QPushButton("Enviar al Servidor")
        self.btn_enviar.clicked.connect(self.enviar_servidor)
        bottom_layout.addWidget(self.btn_enviar)
        
        self.btn_simular = QPushButton("Simular actividad")
        self.btn_simular.clicked.connect(self.simular_actividad)
        bottom_layout.addWidget(self.btn_simular)
        
        layout.addLayout(bottom_layout)
        
        # Inicializar API client
        self.api_client = APIClient()
        
        # Cargar procesos iniciales
        self.actualizar_procesos()
        
        self.simuladores = []  # Lista para guardar los hilos

    def actualizar_procesos(self):
        n = self.num_procesos.value()
        criterio = self.criterio.currentText().lower()
        
        try:
            procesos = obtener_procesos(n, criterio)
            self.mostrar_procesos(procesos)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al obtener procesos: {str(e)}")

    def mostrar_procesos(self, procesos):
        self.tabla.setRowCount(len(procesos))
        for i, proc in enumerate(procesos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(proc["catalogo"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(proc["nombre_catalogo"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(proc["pid"])))
            self.tabla.setItem(i, 3, QTableWidgetItem(proc["nombre"]))
            self.tabla.setItem(i, 4, QTableWidgetItem(proc["usuario"]))
            self.tabla.setItem(i, 5, QTableWidgetItem(proc["descripcion"]))
            self.tabla.setItem(i, 6, QTableWidgetItem(str(proc["prioridad"])))
            
            # Crear archivo de descripción
            crear_archivo_descripcion(proc)

    def guardar_json(self):
        try:
            procesos = []
            for i in range(self.tabla.rowCount()):
                proceso = {
                    "catalogo": int(self.tabla.item(i, 0).text()),
                    "nombre_catalogo": self.tabla.item(i, 1).text(),
                    "pid": int(self.tabla.item(i, 2).text()),
                    "nombre": self.tabla.item(i, 3).text(),
                    "usuario": self.tabla.item(i, 4).text(),
                    "descripcion": self.tabla.item(i, 5).text(),
                    "prioridad": int(self.tabla.item(i, 6).text()),
                    "quantum": self.quantum.value(),
                    "estado": "Listo"
                }
                procesos.append(proceso)
            data = {
                "catalogo": self.nombre_catalogo.text() or "Catalogo_Default",
                "procesos": procesos
            }
            guardar_procesos(data, "data/procesos_catalogados.json")
            QMessageBox.information(self, "Éxito", "Procesos guardados correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar procesos: {str(e)}")

    def enviar_servidor(self):
        try:
            procesos = []
            for i in range(self.tabla.rowCount()):
                proceso = {
                    "catalogo": int(self.tabla.item(i, 0).text()),
                    "nombre_catalogo": self.tabla.item(i, 1).text(),
                    "pid": int(self.tabla.item(i, 2).text()),
                    "nombre": self.tabla.item(i, 3).text(),
                    "usuario": self.tabla.item(i, 4).text(),
                    "descripcion": self.tabla.item(i, 5).text(),
                    "prioridad": int(self.tabla.item(i, 6).text())
                }
                procesos.append(proceso)
            
            response = self.api_client.enviar_procesos(procesos)
            if response and response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Procesos enviados correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudo enviar los procesos al servidor")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al enviar procesos: {str(e)}")

    def simular_actividad(self):
        # Detener simulaciones previas si existen
        for sim in self.simuladores:
            sim.stop()
        self.simuladores = []
        try:
            for i in range(self.tabla.rowCount()):
                nombre_catalogo = self.tabla.item(i, 1).text()
                descripcion = self.tabla.item(i, 5).text()
                quantum = self.quantum.value()
                nombre_archivo = f"data/actividad_{nombre_catalogo}.txt"
                simulador = ProcessSimulator(nombre_archivo, descripcion, quantum)
                simulador.start()
                self.simuladores.append(simulador)
            QMessageBox.information(self, "Simulación", "Simulación de actividad iniciada para todos los procesos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al simular actividad: {str(e)}") 