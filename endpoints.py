from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import FileResponse
from utils.spreadsheet import cargar_datos_local
from utils.helpers import leer_configuracion
from core.Login import iniciar_sesion
from core.Navegacion import navegar_asistente_contratacion
from core.Asistente_Contratacion import procesar_fila
from utils.pdf import generar_pdf_informe
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from auth.auth import verificar_clave, crear_token_acceso
from utils.spreadsheet import cargar_datos_local
from auth.dependencies import get_current_user
from fastapi import Depends
from fastapi import HTTPException, Query
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.credenciales import obtener_credenciales_gt
from utils.encriptador import encriptar, desencriptar
from dotenv import load_dotenv
from auth import database
import os
import json
import logging
import shutil
import pandas as pd
import jwt
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()
router = APIRouter()
UPLOADS_DIR = "uploads"
load_dotenv()

@router.post("/subir_excel")
def subir_excel(
    file: UploadFile = File(...),
    dependencia: str = Query(...)
):
    try:
        os.makedirs(f"uploads/{dependencia}", exist_ok=True)
        nombre_archivo = f"contratos_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
        ruta_destino = os.path.join("uploads", dependencia, nombre_archivo)

        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Revisa si el archivo realmente se puede leer
        df = cargar_datos_local(ruta_destino)
        print("🧠 Columnas detectadas:", df.columns.tolist())
        print("📄 Primeras filas:\n", df.head())
        print("📋 Vista previa del contenido cargado:\n", df.head())

        return {
            "mensaje": "Archivo subido con éxito",
            "archivo_guardado": nombre_archivo
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/automatizar")
def ejecutar_automatizacion(dependencia: str = Query(...), archivo: str = Query(...), usuario: str = Query("Desconocido")):
    # 1. Obtener y desencriptar credenciales
    gt_usuario, gt_clave_encriptada = obtener_credenciales_gt(usuario)
    
    print(f"🛂 Usuario: {usuario}")
    print(f"🔒 Clave encriptada recuperada: {gt_clave_encriptada}")
    if not gt_usuario or not gt_clave_encriptada:
        raise HTTPException(status_code=400, detail="❌ Credenciales de Gestión Transparente no configuradas para este usuario.")

    print("🔐 FERNET_KEY (debug):", os.getenv("FERNET_KEY"))
    gt_clave = desencriptar(gt_clave_encriptada)  # ← 🔐 Aquí se desencripta la clave

    # 2. Cargar configuración y archivo
    config = leer_configuracion()
    ruta_archivo = os.path.join(os.path.dirname(__file__), "uploads", dependencia, archivo)
    if not os.path.exists(ruta_archivo):
        return {"error": f"El archivo '{archivo}' no se encuentra."}

    df = cargar_datos_local(ruta_archivo)
    if df.empty:
        return {"error": "El archivo de contratos está vacío o no se pudo leer."}

    # 3. Configurar logs
    log_path = config.get("informe", "logs/proceso_contratos.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 4. Iniciar WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    try:
        # 5. Iniciar sesión en Gestión Transparente
        if not iniciar_sesion(driver, wait, gt_usuario, gt_clave):
            raise HTTPException(status_code=401, detail="❌ Fallo en el login. Verifica credenciales de Gestión Transparente.")

        # 6. Continuar flujo
        navegar_asistente_contratacion(driver, wait)

        for _, row in df.iterrows():
            contrato = row.get("No. de Contrato", "SIN_ID")
            try:
                procesar_fila(driver, wait, row)
            except Exception as e:
                logging.error(f"❌ Error al procesar contrato {contrato}: {e}")

        informe_dir = os.path.join(os.path.dirname(__file__), "informes", dependencia)
        os.makedirs(informe_dir, exist_ok=True)
        nombre_pdf = f"informe_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"
        ruta_pdf = os.path.join(informe_dir, nombre_pdf)
        generar_pdf_informe(dependencia, archivo, df.to_dict(orient="records"), ruta_pdf)

        historial_path = os.path.join(os.path.dirname(__file__), "historial.json")
        nuevo_registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dependencia": dependencia,
            "archivo": archivo,
            "cantidad_contratos": len(df),
            "estado": "OK",
            "archivo_pdf": nombre_pdf,
            "usuario": usuario
        }

        if os.path.exists(historial_path):
            with open(historial_path, "r", encoding="utf-8") as f:
                historial = json.load(f)
        else:
            historial = []

        historial.append(nuevo_registro)

        with open(historial_path, "w", encoding="utf-8") as f:
            json.dump(historial, f, indent=2, ensure_ascii=False)

        return {"mensaje": "✔️ Automatización finalizada correctamente"}

    finally:
        driver.quit()

@router.get("/descargar_informe")
def descargar_informe(dependencia: str = Query(...), archivo_pdf: str = Query(...)):
    ruta = os.path.join(os.path.dirname(__file__), "informes", dependencia, archivo_pdf)
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail=f"No se encontró el informe {archivo_pdf}")
    return FileResponse(path=ruta, filename=archivo_pdf, media_type='application/pdf')

