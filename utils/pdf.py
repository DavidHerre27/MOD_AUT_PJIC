from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generar_pdf_informe(dependencia, nombre_archivo_excel, contratos, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 50, "Informe de Contratos Procesados")

    c.setFont("Helvetica", 10)
    c.drawString(40, height - 70, f"Dependencia: {dependencia}")
    c.drawString(40, height - 85, f"Archivo: {nombre_archivo_excel}")
    c.drawString(40, height - 100, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 130
    for idx, contrato in enumerate(contratos[:30]):  # Muestra los primeros 30 contratos
        linea = f"{idx+1}. Contrato: {contrato.get('No. de Contrato', 'N/A')} - {contrato.get('Nombre', '')} - {contrato.get('Objeto del Contrato', '')}"
        c.drawString(40, y, linea[:110])
        y -= 15
        if y < 60:
            c.showPage()
            y = height - 50

    c.save()