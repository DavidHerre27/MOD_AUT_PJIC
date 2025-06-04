from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_click, safe_send_keys

def seleccionar_interventor(driver, wait, row):
    try:
        # 1. Pulsar el módulo de Interventores/Supervisores
        safe_click(wait, driver, By.ID, 'bsqControler01')
        print("✅ Módulo Interventores/Supervisores seleccionado.")

        # 2. Hacer clic en el label asociado a "Natural"
        safe_click(wait, driver, By.XPATH, "//label[contains(text(), 'Natural')]")
        print("✅ Opción 'Natural' seleccionada.")

        # 3. Seleccionar el tipo de documento 'Cédula de Ciudadanía'
        select_document_type = Select(wait.until(EC.element_to_be_clickable((By.ID, "CONTROLER_DOCUMENT_TYPE"))))
        try:
            select_document_type.select_by_visible_text("Cedula de Ciudadanía")
            print("✅ Tipo de documento 'Cédula de Ciudadanía' seleccionada")
        except Exception as e:
            print(f"❌ Error seleccionando el tipo de documento: {str(e)}")

        # 4. Ingresar el número de cédula del supervisor desde el Excel
        cédula_supervisor = str(row.get("Cédula Supervisor", "")).strip()
        if cédula_supervisor:
            safe_send_keys(wait, driver, By.ID, "CONTROLER_IDENTIFIERN", cédula_supervisor)
            print(f"✅ Cédula Supervisor ingresada: {cédula_supervisor}")
        else:
            print("❌ Error: No se encontró la columna 'Cédula Supervisor' en el Excel.")

        # 5. Pulsar el botón 'Validar'
        safe_click(wait, driver, By.ID, "btnValidateContractor")
        print("✅ Interventor validado.")

        # 6. Seleccionar el primer resultado visible de la lista de coincidencias
        # Esperar a que aparezca algún resultado
        wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(@class, 'textCodes')]")))
        # Seleccionar el primer resultado
        first_result = driver.find_element(By.XPATH, "//td[contains(@class, 'textCodes')]")
        first_result.click()
        print("✅ Interventor seleccionado.")

        # 7. Pulsar el botón 'Cargar'
        safe_click(wait, driver, By.ID, "btnLoadCtler")
        print("✅ Interventor cargado.")

        # 8. Seleccionar 'Interno' en la lista desplegable
        select_type = Select(wait.until(EC.element_to_be_clickable((By.ID, "CONTROLER_TYPE_NAME_1"))))
        select_type.select_by_visible_text("Interno")
        print("✅ Opción 'Interno' seleccionada")

        # 9. Pulsar el botón 'Validar'
        safe_click(wait, driver, By.ID, "ctl00_contenido_btnValidar")
        print("✅ Validación del interventor completada.")

        # 10. Pulsar el botón 'Vincular'
        safe_click(wait, driver, By.ID, "ctl00_contenido_btnVincular")
        print("✅ Interventor vinculado.")

    except Exception as e:
        print(f"❌ Error en la selección del interventor: {str(e)}")
        raise