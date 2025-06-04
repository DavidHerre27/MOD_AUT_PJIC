from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from core.Normalizar_Texto import normalizar_texto

def seleccionar_rubro_presupuestal(driver, wait, valor):
    try:
        # Acceder al campo Rubro Presupuestal
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "BUDGET_ITEM_NAME_1")))
        dropdown = Select(dropdown_element)

        # Obtener las opciones disponibles en la lista desplegable
        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en 'BUDGET_ITEM_NAME_1':")
        for opt in opciones:
            print(f" - {opt}")

        # Intentar buscar por el número (antes de la descripción)
        valor_numero = valor.split(' ')[0]  # Tomar solo el número antes del espacio
        print(f"🔍 Buscando Rubro Presupuestal: {valor_numero}")

        # 1. Intentar seleccionar por número
        for opcion in opciones:
            if valor_numero in opcion:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Rubro Presupuestal seleccionado: {opcion}")
                return

        # 2. Intentar seleccionar por coincidencia parcial de la descripción
        valor_normalizado = normalizar_texto(valor)

        for opcion in opciones:
            if normalizar_texto(opcion) == valor_normalizado:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Rubro Presupuestal seleccionado (match exacto): {opcion}")
                return

        # Si no se encuentra ninguna coincidencia, lanzamos un error
        raise ValueError(f"No se encontró coincidencia para: '{valor}'")

    except Exception as e:
        print(f"❌ Error seleccionando Rubro Presupuestal: {str(e)}")