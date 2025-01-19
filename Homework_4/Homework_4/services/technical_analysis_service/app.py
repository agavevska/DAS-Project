from flask import Flask, request, jsonify
from analysis_factory.technical_analysis import TechnicalAnalysis

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    company_name = data.get("company_name")
    file_path = data.get("file_path")  # Assumes data is sent in JSON format with file_path to the CSV file

    try:
        analysis = TechnicalAnalysis(file_path)
        analysis.preprocess_data()
        analysis.filter_company(company_name)
        analysis.calculate_indicators()
        response = analysis.company_data.to_dict(orient="records")
        return jsonify({"status": "success", "data": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
