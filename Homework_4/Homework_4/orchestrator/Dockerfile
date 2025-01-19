FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY orchestrator/requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the orchestrator files
COPY orchestrator/ /app/

# Expose port 5000 inside the container
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=orchestrator.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run the Flask app
CMD ["flask", "run"]

