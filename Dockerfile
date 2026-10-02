# Python ki lightweight image use karna
FROM python:3.13-slim

# Container ke andar working directory set karna
WORKDIR /app

# Dependencies wali file container mein copy karna
COPY requirements.txt .

# Python packages install karna
RUN pip install --no-cache-dir -r requirements.txt

# API, model files aur doosri required files container mein copy karna
COPY api ./api
COPY models ./models
COPY data ./data

# FastAPI ka port expose karna
EXPOSE 8000

# FastAPI server start karna
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]