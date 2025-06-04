from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import safe_click

def ingresar_valor_contrato(driver, wait, valor):
    try:
        print(f"📌 Ingresando valor del contrato: {valor}")

        # Esperar el campo, aunque esté deshabilitado
        campo_valor = wait.until(EC.presence_of_element_located((By.ID, "CONTRACT_AMOUNT")))
        print("✅ Campo encontrado.")

        # Habilitar el campo usando JavaScript (remueve el atributo 'disabled')
        driver.execute_script("arguments[0].removeAttribute('disabled')", campo_valor)

        # Establecer el valor usando JavaScript
        driver.execute_script("arguments[0].value = arguments[1]", campo_valor, str(valor))

        # 🔄 Clic adicional para actualizar texto
        safe_click(wait, driver, By.ID, "CONTRACT_AMOUNT")

        print("✅ Valor del contrato ingresado correctamente.")
    except Exception as e:
        print(f"❌ Error ingresando el valor del contrato: {str(e)}")