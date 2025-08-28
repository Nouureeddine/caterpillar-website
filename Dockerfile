# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
