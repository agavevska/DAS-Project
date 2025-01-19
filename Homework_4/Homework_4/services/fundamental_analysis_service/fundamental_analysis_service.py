from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/perform-analysis', methods=['GET'])
def perform_analysis():
    response = {
        "message": "Performing fundamental analysis...",
        "details": "Analyzing financial statements, calculating ratios, evaluating economic factors."
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5002)
