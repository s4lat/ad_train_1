FROM python:3.8.5-slim
COPY . ./service
WORKDIR ./service
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir pastes

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers=2"]