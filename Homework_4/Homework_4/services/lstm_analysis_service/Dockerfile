FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker's layer caching
COPY services/lstm_analysis_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire service folder (includes app.py and other files)
COPY services/lstm_analysis_service/ .

# Expose port 5000 inside the container
EXPOSE 5000

# Run the LSTM analysis service
CMD ["python", "app.py"]
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003
