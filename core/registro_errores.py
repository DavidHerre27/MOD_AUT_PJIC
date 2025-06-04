import os
import json

RUTA_LOG = "logs/errores_criticos.json"

def registrar_error_critico(fila: dict, razon: str):
    os.makedirs("logs", exist_ok=True)

    # Cargar errores previos si existen
    if os.path.exists(RUTA_LOG):
        with open(RUTA_LOG, "r", encoding="utf-8") as f:
            errores = json.load(f)
    else:
        errores = []

    # Agregar nuevo error
    errores.append({
        "fila": fila,
        "razon": razon
    })

    # Guardar nuevamente
    with open(RUTA_LOG, "w", encoding="utf-8") as f:
        json.dump(errores, f, ensure_ascii=False, indent=4)