from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/perform-analysis', methods=['GET'])
def perform_analysis():
    response = {
        "message": "Performing technical analysis..."
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5001)
