import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.helpers import safe_click, safe_send_keys

def iniciar_sesion(driver, wait, usuario, clave):
    driver.get("http://www.gestiontransparente.com/Rendicion/Inicio.aspx")
    safe_send_keys(wait, driver, By.ID, "ctl00_contenido_txtUsuario_I", usuario)
    safe_send_keys(wait, driver, By.ID, "ctl00_contenido_txtClave_I", clave)
    safe_click(wait, driver, By.ID, "ctl00_contenido_imgEntrar")

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Contratación")]')))
        return True
    except:
        print("❌ Inicio de sesión fallido. Verifica las credenciales.")
        return False