from selenium.webdriver.common.by import By
from utils.helpers import safe_click

def seleccionar_validar(driver, wait):
    try:
        # Hacer clic en el botón "Validar"
        safe_click(wait, driver, By.ID, "btnValidarg2")  # ID del botón "Validar"
        print("✅ Botón 'Validar' clickeado.")

    except Exception as e:
        print(f"❌ Error al hacer clic en el botón 'Validar': {str(e)}")