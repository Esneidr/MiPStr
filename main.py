"""
Módulo 12 — API del modelo de regresión lineal (California Housing)

Rutas:
    GET  /          → página con el formulario
    GET  /modelo    → información del modelo
    POST /predict   → predicción para una vivienda
    GET  /docs      → documentación automática (la genera FastAPI)
"""
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

CARPETA = Path(__file__).parent
MODELO = json.loads((CARPETA / "modelo.json").read_text(encoding="utf-8"))

app = FastAPI(
    title="Estimador de valor de vivienda",
    description="Regresión lineal del Módulo 6, desplegada en el Módulo 12.",
    version="1.0",
)


class Vivienda(BaseModel):
    MedInc: float = Field(..., description="Ingreso medio del sector (decenas de miles de USD)", examples=[3.5])
    HouseAge: float = Field(..., description="Edad media de las viviendas (años)", examples=[29])
    AveRooms: float = Field(..., description="Habitaciones promedio por vivienda", examples=[5.2])
    AveBedrms: float = Field(..., description="Dormitorios promedio por vivienda", examples=[1.05])
    Population: float = Field(..., description="Población del sector", examples=[1170])
    AveOccup: float = Field(..., description="Personas promedio por hogar", examples=[2.8])
    Latitude: float = Field(..., description="Latitud", examples=[34.05])
    Longitude: float = Field(..., description="Longitud", examples=[-118.24])


def predecir(datos: dict) -> float:
    # ŷ = b + Σ w_i · (x_i − μ_i) / σ_i   (la misma ecuación del notebook)
    y = MODELO["sesgo"]
    for nombre, mu, sigma, w in zip(MODELO["variables"], MODELO["media"],
                                    MODELO["desviacion"], MODELO["pesos"]):
        y += w * (datos[nombre] - mu) / sigma
    return y


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def pagina():
    return (CARPETA / "index.html").read_text(encoding="utf-8")


@app.get("/modelo")
def info_modelo():
    return {
        "nombre": MODELO["nombre"],
        "variables": MODELO["variables"],
        "r2_prueba": MODELO["r2_prueba"],
        "unidad_salida": MODELO["unidad_salida"],
    }


@app.post("/predict")
def predict(vivienda: Vivienda):
    y = predecir(vivienda.model_dump())
    y = max(y, 0.0)  # una recta puede dar negativos; un precio no
    return {
        "prediccion": round(y, 4),
        "valor_usd": round(y * 100_000),
        "nota": "Valor estimado con datos del censo de 1990",
    }
