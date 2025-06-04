from utils.helpers import safe_click
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def volver_a_menu_principal(driver, wait):
    try:
        print("🔄 Volviendo al menú principal...")

        # Esperar que el DOM se estabilice
        time.sleep(1.5)

        # Reintentar hasta 3 veces por seguridad ante errores de referencia obsoleta
        for intento in range(3):
            try:
                # Volver a buscar el enlace en cada intento
                enlace = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "MenuPpal.aspx")]')))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", enlace)
                enlace.click()

                # Verificar si llegamos al menú principal
                wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Contratación")]')))
                print("✅ Menú principal cargado correctamente.")
                return

            except Exception as e:
                print(f"⚠️ Reintento {intento+1} al hacer clic en 'Menú Principal': {e}")
                time.sleep(1.5)

        raise Exception("❌ No se pudo hacer clic en 'Menú Principal' después de varios intentos.")

    except Exception as final_error:
        print(f"❌ Error al volver al menú principal: {final_error}")

        
def navegar_asistente_contratacion(driver, wait):
    try:
        print("🔄 Navegando al asistente de contratación...")
        # Esperar visibilidad antes de hacer clic
        time.sleep(2)  # Pausa de 2 segundos antes de comenzar navegación
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "Contratación")]')))
        safe_click(wait, driver, By.XPATH, '//span[contains(text(), "Contratación")]')
        safe_click(wait, driver, By.XPATH, '//span[contains(text(), "Ingresar Contrato")]')
        safe_click(wait, driver, By.XPATH, '//a[contains(text(), "Asistente de Contratación")]')
        safe_click(wait, driver, By.ID, "CONTRACT_TYPE_CODE0")
    except Exception as e:
        print(f"❌ Error navegando al asistente: {e}")