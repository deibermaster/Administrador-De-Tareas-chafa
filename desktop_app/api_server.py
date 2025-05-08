from flask import Flask, jsonify, Response
import json
import os
from dicttoxml import dicttoxml

app = Flask(__name__)

@app.route('/procesos', methods=['GET'])
def get_procesos():
    archivo = 'data/procesos_catalogados.json'
    if not os.path.exists(archivo):
        return jsonify({'error': 'No hay catálogo guardado'}), 404
    with open(archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
    formato = 'xml' if 'xml' in (flask_request := getattr(app, 'request', None)).args.get('formato', 'xml').lower() else 'json'
    if formato == 'json':
        return jsonify(data)
    else:
        xml = dicttoxml(data, custom_root='catalogo', attr_type=False)
        return Response(xml, mimetype='application/xml')

if __name__ == '__main__':
    app.run(port=5001, debug=True) 