from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from core.Normalizar_Texto import normalizar_texto

def seleccionar_tipo_contrato(driver, wait, valor):
    try:
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "CONTRACT_TYPE")))
        dropdown = Select(dropdown_element)

        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en {dropdown._el.get_attribute('id')}:")
        for opt in opciones:
            print(f" - {opt}")

        valor_normalizado = normalizar_texto(valor)
        print(f"🔍 Buscando tipo de contrato: '{valor_normalizado}'")  # Agregado para verificar el valor de búsqueda

        for opcion in opciones:
            opcion_normalizada = normalizar_texto(opcion)
            print(f" - Comparando con opción: '{opcion_normalizada}'")  # Agregado para verificar la comparación
            if opcion_normalizada == valor_normalizado:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Tipo de contrato seleccionado: {opcion}")
                return

        for opcion in opciones:
            if valor_normalizado in normalizar_texto(opcion):
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Tipo de contrato seleccionado (match parcial): {opcion}")
                return

        raise ValueError(f"No se encontró coincidencia para: '{valor}'")

    except Exception as e:
        print(f"❌ Error seleccionando tipo de contrato: {str(e)}")