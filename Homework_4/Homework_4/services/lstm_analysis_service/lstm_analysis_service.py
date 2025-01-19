from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/perform-analysis', methods=['GET'])
def perform_analysis():
    response = {
        "message": "Performing LSTM analysis...",
        "details": "Training model, predicting trends from time-series data."
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5003)
