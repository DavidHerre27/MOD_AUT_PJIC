from selenium.webdriver.common.by import By
from utils.helpers import safe_send_keys

def ingresar_objeto_contrato(driver, wait, objeto):
    try:
        print(f"\U0001F4CC Ingresando objeto del contrato: {objeto[:50]}...")
        safe_send_keys(wait, driver, By.ID, "CONTRACT_OBJECT_DESC", objeto)
        print("✅ Objeto del contrato ingresado correctamente.")
    except Exception as e:
        print(f"❌ Error ingresando el objeto del contrato: {str(e)}")