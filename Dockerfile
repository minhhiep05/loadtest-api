# Stage 1: Build dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

# Install compilation tools for python packages with C extensions (like psutil)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install dependencies into user directory to copy them easily
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Run container
FROM python:3.10-slim AS runner

WORKDIR /app

# Copy user installed packages from builder stage
COPY --from=builder /root/.local /root/.local
# Copy source code and templates
COPY . /app

# Add user bin path to environment PATH
ENV PATH=/root/.local/bin:$PATH
# Keep python console outputs unbuffered
ENV PYTHONUNBUFFERED=1

EXPOSE 3000

# Start with Gunicorn WSGI server for production load management
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "4", "--threads", "2", "app:app"]

