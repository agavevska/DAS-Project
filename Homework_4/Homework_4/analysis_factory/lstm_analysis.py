import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.src.layers import LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
import tensorflow as tf


class LSTMAnalysis:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None
        self.model = None
        self.scaler = MinMaxScaler()
        self.n_lags = 5

    def load_and_preprocess_data(self):
        """
        Load the CSV data and preprocess it by creating lags, scaling, and splitting into features and target.
        """
        self.data = pd.read_csv(self.csv_path, delimiter=',')
        self.data['Датум'] = pd.to_datetime(self.data['Датум'], format='%d.%m.%Y')
        self.data = self.data.sort_values(by='Датум')

        # Create synthetic data for demonstration (optional, remove in production)
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=200, freq='D')
        price = np.sin(np.linspace(0, 20, 200)) + np.random.normal(0, 0.1, 200)
        self.data = pd.DataFrame({'Датум': dates, 'Цена на последна трансакција': price})

        # Create lags
        for lag in range(1, self.n_lags + 1):
            self.data[f'Price_Lag_{lag}'] = self.data['Цена на последна трансакција'].shift(lag)

        self.data.dropna(inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        # Scale data
        scaled_data = self.scaler.fit_transform(self.data.drop('Датум', axis=1))

        # Split into features (X) and target (Y)
        X = scaled_data[:, 1:]
        Y = scaled_data[:, 0]

        # Reshape X for LSTM input
        X = X.reshape((X.shape[0], self.n_lags, 1))
        return X, Y

    def build_model(self):
        """
        Build the LSTM model.
        """
        self.model = Sequential([
            Input(shape=(self.n_lags, 1)),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, x_train, y_train, epochs=50, batch_size=32):
        """
        Train the LSTM model on the training data.
        """
        self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1)

    def predict(self, x_test):
        """
        Make predictions using the trained LSTM model.
        """
        return self.model.predict(x_test)

    def plot_results(self, dates, y_test, predictions):
        """
        Plot the actual vs predicted results.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(dates[-len(y_test):], y_test, label='Actual Prices', color='blue')
        plt.plot(dates[-len(predictions):], predictions, label='Predicted Prices', color='red')
        plt.title('Stock Price Prediction')
        plt.xlabel('Date')
        plt.ylabel('Last Transaction Price')
        plt.legend()
        plt.show()
