from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_click, safe_send_keys

def seleccionar_proyecto(driver, wait, codigo):
    try:
        # 1. Pulsar el botón para buscar proyecto
        print(f"📌 Seleccionando proyecto: {codigo}")
        safe_click(wait, driver, By.ID, "ctl00_contenido_bsqProject1")
        wait.until(EC.presence_of_element_located((By.ID, "ProjectIdentifier")))
        
        # 2. Ingresar el código del proyecto en el campo
        safe_send_keys(wait, driver, By.ID, "ProjectIdentifier", str(codigo))
        safe_click(wait, driver, By.ID, "btnValidate")
        xpath = f"//td[contains(text(), '{codigo}')]"
        
        # 3. Desplazar hasta el elemento para asegurarnos de que no esté cubierto
        proyecto_elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", proyecto_elemento)
        
        # 4. Ahora hacer clic en el proyecto
        proyecto_elemento.click()

        # 5. Pulsar el botón 'Cargar'
        safe_click(wait, driver, By.ID, "btnLoadProject")

        # 6. 🔄 Esperar a que desaparezca el loader antes de validar
        wait.until(EC.invisibility_of_element_located((By.ID, "ctl00_contenido_LoadingPanel_LD")))

        # 7. ✅ Clic en "Validar"
        validar_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnValidarg1")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", validar_btn)
        validar_btn.click()
        print("✅ Proyecto validado.")

    except Exception as e:
        print(f"❌ Error seleccionando el proyecto {codigo}: {str(e)}")