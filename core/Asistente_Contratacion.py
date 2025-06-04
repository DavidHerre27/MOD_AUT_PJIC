import logging
from selenium.webdriver.common.by import By
from utils.helpers import safe_click, safe_send_keys
from core.Contratista import seleccionar_contratista
from core.Proyecto import seleccionar_proyecto
from core.Objeto import ingresar_objeto_contrato
from core.Fecha import seleccionar_fecha
from core.Valor_Contrato import ingresar_valor_contrato
from core.Plazo_Contrato import ingresar_plazo_contrato
from core.Modalidad import seleccionar_modalidad
from core.Procedimiento import seleccionar_procedimiento
from core.Tipo_Contrato import seleccionar_tipo_contrato
from core.Opciones_Financieras import seleccionar_opciones_financieras
from core.Rubro_Presupuestal import seleccionar_rubro_presupuestal
from core.Sub_Sector import seleccionar_sub_sector
from core.SECOP import seleccionar_secop
from core.Opciones_No import seleccionar_opciones_no
from core.Opciones_Lista import imprimir_opciones_lista
from core.Provincia_Ciudad import seleccionar_ejecucion_provincia_ciudad
from core.Validar import seleccionar_validar
from core.Ingresar import seleccionar_ingresar
from core.Interventor import seleccionar_interventor
from core.Disponibilidad import vincular_disponibilidad
from core.Fecha_Aprobacion import seleccionar_fecha_aprobacion
from core.Fecha_Web import seleccionar_fecha_web
from core.Fecha_Secop import seleccionar_fecha_secop
from core.Navegacion import volver_a_menu_principal, navegar_asistente_contratacion
from core.registro_errores import registrar_error_critico
import os

os.makedirs("logs", exist_ok=True)
os.makedirs("errors", exist_ok=True)