@router.get("/historial")
def obtener_historial():
    path_historial = os.path.join(os.path.dirname(__file__), "historial.json")

    if not os.path.exists(path_historial):
        return []

    with open(path_historial, "r", encoding="utf-8") as f:
        registros = json.load(f)

    registros_filtrados = []

    for reg in registros:
        dependencia = reg.get("dependencia")
        archivo_pdf = reg.get("archivo_pdf")

        ruta_pdf = os.path.join(os.path.dirname(__file__), "informes", dependencia, archivo_pdf)

        if os.path.exists(ruta_pdf):
            registros_filtrados.append(reg)

    return registros_filtrados

@router.get("/contratos")
def obtener_contratos(
    archivo: str = Query(...),
    dependencia: str = Query(...)
):
    ruta_local = os.path.join(os.path.dirname(__file__), "uploads", dependencia, archivo)
    print(f"📁 Leyendo archivo en ruta: {ruta_local}")
    df = cargar_datos_local(ruta_local)

    print(f"🧾 Vista previa del contenido cargado:\n", df.head())

    if df.empty:
        return []

    return df.fillna("").to_dict(orient="records")

@router.get("/ver_archivo_excel")
def ver_contratos_excel(dependencia: str = Query(...), archivo: str = Query(...)):
    path = os.path.join(os.path.dirname(__file__), "uploads", dependencia, archivo)
    if not os.path.exists(path):
        return {"error": f"No se encontró el archivo '{archivo}' para la dependencia '{dependencia}'"}
    df = cargar_datos_local(path)
    if df.empty:
        return {"error": "El archivo está vacío o no se pudo leer."}
    return df.fillna("").to_dict(orient="records")

