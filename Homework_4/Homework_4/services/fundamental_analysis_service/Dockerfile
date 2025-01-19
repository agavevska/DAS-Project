FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY services/fundamental_analysis_service/requirements.txt ./requirements.txt

COPY . /app

# Install any dependencies in requirements.txt
 pip install --no-cache-dir -r requirements.txt/

# Expose port 5000 to the outside world
EXPOSE 5000

# Set environment variable to prevent Python from writing pyc files
ENV PYTHONUNBUFFERED = 1

# Run the Flask app when the container starts
CMD ["python", "app.py"]

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
