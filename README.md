# Bot RPA para Gestión Transparente

Este bot automatiza el proceso de ingreso de contratos en la plataforma [gestiontransparente.com](http://www.gestiontransparente.com/Rendicion/Inicio.aspx) leyendo los datos desde un archivo de Google Spreadsheet.

---

## 📁 Estructura del Proyecto

```
rpa_bot/
├── main.py                      # Script principal
├── utils/
│   ├── helpers.py               # Funciones reutilizables (click, send_keys)
│   └── spreadsheet.py           # Lectura del Google Spreadsheet
├── core/
│   ├── login.py                 # Login y navegación
│   ├── contrato.py              # Flujo de procesamiento por fila
│   ├── contratista.py           # Selección y validación del contratista
│   ├── proyecto.py              # Selección y validación del proyecto
│   └── objeto.py                # Ingreso del objeto contractual
```

---

## ⚙️ Requisitos

- Python 3.7 o superior
- Google Chrome + ChromeDriver (instalado y compatible)
- Conexión a Internet
- Paquetes Python:

```bash
pip install selenium pandas requests openpyxl
```

---

## ▶️ ¿Cómo usarlo?

1. Clona o descomprime este repositorio.
2. Asegúrate de tener `chromedriver` en la misma carpeta o en tu PATH.
3. Ejecuta el bot:

```bash
python main.py
```

---

## 🧠 Notas

- El spreadsheet debe estar publicado y tener columnas como:
  - `No. de Contrato`
  - `Cédula o Nit Contratista`
  - `Código del Proyecto`
  - `Objeto del Contrato`
- El bot tomará cada fila del Excel y la ingresará en el sistema automáticamente.

---

## 📬 Contacto

Desarrollado por Carlos David Herrera García – `carlos_herrera82181@elpoli.edu.co`
