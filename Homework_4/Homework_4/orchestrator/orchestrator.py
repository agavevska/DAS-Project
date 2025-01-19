import requests
import logging


class Orchestrator:
    def __init__(self, technical_url, fundamental_url, lstm_url):
        self.technical_analysis_url = technical_url
        self.fundamental_analysis_url = fundamental_url
        self.lstm_analysis_url = lstm_url

    def get_analysis_url(self, analysis_type):
        """
        Returns the service URL based on the analysis type.
        """
        if analysis_type == "technical":
            return self.technical_analysis_url
        elif analysis_type == "fundamental":
            return self.fundamental_analysis_url
        elif analysis_type == "lstm":
            return self.lstm_analysis_url
        else:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")

    def analyze_company(self, analysis_type, company_name, file_path):
        """
        Performs analysis by making requests to the appropriate service.
        """
        try:
            if analysis_type == "technical":
                url = self.get_analysis_url(analysis_type)
                response = requests.post(url, json={"company_name": company_name, "file_path": file_path})
                response.raise_for_status()  # Ensure request was successful
                data = response.json().get("data")
                return data
            elif analysis_type == "fundamental":
                url = self.get_analysis_url(analysis_type)
                response = requests.post(url, json={"company_name": company_name, "file_path": file_path})
                response.raise_for_status()  # Ensure request was successful
                data = response.json().get("data")
                return data
            elif analysis_type == "lstm":
                response = requests.post(self.lstm_analysis_url, json={"file_path": file_path})
                response.raise_for_status()  # Ensure request was successful
                predictions = response.json().get("predictions")
                return predictions
            else:
                raise ValueError(f"Unsupported analysis type: {analysis_type}")
        except Exception as e:
            logging.error(f"Error while performing analysis: {str(e)}")
            return None

    def fetch_service_data(self, service_url):
        """
        Fetches analysis results from the given service URL.
        """
        try:
            if not isinstance(service_url, str):
                raise TypeError(f"Expected a string URL, got {type(service_url).__name__} instead.")

            response = requests.get(service_url)
            response.raise_for_status()  # Ensure request was successful
            result = response.json()

            # Validate the JSON response
            if not isinstance(result, dict):  # Ensure result is a JSON object
                raise ValueError(f"Unexpected response format: {result}")

            return result
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from {service_url}: {e}")
            return {"error": f"Request failed: {str(e)}"}
        except ValueError as ve:
            logging.error(f"Invalid JSON from {service_url}: {ve}")
            return {"error": f"Invalid JSON response: {str(ve)}"}
        except TypeError as te:
            logging.error(str(te))
            return {"error": str(te)}


if __name__ == "__main__":
    orchestrator = Orchestrator(
        # technical_url="http://custom-url:5001",
        # fundamental_url="http://custom-url:5002",
        # lstm_url="http://custom-url:5003"
        technical_url="http://localhost:5001/perform-analysis",
        fundamental_url="http://localhost:5002/perform-analysis",
        lstm_url="http://localhost:5003/perform-analysis"
    )

    technical_data = orchestrator.analyze_company("technical", "Company A",
                                                  file_path="data/companies.csv")
    fundamental_data = orchestrator.analyze_company("fundamental",
                                                    "Company A",
                                                    file_path="data/companies_with_news.csv")
    lstm_predictions = orchestrator.analyze_company("lstm", "Company A",
                                                    file_path="data/companies.csv")
