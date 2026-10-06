# 1. Imagen base: Django 6.x exige Python 3.12 o superior
FROM python:3.13-slim

# 2. Evitamos archivos .pyc y buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Código fuente
COPY . /app/

# 6. Puerto interno (solo lo ve Nginx dentro de la red de Docker)
EXPOSE 8000

# 7. Comando por defecto: Gunicorn (el paquete del proyecto se llama "Tienda")
CMD ["gunicorn", "Tienda.wsgi:application", "--bind", "0.0.0.0:8000"]