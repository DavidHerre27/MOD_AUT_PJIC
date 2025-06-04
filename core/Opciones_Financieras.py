from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_click

def seleccionar_opciones_financieras(driver, wait):
    try:
        # 1. Marcar "No" en el campo OTHER_CURRENCY
        safe_click(wait, driver, By.ID, "OTHER_CURRENCY1")
        print("✅ Opción 'No' seleccionada en 'OTHER_CURRENCY'")

        # 2. Seleccionar plan de gobierno
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "BUDGET_DEVELOPMENT_PLAN_1")))
        dropdown = Select(dropdown_element)
        
        # Imprimir todas las opciones disponibles en el dropdown para verificar
        opciones = [option.text.strip() for option in dropdown.options]
        print(f"\n🔍 Opciones disponibles en 'BUDGET_DEVELOPMENT_PLAN_1':")
        for opt in opciones:
            print(f" - {opt}")

        # Realizar búsqueda con coincidencia parcial en vez de texto exacto
        plan_gobierno_parcial = "2022-2025"  # Buscar por el año que aparece en las opciones
        plan_gobierno_encontrado = False
        for opcion in opciones:
            if plan_gobierno_parcial in opcion:
                dropdown.select_by_visible_text(opcion)
                print(f"✅ Plan de gobierno seleccionado: {opcion}")
                plan_gobierno_encontrado = True
                break
        
        if not plan_gobierno_encontrado:
            print(f"❌ No se encontró el plan de gobierno con coincidencia parcial '{plan_gobierno_parcial}'")

        # 3. Seleccionar año de rubro
        dropdown_year = wait.until(EC.element_to_be_clickable((By.ID, "BUDGET_YEAR_1")))
        select_year = Select(dropdown_year)
        select_year.select_by_visible_text("2025")  # Año 2025 según la imagen
        print("✅ Año seleccionado: 2025")
    
    except Exception as e:
        print(f"❌ Error seleccionando opciones financieras: {str(e)}")