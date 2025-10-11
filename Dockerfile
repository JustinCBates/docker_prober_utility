FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    iproute2 \
    net-tools \
    procps \
    util-linux \
    systemd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application files
COPY app.py /app/app.py
COPY scripts/ /app/scripts/
COPY entrypoint.sh /app/entrypoint.sh

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/scripts/*.sh /app/scripts/*.py

# Install Python dependencies (rich is optional, installed separately)
RUN pip install --no-cache-dir flask

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]