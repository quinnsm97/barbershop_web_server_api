# Use lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port
EXPOSE 8080

# Run app using gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} "main:create_app()"