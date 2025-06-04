from selenium.webdriver.common.by import By
from utils.helpers import safe_click
def seleccionar_ingresar(driver, wait):
    try:
        # Hacer clic en el botón "Ingresar"
        safe_click(wait, driver, By.ID, "btnIngresar")  # ID del botón "Ingresar"
        print("✅ Botón 'Ingresar' clickeado.")
    
    except Exception as e:
        print(f"❌ Error al hacer clic en el botón 'Ingresar': {str(e)}")