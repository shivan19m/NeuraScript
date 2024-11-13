FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the source code, tests, and requirements
COPY ./src /app/src
COPY ./tests /app/tests
COPY ./run_scanner.sh /app
COPY ./parser.py /app/src
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Make the run_scanner.sh executable
RUN chmod +x /app/run_scanner.sh

# Set the entry point for the container
CMD ["./run_scanner.sh"]