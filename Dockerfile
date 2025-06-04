# Base oficial de Python
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY . /app

# Instalar Chrome y dependencias
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del backend
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]