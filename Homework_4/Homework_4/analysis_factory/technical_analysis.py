import pandas as pd
import numpy as np
import ta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")


class TechnicalAnalysis:
    def __init__(self, data_path):
        """
        Initialize the TechnicalAnalysis class with the data file path.

        :param data_path: Path to the CSV file containing company stock data.
        """
        self.data = pd.read_csv(data_path)
        self.company_data = None

    def preprocess_data(self):
        """
        Preprocess the data by sorting, converting columns to numeric, and filling missing values.
        """
        self.data['Датум'] = pd.to_datetime(self.data['Датум'], format='%d.%m.%Y')
        self.data = self.data.sort_values('Датум')

        # Convert necessary columns to numeric, handle errors by coercing to NaN
        numeric_columns = ['Цена на последна трансакција', 'Мак.', 'Мин.', 'Количина']
        for col in numeric_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')

        # Fill missing values in 'Количина' with the mean
        self.data['Количина'].fillna(self.data['Количина'].mean(), inplace=True)

    def filter_company(self, company_name):
        """
        Filter the dataset for a specific company.

        :param company_name: Name of the company to filter data for.
        """
        self.company_data = self.data[self.data['Име'] == company_name].copy()

    @staticmethod
    def weighted_moving_average(data, window):
        """
        Calculate the Weighted Moving Average (WMA).

        :param data: Series of data.
        :param window: Window size for WMA.
        :return: Weighted Moving Average as a pandas Series.
        """
        weights = np.arange(1, window + 1)
        return data.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

    @staticmethod
    def tema(data, window):
        """
        Calculate the Triple Exponential Moving Average (TEMA).

        :param data: Series of data.
        :param window: Window size for TEMA.
        :return: Triple Exponential Moving Average as a pandas Series.
        """
        ema1 = data.ewm(span=window, adjust=False).mean()
        ema2 = ema1.ewm(span=window, adjust=False).mean()
        ema3 = ema2.ewm(span=window, adjust=False).mean()
        return 3 * ema1 - 3 * ema2 + ema3

    @staticmethod
    def hma(data, window):
        """
        Calculate the Hull Moving Average (HMA).

        :param data: Series of data.
        :param window: Window size for HMA.
        :return: Hull Moving Average as a pandas Series.
        """
        half_window = int(window / 2)
        sqrt_window = int(np.sqrt(window))
        wma_half = TechnicalAnalysis.weighted_moving_average(data, half_window)
        wma_full = TechnicalAnalysis.weighted_moving_average(data, window)
        diff = 2 * wma_half - wma_full
        return TechnicalAnalysis.weighted_moving_average(diff, sqrt_window)

    def calculate_indicators(self):
        """
        Calculate various technical indicators and signals.
        """
        if self.company_data is None:
            raise ValueError("Company data not filtered. Call filter_company() first.")

        # Moving Averages
        self.company_data['SMA_1_day'] = self.company_data['Цена на последна трансакција'].rolling(window=1).mean()
        self.company_data['SMA_1_week'] = self.company_data['Цена на последна трансакција'].rolling(window=7).mean()
        self.company_data['SMA_1_month'] = self.company_data['Цена на последна трансакција'].rolling(window=30).mean()

        # Exponential Moving Averages (EMA)
        self.company_data['EMA_1_day'] = self.company_data['Цена на последна трансакција'].ewm(span=1,
                                                                                               adjust=False).mean()
        self.company_data['EMA_1_week'] = self.company_data['Цена на последна трансакција'].ewm(span=7,
                                                                                                adjust=False).mean()
        self.company_data['EMA_1_month'] = self.company_data['Цена на последна трансакција'].ewm(span=30,
                                                                                                 adjust=False).mean()

        # Weighted, Triple Exponential, and Hull Moving Averages
        self.company_data['WMA_1_day'] = self.weighted_moving_average(self.company_data['Цена на последна трансакција'],
                                                                      1)
        self.company_data['TEMA_1_week'] = self.tema(self.company_data['Цена на последна трансакција'], 7)
        self.company_data['HMA_1_month'] = self.hma(self.company_data['Цена на последна трансакција'], 30)

        # RSI, Stochastic Oscillator, and MACD
        self.company_data['RSI'] = ta.momentum.RSIIndicator(self.company_data['Цена на последна трансакција'],
                                                            window=14).rsi()
        self.company_data['stoch'] = ta.momentum.StochasticOscillator(
            high=self.company_data['Мак.'],
            low=self.company_data['Мин.'],
            close=self.company_data['Цена на последна трансакција'],
            window=14,
            smooth_window=3
        ).stoch()
        macd = ta.trend.MACD(self.company_data['Цена на последна трансакција'])
        self.company_data['macd'] = macd.macd()
        self.company_data['macd_signal'] = macd.macd_signal()

    def visualize_signals(self):
        """
        Visualize buy and sell signals for the company data.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.company_data.index, self.company_data['Цена на последна трансакција'],
                 label='Цена на последна трансакција', color='blue')

        # Highlight buy and sell signals
        buy_signals = self.company_data[self.company_data['RSI'] < 30]
        sell_signals = self.company_data[self.company_data['RSI'] > 70]

        plt.scatter(buy_signals.index, buy_signals['Цена на последна трансакција'], marker='^', color='green',
                    label='Buy Signal', alpha=1)
        plt.scatter(sell_signals.index, sell_signals['Цена на последна трансакција'], marker='v', color='red',
                    label='Sell Signal', alpha=1)

        plt.title(f"Technical Analysis Signals for {self.company_data['Име'].iloc[0]}")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.tight_layout()

        # Save the plot as base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return img_base64
