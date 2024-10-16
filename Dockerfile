FROM python:3.8-slim 
WORKDIR /app
COPY ./src /app/src
COPY ./test /app/test
COPY ./run_scanner.sh /app
RUN pip install --no-cache-dir
CMD ["./run_scanner.sh"]
