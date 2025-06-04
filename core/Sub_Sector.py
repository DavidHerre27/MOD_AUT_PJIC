from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from core.Normalizar_Texto import normalizar_texto

def seleccionar_sub_sector(driver, wait, valor):
    try:
        # 1. Seleccionar el campo Sub-Sector
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "BUDGET_EXPENDITURE_SUB_SECTOR_1")))
        dropdown = Select(dropdown_element)

        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en {dropdown._el.get_attribute('id')}:")
        for opt in opciones:
            print(f" - {opt}")

        valor_normalizado = normalizar_texto(valor)

        for opcion in opciones:
            if normalizar_texto(opcion) == valor_normalizado:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Sub-Sector seleccionado: {opcion}")
                break

        # Si no se encuentra una coincidencia exacta, hacer una coincidencia parcial
        for opcion in opciones:
            if valor_normalizado in normalizar_texto(opcion):
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Sub-sector seleccionado (match parcial): {opcion}")
                break

         # 2. Intentar hacer clic en el botón "Vincular" usando JavaScript
        vincular_button = driver.find_element(By.ID, "btnAddBudgetGrid")
        driver.execute_script("arguments[0].click();", vincular_button)
        print("✅ Botón 'Vincular' clickeado con JavaScript.")

    except Exception as e:
        print(f"❌ Error seleccionando Sub-sector o clickeando 'Vincular': {str(e)}")