from selenium.webdriver.common.by import By
from utils.helpers import safe_click

def seleccionar_opciones_no(driver, wait):
    try:

        safe_click(wait, driver, By.ID, "ADVANCE_DEFINED1")
        print("✅ Opción 'No' seleccionada en 'ADVANCE_DEFINED'")

        safe_click(wait, driver, By.ID, "COMMERCIAL_TRUST1")
        print("✅ Opción 'No' seleccionada en 'COMMERCIAL_TRUST'")

        safe_click(wait, driver, By.ID, "URGENCY_MANIFEST1")
        print("✅ Opción 'No' seleccionada en 'URGENCY_MANIFEST'")

        safe_click(wait, driver, By.ID, "VALIDITY_FUTURE1")
        print("✅ Opción 'No' seleccionada en 'VALIDITY_FUTURE'")

        safe_click(wait, driver, By.ID, "COOPERATION_CONTRACT1")
        print("✅ Opción 'No' seleccionada en 'COOPERATION_CONTRACT'")

    except Exception as e:
        print(f"❌ Error seleccionando las opciones 'No': {str(e)}")