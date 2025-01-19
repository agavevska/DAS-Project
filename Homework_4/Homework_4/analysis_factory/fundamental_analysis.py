import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt


class FundamentalAnalysis:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None
        self.recommendations_df = None
        nltk.download('vader_lexicon')
        self.sia = SentimentIntensityAnalyzer()

    def load_and_preprocess_data(self):
        self.data = pd.read_csv(self.csv_path)
        self.data = self.data.dropna(subset=['Опис'])

    def analyze_sentiment(self, description):
        sentiment = self.sia.polarity_scores(description)
        return sentiment['compound']

    def generate_recommendations(self):
        grouped_data = self.data.groupby('Компанија')

        recommendations = []
        for name, group in grouped_data:
            group['Sentiment'] = group['Опис'].apply(self.analyze_sentiment)
            sentiment_score = group['Sentiment'].mean()
            recommendation = 'Buy' if sentiment_score > 0 else 'Sell'

            recommendations.append({
                'Компанија': name,
                'Средна оценка за сентимент': sentiment_score,
                'Рекомендација': recommendation
            })

        self.recommendations_df = pd.DataFrame(recommendations)
        return self.recommendations_df

    def save_recommendations(self, output_path):
        if self.recommendations_df is not None:
            self.recommendations_df.to_csv(output_path, index=False)
        else:
            raise ValueError("Recommendations not generated. Please run generate_recommendations() first.")

    def plot_heatmap(self):
        if self.recommendations_df is not None:
            plt.figure(figsize=(14, 20))
            heatmap_data = self.recommendations_df.pivot(
                index="Компанија",
                columns="Рекомендација",
                values="Средна оценка за сентимент"
            )
            sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", linewidths=.5)
            plt.title('Sentiment Analysis Heatmap')
            plt.xlabel('Рекомендација')
            plt.ylabel('Компанија')
            plt.show()
        else:
            raise ValueError("Recommendations not generated. Please run generate_recommendations() first.")


# Example usage:
if __name__ == "__main__":
    analysis = FundamentalAnalysis(csv_path='companies_with_news.csv')
    analysis.load_and_preprocess_data()
    recommendations = analysis.generate_recommendations()
    analysis.save_recommendations(output_path='recommendations.csv')
    analysis.plot_heatmap()
