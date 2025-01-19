import os
import requests
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Load service URLs from environment variables (with defaults for local testing)
TECHNICAL_SERVICE_URL = os.getenv("TECHNICAL_SERVICE_URL", "http://localhost:5001/perform-analysis")
LSTM_SERVICE_URL = os.getenv("LSTM_SERVICE_URL", "http://localhost:5002/perform-analysis")
FUNDAMENTAL_SERVICE_URL = os.getenv("FUNDAMENTAL_SERVICE_URL", "http://localhost:5003/perform-analysis")


def get_analysis(service_url):
    """
    Fetches analysis results from the given service URL.

    Args:
        service_url (str): The URL of the service to query.

    Returns:
        dict: The JSON response from the service or an error message.
    """
    try:
        response = requests.get(service_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {service_url}: {e}")
        return {"error": str(e)}


@app.route('/aggregate-analysis', methods=['GET'])
def aggregate_analysis():
    """
    Aggregates results from all analysis services and returns them in a combined response.

    Returns:
        dict: A combined JSON object containing results from all services.
    """
    logging.info("Starting to aggregate analysis results...")

    # Call each service and collect results
    technical_result = get_analysis(TECHNICAL_SERVICE_URL)
    lstm_result = get_analysis(LSTM_SERVICE_URL)
    fundamental_result = get_analysis(FUNDAMENTAL_SERVICE_URL)

    # Combine results into a single response
    aggregated_result = {
        "technical_analysis": technical_result,
        "lstm_analysis": lstm_result,
        "fundamental_analysis": fundamental_result,
    }

    logging.info("Aggregation complete.")
    return jsonify(aggregated_result)


if __name__ == "__main__":
    # Run the Flask app
    logging.info("Starting Orchestrator Service...")
    app.run(host='0.0.0.0', port=5000)
