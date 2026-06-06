FROM python:3.11-slim

WORKDIR /app

COPY flask/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask/ .

EXPOSE 5005

CMD ["gunicorn", "--bind", "0.0.0.0:5005", "app:app"]
