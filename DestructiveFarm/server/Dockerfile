FROM python:3.8.5-slim
COPY . ./server
WORKDIR ./server
RUN pip install --no-cache-dir -r requirements.txt

CMD ["./start_server.sh"]