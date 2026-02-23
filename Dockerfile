# Použijeme oficiální Python image
FROM python:3.11-slim

# Nastavíme pracovní adresář
WORKDIR /app

# Zkopírujeme requirements a nainstalujeme závislosti
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopírujeme celý projekt do kontejneru
COPY . .

# Port pro FastAPI
EXPOSE 8000

# Příkaz pro spuštění aplikace
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]