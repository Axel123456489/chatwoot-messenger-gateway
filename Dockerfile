FROM python:3.11-slim

# Variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependencias
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-root --no-dev

# Copiar código
COPY . /app

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
