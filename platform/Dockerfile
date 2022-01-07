FROM python:3.8.5-slim
COPY . ./service
WORKDIR ./service
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p shared

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app", "--workers=2", "--preload"]