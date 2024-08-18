import psutil
import platform
import requests
import socket
import json
from datetime import datetime

def obtener_info_sistema():
    # Información del procesador
    cpu_info = {
        "nombre": platform.processor(),
        "nucleos": psutil.cpu_count(logical=True),
        "frecuencia": psutil.cpu_freq().current
    }

    # Listado de procesos corriendo
    procesos = [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'username'])]

    # Usuarios con sesión abierta
    usuarios = [u.name for u in psutil.users()]

    # Nombre y versión del SO
    sistema_operativo = {
        "nombre": platform.system(),
        "version": platform.version()
    }

    # Recolección de información
    info = {
        "cpu_info": cpu_info,
        "procesos": procesos,
        "usuarios": usuarios,
        "sistema_operativo": sistema_operativo,
        "ip": socket.gethostbyname(socket.gethostname()),
        "timestamp": datetime.now().isoformat()
    }

    return info

def enviar_info(api_url, info):
    response = requests.post(api_url, json=info)
    if response.status_code == 200:
        print("Información enviada correctamente.")
    else:
        print("Error al enviar la información:", response.status_code)

if __name__ == "__main__":
    api_url = "http://<IP_DEL_SERVIDOR>:5000/upload"  # Aca va IP del Serv
    info_sistema = obtener_info_sistema()
    enviar_info(api_url, info_sistema)