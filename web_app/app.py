from flask import Flask, request, jsonify, render_template
from simulador import SimuladorRoundRobin
import json
import os

app = Flask(__name__)
procesos_cargados = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/procesos', methods=['POST'])
def cargar_procesos():
    global procesos_cargados
    procesos_cargados = request.json
    
    # Guardar procesos en archivo
    os.makedirs('storage', exist_ok=True)
    with open('storage/procesos.json', 'w') as f:
        json.dump(procesos_cargados, f, indent=4)
    
    return {"status": "procesos cargados"}, 200

@app.route('/api/simular', methods=['GET'])
def simular():
    th = int(request.args.get("th", 100))
    quantum = int(request.args.get("quantum", 2))
    
    if not procesos_cargados:
        return {"error": "No hay procesos cargados"}, 400
    
    sim = SimuladorRoundRobin(procesos_cargados, th, quantum)
    resultados = sim.ejecutar()
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True) 