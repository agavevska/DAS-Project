from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split

from analysis_factory.lstm_analysis import LSTMAnalysis

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    csv_path = data.get("file_path")
    try:
        analysis = LSTMAnalysis(csv_path)
        X, Y = analysis.load_and_preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
        analysis.build_model()
        analysis.train_model(X_train, y_train)
        predictions = analysis.predict(X_test)
        return jsonify({"status": "success", "predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
