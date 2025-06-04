import pandas as pd
import requests
from io import BytesIO

def cargar_datos(url_excel):
    try:
        response = requests.get(url_excel)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        df.columns = df.columns.str.strip()
        print(f"📄 Excel cargado con columnas: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"❌ Error al cargar el Excel: {str(e)}")
        return pd.DataFrame()
    
def cargar_datos_local(ruta):
    df = pd.read_excel(ruta)
    df.columns = df.columns.str.strip()  # Limpia espacios en nombres de columnas
    print("📋 Columnas detectadas:", df.columns.tolist())
    print("📊 Primeras filas:\n", df.head())
    return df