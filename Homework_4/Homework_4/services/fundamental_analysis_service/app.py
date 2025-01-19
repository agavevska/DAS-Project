from flask import Flask, jsonify
from analysis_factory.fundamental_analysis import FundamentalAnalysis

app = Flask(__name__)


@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        news = FundamentalAnalysis.fetchNews()
        sentiments = FundamentalAnalysis.analyze_sentiment(news)
        response = [{"news": n, "sentiment": s} for n, s in zip(news, sentiments)]
        return jsonify({"status": "success", "data": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