@router.get("/configuracion")
def obtener_configuracion():
    path = os.path.join(os.path.dirname(__file__), "configuracion.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@router.post("/configuracion")
def guardar_configuracion(datos: dict):
    path = os.path.join(os.path.dirname(__file__), "configuracion.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    return {"mensaje": "✔️ Configuración actualizada"}

@router.get("/ver_archivo_excel")
def ver_contratos_excel(
    dependencia: str = Query(...),
    archivo: str = Query(...)
):
    from utils.spreadsheet import cargar_datos_local

    ruta = os.path.join(os.path.dirname(__file__), "uploads", dependencia, archivo)
    if not os.path.exists(ruta):
        return {"error": f"No se encontró el archivo '{archivo}' para la dependencia '{dependencia}'."}

    df = cargar_datos_local(ruta)
    if df.empty:
        return {"error": "El archivo está vacío o no se pudo leer."}

    return df.fillna("").to_dict(orient="records")

@router.get("/descargar_informe")
def descargar_informe(
    dependencia: str = Query(...),
    archivo_pdf: str = Query(...)
):
    ruta = os.path.join(os.path.dirname(__file__), "informes", dependencia, archivo_pdf)
    if not os.path.exists(ruta):
        return {"error": f"No se encontró el informe {archivo_pdf}"}
    return FileResponse(path=ruta, filename=archivo_pdf, media_type='application/pdf')

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = """
        SELECT clave_hash, dependencia, es_superusuario 
        FROM usuarios 
        WHERE usuario = :usuario
    """
    values = {"usuario": form_data.username}
    resultado = await database.fetch_one(query=query, values=values)

    if not resultado:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    clave_hash = resultado["clave_hash"]
    dependencia = resultado["dependencia"]
    es_superusuario = resultado["es_superusuario"]

    if not verificar_clave(form_data.password, clave_hash):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # 🔐 Generar token JWT con info
    token = crear_token_acceso({
        "sub": form_data.username,
        "dependencia": dependencia,
        "es_superusuario": bool(es_superusuario)
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": form_data.username,
        "dependencia": dependencia,
        "es_superusuario": bool(es_superusuario)
    }

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, "SECRETO", algorithms=["HS256"])
        return payload.get("sub")  # "sub" es donde solemos guardar el nombre de usuario
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.delete("/eliminar_excel")
async def eliminar_excel(archivo: str = Query(...), dependencia: str = Query(...)):
    ruta_archivo = os.path.join(UPLOADS_DIR, dependencia, archivo)

    if not os.path.exists(ruta_archivo):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    try:
        os.remove(ruta_archivo)
        return {"mensaje": "Archivo eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el archivo: {e}")
    
class UsuarioNuevo(BaseModel):
    usuario: str
    clave: str
    dependencia: str

@router.post("/crear_usuario")
async def crear_usuario(data: UsuarioNuevo, token: str = Depends(oauth2_scheme)):
    usuario_actual = get_current_user(token)

    # Verificar si el usuario actual es superusuario
    query_super = "SELECT es_superusuario FROM usuarios WHERE usuario = :usuario"
    resultado = await database.fetch_one(query=query_super, values={"usuario": usuario_actual})
    
    if not resultado or resultado["es_superusuario"] != 1:
        raise HTTPException(status_code=403, detail="❌ Acceso denegado: solo superusuarios")

    # Verificar si el nuevo usuario ya existe
    query_existente = "SELECT 1 FROM usuarios WHERE usuario = :usuario"
    existente = await database.fetch_one(query=query_existente, values={"usuario": data.usuario})

    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Hashear la contraseña
    hashed = bcrypt.hashpw(data.clave.encode("utf-8"), bcrypt.gensalt())

    # Insertar nuevo usuario
    query_insert = """
        INSERT INTO usuarios (usuario, clave_hash, dependencia, es_superusuario)
        VALUES (:usuario, :clave_hash, :dependencia, 0)
    """
    await database.execute(query=query_insert, values={
        "usuario": data.usuario,
        "clave_hash": hashed,
        "dependencia": data.dependencia
    })

    return {"mensaje": "✅ Usuario creado correctamente"}


@router.post("/actualizar_credenciales_gt")
async def actualizar_credenciales_gt(
    usuario_sistema: str = Query(...),
    gt_usuario: str = Query(...),
    gt_clave_encriptada: str = Query(...)
):
    clave_gt_encriptada = encriptar(gt_clave_encriptada)

    query = """
        INSERT INTO credenciales_gt (usuario_sistema, gt_usuario, gt_clave_encriptada)
        VALUES (:usuario_sistema, :gt_usuario, :gt_clave_encriptada)
        ON CONFLICT (usuario_sistema) DO UPDATE SET
            gt_usuario = EXCLUDED.gt_usuario,
            gt_clave_encriptada = EXCLUDED.gt_clave_encriptada
    """
    values = {
        "usuario_sistema": usuario_sistema,
        "gt_usuario": gt_usuario,
        "gt_clave_encriptada": clave_gt_encriptada
    }

    await database.execute(query=query, values=values)

    return {"mensaje": "✅ Credenciales actualizadas correctamente"}

@router.post("/guardar_credenciales")
async def guardar_credenciales(data: dict):
    usuario_sistema = data["usuario_sistema"]
    gt_usuario = data["gt_usuario"]
    clave_gt = data["gt_clave"]  # Texto plano

    clave_encriptada = encriptar(clave_gt)

    query = """
        INSERT INTO credenciales_gt (usuario_sistema, gt_usuario, gt_clave_encriptada)
        VALUES (:usuario_sistema, :gt_usuario, :gt_clave_encriptada)
        ON CONFLICT (usuario_sistema) DO UPDATE SET
            gt_usuario = EXCLUDED.gt_usuario,
            gt_clave_encriptada = EXCLUDED.gt_clave_encriptada
    """
    values = {
        "usuario_sistema": usuario_sistema,
        "gt_usuario": gt_usuario,
        "gt_clave_encriptada": clave_encriptada
    }

    await database.execute(query=query, values=values)

    return {"mensaje": "✅ Credenciales actualizadas"}

@router.get("/errores")
def obtener_errores_criticos():
    archivo = "logs/errores.json"
    
    if not os.path.exists(archivo):
        return JSONResponse(status_code=200, content=[])

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            errores = json.load(f)
        return errores
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error al leer errores: {str(e)}"})