FROM python:3.8-slim

WORKDIR /app
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./run_scanner.sh /app
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/run_scanner.sh
CMD ["./run_scanner.sh"]
