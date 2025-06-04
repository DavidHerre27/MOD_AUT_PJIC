from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import os

def safe_click(wait, driver, by, value):
    try:
        element = wait.until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        element.click()
    except TimeoutException:
        print(f"❌ No se pudo hacer clic en {value}")

def safe_send_keys(wait, driver, by, value, text):
    try:
        element = wait.until(EC.visibility_of_element_located((by, value)))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        element.clear()
        element.send_keys(text)
    except Exception as e:
        print(f"❌ Error al escribir en {value}: {str(e)}")

def safe_send_keys_wait_enabled(wait, driver, by, value, text, timeout=10):
    try:
        input_element = wait.until(EC.presence_of_element_located((by, value)))
        wait.until(EC.visibility_of_element_located((by, value)))
        wait.until(EC.element_to_be_clickable((by, value)))

        is_disabled = input_element.get_attribute("disabled")
        if is_disabled:
            print(f"⚠️ El campo {value} estaba disabled. Esperando que se habilite...")
            for _ in range(timeout):
                time.sleep(1)
                is_disabled = input_element.get_attribute("disabled")
                if not is_disabled:
                    break
            else:
                raise Exception(f"⏰ Timeout esperando que el campo {value} se habilite")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_element)
        time.sleep(0.3)
        input_element.clear()
        input_element.send_keys(text)
        print(f"✅ Texto enviado a {value}: {text}")

    except Exception as e:
        print(f"❌ Error al escribir en {value}: {str(e)}")
        raise

def safe_click_js(wait, driver, by, value):
    """Hace clic usando JavaScript forzado en un elemento."""
    try:
        element = wait.until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        driver.execute_script("arguments[0].click();", element)
        print(f"✅ Click forzado con JS en {value}")
    except Exception as e:
        print(f"❌ Error haciendo click JS en {value}: {str(e)}")
        raise
    
def leer_configuracion():
    config_path = os.path.join(os.path.dirname(__file__), "..", "configuracion.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "url": "",
            "script": "",
            "informe": ""
        }