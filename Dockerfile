# Imagen base liviana de Python
FROM python:3.9.13-slim

# Evita prompts durante instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo lo necesario
COPY requirements.txt .

# Instalar dependencias del sistema (solo lo esencial)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential gcc \
    && apt-get autoremove -y \
    && apt-get clean

# Copiar el resto de tu código
COPY . .

# Puerto que usará tu app (coincide con app.run(port=5000))
EXPOSE 5000

# Comando para correr la app (ajustar si usás otra ruta)
CMD ["python", "-m", "app.main"]
