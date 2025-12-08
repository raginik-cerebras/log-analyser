FROM python:3.10-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . /app/

# Make start script executable
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
