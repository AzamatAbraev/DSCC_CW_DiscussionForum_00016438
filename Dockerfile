# Stage 1: Build dependencies
FROM python:3.11-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

# Stage 2: Final Runtime
FROM python:3.11-slim
WORKDIR /app/discussion_forum_00016438

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Install runtime database library
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy the entire project
COPY . /app/

# Set permissions
RUN mkdir -p staticfiles media && chown -R app:app /app

USER app
ENV PYTHONPATH="/app/discussion_forum_00016438"

# Run Gunicorn using the config file from the root
CMD ["gunicorn", "-c", "/app/gunicorn.conf.py", "config.wsgi:application"]