logging.basicConfig(
    filename='logs/proceso_contratos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def procesar_fila(driver, wait, row):
    campos_criticos = [
        ("No. de Contrato", "número de contrato"),
        ("Cédula o Nit Contratista", "cédula o NIT del contratista"),
        ("Código del Proyecto", "código del proyecto"),
        ("Rubro Presupuestal", "rubro presupuestal"),
        ("Sub-Sector", "sub-sector"),
        ("Cédula Supervisor", "cédula del supervisor"),
        ("No. CDP", "CDP")
    ]

    campos_faltantes = []
    for clave, nombre in campos_criticos:
        if not row.get(clave):
            campos_faltantes.append(f"{nombre} ({clave})")

    if campos_faltantes:
        contrato_id = row.get("No. de Contrato", "SIN IDENTIFICAR")
        dependencia = row.get("Dependencia", "Desconocida")
        logging.error(f"❌ Contrato {contrato_id} omitido. Campos faltantes: {campos_faltantes}")
        print(f"⚠️ Contrato omitido: {contrato_id}")
        registrar_error_critico(contrato_id, dependencia, campos_faltantes)
        volver_a_menu_principal(driver, wait)
        navegar_asistente_contratacion(driver, wait)
        return

    try:
        contrato_id = row["No. de Contrato"]
        logging.info(f"📌 Iniciando procesamiento para contrato: {contrato_id}")
        print(f"📌 Procesando contrato: {contrato_id}")

        safe_send_keys(wait, driver, By.ID, 'CONTRACT_IDENTIFIER', str(contrato_id))
        ingresado = driver.find_element(By.ID, 'CONTRACT_IDENTIFIER').get_attribute("value").strip()
        if not ingresado:
            raise ValueError("El número de contrato no se ingresó correctamente")
        logging.info(f"✅ Número de contrato ingresado: {ingresado}")

        seleccionar_contratista(driver, wait, row)
        logging.info(f"✅ Contratista procesado")

        seleccionar_proyecto(driver, wait, row["Código del Proyecto"])
        logging.info("✅ Proyecto seleccionado")

        if row.get("Objeto del Contrato"):
            ingresar_objeto_contrato(driver, wait, row["Objeto del Contrato"])
            logging.info("✅ Objeto del contrato ingresado")
        else:
            logging.warning("⚠️ Falta 'Objeto del Contrato'")

        if row.get("Fecha de Suscripción"):
            seleccionar_fecha(driver, wait, row["Fecha de Suscripción"], "CONTRACT_SIGNING_DATE")
            logging.info("✅ Fecha de Suscripción seleccionada")
        else:
            logging.warning("⚠️ Falta 'Fecha de Suscripción'")

        if row.get("Fecha de Inicio"):
            seleccionar_fecha(driver, wait, row["Fecha de Inicio"], "CONTRACT_STARTING_DATE")
            logging.info("✅ Fecha de Inicio seleccionada")
        else:
            logging.warning("⚠️ Falta 'Fecha de Inicio'")

        if row.get("Valor"):
            valor = str(row["Valor"]).replace("$", "").replace(",", "").strip()
            ingresar_valor_contrato(driver, wait, valor)
            logging.info(f"✅ Valor del contrato ingresado: {valor}")
        else:
            logging.warning("⚠️ Falta 'Valor del contrato'")

        if row.get("Plazo Estimado (En Dias)"):
            ingresar_plazo_contrato(driver, wait, row["Plazo Estimado (En Dias)"])
            logging.info("✅ Plazo estimado ingresado")
        else:
            logging.warning("⚠️ Falta 'Plazo Estimado (En Dias)'")

        if row.get("Modalidad o Proceso"):
            seleccionar_modalidad(driver, wait, row["Modalidad o Proceso"])
            logging.info("✅ Modalidad seleccionada")
        else:
            logging.warning("⚠️ Falta 'Modalidad o Proceso'")

        if row.get("Procedimiento/Causal"):
            seleccionar_procedimiento(driver, wait, row["Procedimiento/Causal"])
            logging.info("✅ Procedimiento/Causal seleccionado")
        else:
            logging.warning("⚠️ Falta 'Procedimiento/Causal'")

        if row.get("Tipo de Contrato"):
            seleccionar_tipo_contrato(driver, wait, row["Tipo de Contrato"])
            logging.info("✅ Tipo de contrato seleccionado")
        else:
            logging.warning("⚠️ Falta 'Tipo de Contrato'")

        seleccionar_opciones_financieras(driver, wait)
        logging.info("✅ Opciones financieras seleccionadas")

        seleccionar_rubro_presupuestal(driver, wait, row["Rubro Presupuestal"])
        logging.info("✅ Rubro presupuestal seleccionado")

        seleccionar_sub_sector(driver, wait, row["Sub-Sector"])
        logging.info("✅ Sub-sector seleccionado")

        seleccionar_secop(driver, wait, row["Enlace Proceso SECOP II"])
        seleccionar_opciones_no(driver, wait)
        imprimir_opciones_lista(driver, wait, "EXECUTION_CITY")
        seleccionar_ejecucion_provincia_ciudad(driver, wait)
        seleccionar_validar(driver, wait)
        seleccionar_ingresar(driver, wait)
        logging.info("✅ Contrato ingresado correctamente")

        seleccionar_interventor(driver, wait, row)

        vincular_disponibilidad(driver, wait, row)

        if row.get("Fecha Aprobación Garantía Única"):
            seleccionar_fecha_aprobacion(driver, wait, row["Fecha Aprobación Garantía Única"], "CONTRACT_DATE_VALUE_2")
            logging.info("✅ Fecha de aprobación ingresada")

        if row.get("Fecha Publicación pagina Web"):
            seleccionar_fecha_web(driver, wait, row["Fecha Publicación pagina Web"], "CONTRACT_DATE_VALUE_3")
            logging.info("✅ Fecha de publicación web ingresada")

        if row.get("Fecha Publicación SECOP II"):
            seleccionar_fecha_secop(driver, wait, row["Fecha Publicación SECOP II"], "CONTRACT_DATE_VALUE_4")
            logging.info("✅ Fecha SECOP ingresada")

        safe_click(wait, driver, By.ID, "btnValidar")
        safe_click(wait, driver, By.ID, "btnVincular")
        logging.info("✅ Validación y vinculación completadas")

        print(f"✅ Procesamiento completado para contrato: {row['No. de Contrato']}")
        print("=" * 60)
        volver_a_menu_principal(driver, wait)
        navegar_asistente_contratacion(driver, wait)

    except Exception as e:
        logging.error(f"❌ Error al procesar contrato {row.get('No. de Contrato', 'DESCONOCIDO')}: {e}")
        driver.save_screenshot(f"errors/error_{row.get('No. de Contrato', 'DESCONOCIDO')}.png")