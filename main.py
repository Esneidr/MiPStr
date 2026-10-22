"""
Módulo 12 — API del modelo de regresión logística (¿lloverá mañana?)

Rutas:
    GET  /          → página con el formulario
    GET  /modelo    → información y métricas del modelo
    POST /predict   → probabilidad de lluvia y decisión
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
    title="¿Lloverá mañana?",
    description="Regresión logística del Módulo 8, desplegada en el Módulo 12.",
    version="1.0",
)


class Dia(BaseModel):
    temperatura: float = Field(..., ge=-10, le=50, description="Temperatura promedio (°C)", examples=[24])
    humedad: float = Field(..., ge=0, le=100, description="Humedad relativa (%)", examples=[85])
    viento: float = Field(..., ge=0, le=150, description="Velocidad del viento (km/h)", examples=[12])


def sigmoide(z: float) -> float:
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    e = math.exp(z)
    return e / (1 + e)


def clasificar(datos: dict):
    # z = b + Σ w_i · x_i   →   p = σ(z)   →   clase = p ≥ umbral
    z = MODELO["sesgo"]
    for nombre, w in zip(MODELO["variables"], MODELO["pesos"]):
        z += w * datos[nombre]
    p = sigmoide(z)
    return p, int(p >= MODELO["umbral"])


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def pagina():
    return (CARPETA / "index.html").read_text(encoding="utf-8")


@app.get("/modelo")
def info_modelo():
    return {
        "nombre": MODELO["nombre"],
        "variables": MODELO["variables"],
        "umbral": MODELO["umbral"],
        "metricas_prueba": MODELO["metricas_prueba"],
    }


@app.post("/predict")
def predict(dia: Dia):
    p, clase = clasificar(dia.model_dump())
    return {
        "probabilidad": round(p, 4),
        "clase": clase,
        "decision": MODELO["clases"][str(clase)],
        "umbral": MODELO["umbral"],
    }
