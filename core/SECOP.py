from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_send_keys
import time

def seleccionar_secop(driver, wait, enlace_secop):
    try:
        # 1. Asegurarnos de que el botón de radio 'Sí' esté visible y no cubierto por otros elementos.
        secop_radio_button = wait.until(EC.element_to_be_clickable((By.ID, "SECOP_PUBLICATION0")))
        
        # Usamos JavaScript para hacer scroll hasta el radio button, asegurándonos de que sea visible
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", secop_radio_button)
        time.sleep(0.5)  # Espera para asegurar que el scroll se haya realizado correctamente
        
        # Intentamos hacer clic en el radio button
        secop_radio_button.click()
        print("✅ Opción 'Sí' seleccionada en 'SECOP_PUBLICATION'")
        
        # 2. Ingresar el enlace SECOP II
        secop_url_field = wait.until(EC.element_to_be_clickable((By.ID, "SECOP_URL")))
        safe_send_keys(wait, driver, By.ID, "SECOP_URL", enlace_secop)  # Ingresar el enlace en el campo correspondiente
        print(f"✅ Enlace SECOP II ingresado: {enlace_secop}")
    
    except Exception as e:
        print(f"❌ Error seleccionando SECOP: {str(e)}")