import unicodedata

def normalizar_texto(texto):
    """Elimina acentos, convierte a minúsculas y quita espacios extras."""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()