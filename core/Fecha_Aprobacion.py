from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime

def seleccionar_fecha_aprobacion(driver, wait, fecha_raw, campo="BUDGET_REGISTER_DATE_2"):
    try:
        # 1. Convertir la fecha según el tipo
        if isinstance(fecha_raw, datetime):
            fecha = fecha_raw
        else:
            fecha = datetime.strptime(str(fecha_raw), "%d/%m/%Y")

        dia = fecha.day
        anio = fecha.year

        # 2. Hacer clic en el ícono del calendario asociado al campo
        calendar_icon = wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//input[@id='{campo}']/following-sibling::img[contains(@class, 'ui-datepicker-trigger')]"
        )))
        calendar_icon.click()

        # 3. Seleccionar año
        select_year = Select(wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-year"))))
        select_year.select_by_visible_text(str(anio))

        # 4. Seleccionar mes (enero = 0)
        select_month = Select(wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-month"))))
        select_month.select_by_index(fecha.month - 1)

        # 5. Seleccionar día
        xpath_dia = f"//a[text()='{dia}']"
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dia))).click()

        print(f"✅ Fecha seleccionada en '{campo}': {fecha.strftime('%d/%m/%Y')}")

    except Exception as e:
        print(f"❌ Error seleccionando fecha en '{campo}': {str(e)}")