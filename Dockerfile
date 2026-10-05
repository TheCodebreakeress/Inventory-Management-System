# Use official lightweight Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency definition file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without caching to keep image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the container
COPY . .

# Ensure the SQLite data directory exists
RUN mkdir -p /app/data

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run FastAPI with Uvicorn (production mode, no reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
