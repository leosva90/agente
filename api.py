from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Obtener IP y fecha
    ip = data['ip']
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"{ip}_{fecha}.csv"

    # Guardar datos en CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['timestamp'], data['cpu_info'], data['procesos'], data['usuarios'], data['sistema_operativo']])

    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/data/<ip>', methods=['GET'])
def get_data(ip):
    filename = f"{ip}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    if not os.path.exists(filename):
        return jsonify({"error": "File not found"}), 404

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)