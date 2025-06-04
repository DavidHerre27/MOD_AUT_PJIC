from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from core.Fecha_Disponibilidad import seleccionar_fecha
from core.Valor_Disponibilidad import ingresar_valor_disponibilidad
import time

def safe_click(driver, wait, locator, max_attempts=3):
    """Función mejorada para hacer clic seguro con reintentos"""
    for attempt in range(1, max_attempts + 1):
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            time.sleep(0.5)
            ActionChains(driver).move_to_element(element).pause(0.3).click().perform()
            return True
        except Exception as e:
            print(f"⚠️ Intento {attempt} fallido al hacer clic: {str(e)}")
            if attempt == max_attempts:
                raise
            time.sleep(1)

def clean_input_field(driver, element):
    """Limpia un campo de entrada de múltiples formas"""
    element.clear()
    time.sleep(0.2)
    element.send_keys(Keys.CONTROL + 'a')
    element.send_keys(Keys.DELETE)
    time.sleep(0.2)
    driver.execute_script("arguments[0].value = '';", element)

def seleccionar_cdp(driver, wait, numero_cdp):
    """Selecciona un CDP específico en la tabla"""
    try:
        print(f"🔍 Buscando CDP: {numero_cdp}")
        
        # Esperar a que la tabla esté cargada
        tabla = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//table[contains(@id, 'GRIDBUDGETAVAILABILITY')]")
        ))
        
        # Buscar la celda que contiene el CDP
        xpath_cdp = f"//td[@class='textDescription dxgv' and normalize-space()='{numero_cdp}']"
        celda_cdp = wait.until(EC.presence_of_element_located((By.XPATH, xpath_cdp)))
        
        # Encontrar toda la fila
        fila_cdp = celda_cdp.find_element(By.XPATH, "./ancestor::tr[1]")
        
        # Localizar el checkmark verde
        checkmark = fila_cdp.find_element(
            By.XPATH, ".//img[contains(@onclick, 'btnGridSelectAvailability')]"
        )
        
        # Scroll y clic seguro
        driver.execute_script("arguments[0].scrollIntoView();", checkmark)
        time.sleep(0.5)
        
        # Intentar clic normal y luego con JavaScript si falla
        try:
            checkmark.click()
        except:
            driver.execute_script("arguments[0].click();", checkmark)
        
        print(f"✅ CDP {numero_cdp} seleccionado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al seleccionar CDP: {str(e)}")
        # Debug adicional
        print("ℹ️ CDPs visibles en la tabla:")
        cdps_visibles = driver.find_elements(By.XPATH, "//td[@class='textDescription dxgv']")
        print([cdp.text for cdp in cdps_visibles])
        raise

def vincular_disponibilidad(driver, wait, row):
    """Función principal para el proceso completo de vinculación"""
    try:
        # 1. Validar campos requeridos
        required_fields = ['No. CDP', 'No. RP', 'Fecha RP', 'Valor RP']
        for field in required_fields:
            if field not in row or not str(row[field]).strip():
                raise ValueError(f"Campo requerido faltante: {field}")

        # 2. Seleccionar CDP
        seleccionar_cdp(driver, wait, str(row['No. CDP']).strip())

        # 3. Pulsar Continuar
        for attempt in range(1, 4):
            try:
                print(f"🔄 Intento {attempt} de Continuar")
                btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSiguiente")))
                driver.execute_script("arguments[0].scrollIntoView();", btn)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", btn)
                
                # Verificar que avanzó
                wait.until(EC.presence_of_element_located(
                    (By.ID, "BUDGET_REGISTER_IDENTIFIER_1")
                ))
                print("✅ Continuar exitoso")
                break
            except Exception as e:
                if attempt == 3:
                    raise
                print(f"⚠️ Intento {attempt} fallido: {str(e)}")
                time.sleep(2)

        # 4. Ingresar Número RP
        numero_rp = str(row['No. RP']).strip()
        rp_field = wait.until(EC.element_to_be_clickable(
            (By.ID, "BUDGET_REGISTER_IDENTIFIER_1")
        ))
        clean_input_field(driver, rp_field)
        rp_field.send_keys(numero_rp)
        print(f"✅ Número RP ingresado: {numero_rp}")

        # 5. Seleccionar Fecha RP
        seleccionar_fecha(driver, wait, row['Fecha RP'], "BUDGET_REGISTER_DATE_1")

        # 6. Seleccionar Disponibilidad Presupuestal
        select = Select(wait.until(EC.element_to_be_clickable(
            (By.ID, "BUDGET_AVAILABILITY_IDENTIFIER_1")
        )))
        select.select_by_index(1)  # Seleccionar primera opción
        print("✅ Disponibilidad seleccionada")

        # 7. Ingresar Valor RP
        #valor_rp = str(row['Valor RP']).strip().replace('.', '').replace(',', '')
        #amount_field = wait.until(EC.element_to_be_clickable(
        #    (By.ID, "BUDGET_REGISTER_AMOUNT_1")
        #))
        #clean_input_field(driver, amount_field)
        #amount_field.send_keys(valor_rp)
        #print(f"✅ Valor RP ingresado: {valor_rp}")
        
        # 7. Ingresar valor del contrato si existe
        if "Valor RP" in row:
            valor_rp = str(row["Valor RP"]).replace("$", "").replace(",", "").strip()
            ingresar_valor_disponibilidad(driver, wait, valor_rp)
            print(f"✅ Valor RP ingresado: {valor_rp}")
        else:
            print("⚠️ Advertencia: No se encontró la columna 'Valor RP' en el Excel.")
        
        # 8. Validar
        safe_click(driver, wait, (By.ID, "btnValidar"))
        print("✅ Validación completada")
        time.sleep(2)

        # 9. Vincular
        safe_click(driver, wait, (By.ID, "btnVincular"))
        print("✅ Vinculación completada")
        time.sleep(3)

        print("🎉 Proceso completado exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        driver.save_screenshot('error_vinculacion.png')
        raise