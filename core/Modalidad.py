from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from core.Normalizar_Texto import normalizar_texto
import time

def seleccionar_modalidad(driver, wait, valor):
    try:
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "CONTRACT_PROCESS_TYPE_CODE")))
        wait.until(lambda d: len(Select(dropdown_element).options) > 1)
        time.sleep(0.5)
        dropdown = Select(dropdown_element)


        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en {dropdown._el.get_attribute('id')}:")
        for opt in opciones:
            print(f" - {opt}")

        valor_normalizado = normalizar_texto(valor)
        print(f"🔍 Buscando modalidad: '{valor_normalizado}'")  # Agregado para verificar el valor de búsqueda

        for opcion in opciones:
            opcion_normalizada = normalizar_texto(opcion)
            print(f" - Comparando con opción: '{opcion_normalizada}'")  # Agregado para verificar la comparación
            if opcion_normalizada == valor_normalizado:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Modalidad seleccionada: {opcion}")
                return

        for opcion in opciones:
            if valor_normalizado in normalizar_texto(opcion):
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Modalidad seleccionada (match parcial): {opcion}")
                return

        raise ValueError(f"No se encontró coincidencia para: '{valor}'")

    except Exception as e:
        print(f"❌ Error seleccionando modalidad: {str(e)}")