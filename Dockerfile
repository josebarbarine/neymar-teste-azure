FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

# ESSA É A LINHA MÁGICA: O Python vai abrir todos os arquivos .py e trocar o espaço alienígena por um espaço normal
RUN python -c "import os; [open(f, 'w', encoding='utf-8').write(open(f, 'r', encoding='utf-8').read().replace('\xa0', ' ')) for f in os.listdir('.') if f.endswith('.py')]"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
