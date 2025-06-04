from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time
from core.Normalizar_Texto import normalizar_texto 

def seleccionar_procedimiento(driver, wait, valor):
    try:
        print(f"\n🔍 Intentando seleccionar procedimiento: '{valor}'")
        
        # Esperar a que el dropdown esté presente y sea interactuable
        dropdown_element = wait.until(
            EC.presence_of_element_located((By.ID, "CONTRACT_TYPOLOGY_CODE"))
        )
        dropdown = Select(dropdown_element)
        
        # Forzar scroll al elemento para asegurar visibilidad
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", dropdown_element)
        time.sleep(0.5)  # Pequeña pausa para animación
        
        # Obtener opciones disponibles con su valor y texto
        opciones = []
        for option in dropdown.options:
            opciones.append({
                'texto': option.text.strip(),
                'valor': option.get_attribute('value')
            })
        
        print("📋 Opciones disponibles:")
        for op in opciones:
            print(f" - Texto: '{op['texto']}' | Valor: '{op['valor']}'")
        
        valor_normalizado = normalizar_texto(valor)
        print(f"🔍 Buscando coincidencia para: '{valor_normalizado}'")
        
        # Intentar coincidencia exacta primero
        for op in opciones:
            if normalizar_texto(op['texto']) == valor_normalizado:
                print(f"✅ Coincidencia exacta encontrada: {op['texto']}")
                dropdown.select_by_visible_text(op['texto'])
                time.sleep(0.5)  # Esperar a que se aplique la selección
                return
        
        # Intentar coincidencia parcial si no se encontró exacta
        for op in opciones:
            if valor_normalizado in normalizar_texto(op['texto']):
                print(f"✅ Coincidencia parcial encontrada: {op['texto']}")
                dropdown.select_by_visible_text(op['texto'])
                time.sleep(0.5)
                return
        
        # Si todo falla, intentar seleccionar por valor (attribute value)
        for op in opciones:
            if valor_normalizado in normalizar_texto(op['valor']):
                print(f"✅ Seleccionando por valor interno: {op['valor']}")
                dropdown.select_by_value(op['valor'])
                time.sleep(0.5)
                return
        
        # Si no hay coincidencia, probar con JavaScript directo
        print("⚠️ Intentando selección vía JavaScript...")
        for index, op in enumerate(opciones):
            if valor_normalizado in normalizar_texto(op['texto']):
                driver.execute_script(f"""
                    document.getElementById('CONTRACT_TYPOLOGY_CODE').selectedIndex = {index};
                    var event = new Event('change', {{ bubbles: true }});
                    document.getElementById('CONTRACT_TYPOLOGY_CODE').dispatchEvent(event);
                """)
                print(f"✅ Selección JS exitosa: {op['texto']}")
                time.sleep(1)
                return
        
        raise ValueError(f"No se encontró ninguna coincidencia para: '{valor}'")
    
    except Exception as e:
        print(f"❌ Error crítico al seleccionar procedimiento: {str(e)}")
        # Tomar screenshot para diagnóstico
        driver.save_screenshot('error_seleccion_procedimiento.png')
        raise