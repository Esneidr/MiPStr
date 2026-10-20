"""Tareas de ejemplo que usan los workers.

Están en un archivo aparte porque los procesos solo pueden ejecutar funciones
que se importan desde un módulo (no funciones definidas dentro de app.py).
"""
import random
import time

import numpy as np

N_LECTURAS = 2_000_000


# ---------- Tareas que ESPERAN (toma de datos) ----------
def leer_sensor(id_sensor):
    time.sleep(0.5)                                  # espera la respuesta del sensor
    return f"Sensor {id_sensor}: {random.uniform(18, 30):.1f} °C"


def leer_sensor_rapido(id_sensor):
    time.sleep(0.25)
    return f"Sensor {id_sensor}: {random.uniform(18, 30):.1f} °C"


def calibrar(lectura, ajuste):
    time.sleep(0.3)                                  # simula enviar el ajuste al sensor
    return round(lectura + ajuste, 1)


def leer_gps():
    time.sleep(1)
    return "GPS: 6.2442, -75.5812"


def leer_bateria():
    time.sleep(1)
    return "Batería: 87 %"


# ---------- Tareas que CALCULAN (procesamiento) ----------
def procesar_sensor(id_sensor):
    suma = 0
    for i in range(N_LECTURAS):                      # el procesador trabaja todo el tiempo
        codigo = (i * id_sensor) % 100               # lectura cruda (0 a 99)
        suma += codigo
    promedio = 20 + 0.05 * suma / N_LECTURAS         # convierte a °C
    return f"Sensor {id_sensor}: promedio {promedio:.2f} °C"


def procesar_sensor_numpy(id_sensor):
    i = np.arange(N_LECTURAS)
    codigos = (i * id_sensor) % 100                  # la misma fórmula, sobre todos a la vez
    promedio = 20 + 0.05 * codigos.sum() / N_LECTURAS
    return f"Sensor {id_sensor}: promedio {promedio:.2f} °C"
