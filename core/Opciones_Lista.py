from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

def imprimir_opciones_lista(driver, wait, campo_id):
    try:
        # Esperar a que la lista desplegable esté disponible
        dropdown_element = wait.until(EC.presence_of_element_located((By.ID, campo_id)))
        dropdown = Select(dropdown_element)

        # Imprimir las opciones disponibles
        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en '{campo_id}':")
        for opt in opciones:
            print(f" - {opt}")

    except Exception as e:
        print(f"❌ Error imprimiendo opciones de lista desplegable: {str(e)}")