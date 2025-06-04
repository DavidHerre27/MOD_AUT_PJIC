from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_click, safe_send_keys

def ingresar_plazo_contrato(driver, wait, plazo_dias):
    try:
        print(f"📆 Ingresando plazo del contrato: {plazo_dias} días")
        
        # Esperar el campo
        campo_plazo = wait.until(EC.presence_of_element_located((By.ID, "CONTRACT_TERM_MEASURE")))
        print("✅ Campo encontrado.")
        
        # Establecer el valor
        safe_send_keys(wait, driver, By.ID, "CONTRACT_TERM_MEASURE", str(plazo_dias))

        # Seleccionar opción días (radio button)
        safe_click(wait, driver, By.ID, "CONTRACT_TIME_UNIT_CODE1")

        print(f"✅ Plazo del contrato ingresado y opción 'días' seleccionada.")
    
    except Exception as e:
        print(f"❌ Error al ingresar plazo del contrato: {str(e)}")