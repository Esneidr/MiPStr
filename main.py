"""
Módulo 12 — API del modelo KNN (¿lloverá mañana?)

Rutas:
    GET  /          → página con el formulario
    GET  /modelo    → información y métricas del modelo
    POST /predict   → votación de los k vecinos más cercanos
    GET  /docs      → documentación automática (la genera FastAPI)
"""
import json
import math
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

CARPETA = Path(__file__).parent
MODELO = json.loads((CARPETA / "modelo.json").read_text(encoding="utf-8"))

app = FastAPI(
    title="¿Lloverá mañana? (KNN)",
    description="KNN con los días del Módulo 8, desplegado en el Módulo 12.",
    version="1.0",
)


class Dia(BaseModel):
    temperatura: float = Field(..., ge=-10, le=50, description="Temperatura promedio (°C)", examples=[24])
    humedad: float = Field(..., ge=0, le=100, description="Humedad relativa (%)", examples=[85])
    viento: float = Field(..., ge=0, le=150, description="Velocidad del viento (km/h)", examples=[12])


def a_unidades(punto):
    # De vuelta a °C, % y km/h:  x = z · σ + μ
    return {v: round(z * s + mu, 1)
            for v, z, mu, s in zip(MODELO["variables"], punto, MODELO["media"], MODELO["desviacion"])}


def clasificar(datos: dict):
    z = [(datos[v] - mu) / s for v, mu, s in zip(MODELO["variables"], MODELO["media"], MODELO["desviacion"])]
    distancias = sorted((math.dist(z, punto), j) for j, punto in enumerate(MODELO["puntos"]))
    vecinos = distancias[:MODELO["k"]]
    votos = sum(MODELO["etiquetas"][j] for _, j in vecinos)
    p = votos / MODELO["k"]
    return p, int(p >= 0.5), vecinos


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def pagina():
    return (CARPETA / "index.html").read_text(encoding="utf-8")


@app.get("/modelo")
def info_modelo():
    return {
        "nombre": MODELO["nombre"],
        "variables": MODELO["variables"],
        "k": MODELO["k"],
        "dias_guardados": len(MODELO["puntos"]),
        "metricas_prueba": MODELO["metricas_prueba"],
    }


@app.post("/predict")
def predict(dia: Dia):
    p, clase, vecinos = clasificar(dia.model_dump())
    return {
        "probabilidad": round(p, 4),
        "clase": clase,
        "decision": MODELO["clases"][str(clase)],
        "k": MODELO["k"],
        "vecinos": [
            {**a_unidades(MODELO["puntos"][j]), "llovio": MODELO["etiquetas"][j], "distancia": round(d, 3)}
            for d, j in vecinos
        ],
    }
