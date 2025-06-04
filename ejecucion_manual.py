from utils.spreadsheet import cargar_datos
from core.Login import iniciar_sesion
from core.Asistente_Contratacion import procesar_fila
from core.Navegacion import navegar_asistente_contratacion
from configuracion_usuario import seleccionar_dependencia
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import logging, os
from utils.credenciales import obtener_credenciales_gt
from utils.encriptador import desencriptar
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configurar el archivo de log
logging.basicConfig(
    filename='logs/proceso_contratos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Inicializar WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 25)

usuario = input("👤 Ingrese su nombre de usuario del sistema: ").strip()

try:
    logging.info("🚀 Iniciando sesión en la plataforma Gestión Transparente")

    gt_usuario, gt_clave_encriptada = obtener_credenciales_gt(usuario)
    gt_clave = desencriptar(gt_clave_encriptada)

    if not iniciar_sesion(driver, wait, gt_usuario, gt_clave):
        logging.error("❌ Login fallido. Se detiene el proceso.")
        input("⚠️ Presiona Enter para cerrar...")
        exit()

    logging.info("🔁 Navegando al asistente de contratación")
    navegar_asistente_contratacion(driver, wait)

    url_excel = seleccionar_dependencia()
    logging.info(f"📥 URL de hoja de cálculo seleccionada: {url_excel}")
    df = cargar_datos(url_excel)

    if df.empty:
        logging.warning("⚠️ La hoja de cálculo está vacía o no se pudo cargar.")
    else:
        logging.info(f"📄 Total de contratos cargados: {len(df)}")

    for _, row in df.iterrows():
        contrato = row.get("No. de Contrato", "SIN_ID")
        logging.info(f"📌 Procesando contrato: {contrato}")
        try:
            procesar_fila(driver, wait, row)
        except Exception as e:
            logging.error(f"❌ Error al procesar el contrato {contrato}: {e}")

finally:
    driver.quit()
    logging.info("✅ Navegador cerrado correctamente. Proceso finalizado.")
    input("✅ Proceso finalizado. Presiona Enter para cerrar...")