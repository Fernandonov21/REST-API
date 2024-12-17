# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar las dependencias necesarias para mysqlclient (usando MariaDB)
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto al contenedor
COPY . .

# Exponer el puerto 8000 para el servidor FastAPI
EXPOSE 8000

# Comando para ejecutar el servidor de FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
