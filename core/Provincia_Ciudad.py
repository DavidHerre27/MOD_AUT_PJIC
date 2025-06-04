from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time

def seleccionar_ejecucion_provincia_ciudad(driver, wait):
    try:
        # 1. Seleccionar provincia
        select_provincia = Select(wait.until(EC.element_to_be_clickable((By.ID, "EXECUTION_PROVINCE"))))
        select_provincia.select_by_visible_text("Antioquia")
        print("✅ Provincia seleccionada: Antioquia")
        time.sleep(1)  # Pequeña pausa para asegurar carga

        # 2. Localizar y hacer click en el dropdown de ciudad primero (si es necesario)
        dropdown_ciudad = wait.until(EC.element_to_be_clickable((By.ID, "EXECUTION_CITY")))
        dropdown_ciudad.click()
        time.sleep(0.5)

        # 3. Obtener opciones de ciudad
        select_ciudad = Select(dropdown_ciudad)
        opciones_ciudad = [option.text.strip() for option in select_ciudad.options]
        
        print(f"\n🔍 Opciones disponibles en 'EXECUTION_CITY':")
        for opt in opciones_ciudad:
            print(f" - {opt}")

        # 4. Buscar Medellín de forma robusta
        ciudad_a_seleccionar = "Medellín"
        ciudad_encontrada = False
        
        for option in select_ciudad.options:
            if ciudad_a_seleccionar.lower() in option.text.strip().lower():
                option.click()  # Seleccionar directamente el elemento
                print(f"✅ Ciudad seleccionada: {option.text.strip()}")
                ciudad_encontrada = True
                break
            elif "medellin" in option.text.strip().lower():  # Sin tilde por si acaso
                option.click()
                print(f"✅ Ciudad seleccionada (alternativa): {option.text.strip()}")
                ciudad_encontrada = True
                break
        
        if not ciudad_encontrada:
            # Intentar forzar selección por valor si existe
            try:
                select_ciudad.select_by_value("medellin")  # o algún valor conocido
                print("✅ Ciudad seleccionada por valor")
            except:
                print(f"❌ No se pudo seleccionar '{ciudad_a_seleccionar}'. Opciones: {opciones_ciudad}")
    
    except Exception as e:
        print(f"❌ Error seleccionando provincia o ciudad: {str(e)}")
        raise  # Relanzar la excepción para manejo externo