from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.helpers import safe_click, safe_send_keys_wait_enabled

def seleccionar_contratista(driver, wait, row):
    try:
        # Validaciones previas
        tipo_contratista = str(row.get('Tipo de Contratista', '')).strip().lower()
        numero_id = str(row.get('Cédula o Nit Contratista', '')).strip()

        if not tipo_contratista or tipo_contratista not in ['juridica', 'natural']:
            raise ValueError("⚠️ Campo 'Tipo de Contratista' inválido o vacío. Debe ser 'Jurídica' o 'Natural'.")

        if not numero_id:
            raise ValueError("⚠️ Campo 'Cédula o Nit Contratista' está vacío.")

        # 1. Pulsar el botón para buscar contratista
        safe_click(wait, driver, By.ID, 'ctl00_contenido_bsqContractor')
        wait.until(EC.presence_of_element_located((By.ID, 'CONTRACTOR_LEGAL_NATURE_CODE0')))
        print("✅ Módulo Contratistas abierto")

        # 2. Seleccionar tipo de persona y tipo de documento
        if tipo_contratista == 'juridica':
            es_juridica = True
            tipo_doc = "NIT"
            safe_click(wait, driver, By.ID, 'CONTRACTOR_LEGAL_NATURE_CODE0')
        else:
            es_juridica = False
            tipo_doc = "Cedula de Ciudadanía"
            safe_click(wait, driver, By.ID, 'CONTRACTOR_LEGAL_NATURE_CODE1')

        print("✅ Opción seleccionada:", "Persona Jurídica" if es_juridica else "Persona Natural")

        dropdown_id = "DOCUMENT_TYPE_CORP" if es_juridica else "CONTRACTOR_DOCUMENT_TYPE"
        dropdown = wait.until(EC.element_to_be_clickable((By.ID, dropdown_id)))
        select = Select(dropdown)
        select.select_by_visible_text(tipo_doc)
        print(f"✅ Tipo de documento seleccionado: {tipo_doc}")

        # 3. Escribir número de identificación (tal cual del Excel)
        safe_send_keys_wait_enabled(wait, driver, By.ID, "CONTRACTOR_IDENTIFIERN", numero_id)

        # 4. Click en Validar Contratista
        buscar_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnValidateContractor")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buscar_btn)
        driver.execute_script("arguments[0].click();", buscar_btn)

        # 5. Esperar a que desaparezca el loading
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.dxpc-loading')))

        # 6. Cargar los datos del contratista
        descripcion_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "textDescription")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", descripcion_btn)
        safe_click(wait, driver, By.CLASS_NAME, "textDescription")

        safe_click(wait, driver, By.ID, "btnLoadEntity")
        print("✅ Contratista validado y cargado exitosamente.")

    except Exception as e:
        print(f"❌ Error seleccionando contratista: {str(e)}")