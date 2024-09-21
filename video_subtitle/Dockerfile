# Use the official Python 3.12 base image
FROM python:3.12-slim

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install system dependencies
# ffmpeg is required for your video processing, and installing it with --no-install-recommends helps reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first, for more efficient layer caching
COPY requirements.txt .

# Install Python dependencies (using --no-cache-dir to avoid cache bloat)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Run the Django development server (replace with a production-ready server like Gunicorn in production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
