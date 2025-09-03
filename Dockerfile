# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Railway sets PORT dynamically, so use it
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Run with gunicorn (production server)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:${PORT}"]
