import pandas as pd
import numpy as np
import ta

data=pd.read_csv("companies.csv")

def weighted_moving_average(data, window):
    weights = np.arange(1, window+1)
    return data.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

# Function for Triple Exponential Moving Average (TEMA)
def tema(data, window):
    ema1 = data.ewm(span=window, adjust=False).mean()
    ema2 = ema1.ewm(span=window, adjust=False).mean()
    ema3 = ema2.ewm(span=window, adjust=False).mean()
    return 3 * ema1 - 3 * ema2 + ema3

# Function for Hull Moving Average (HMA)
def hma(data, window):
    half_window = int(window / 2)
    sqrt_window = int(np.sqrt(window))
    wma_half = weighted_moving_average(data, half_window)
    wma_full = weighted_moving_average(data, window)
    diff = 2 * wma_half - wma_full
    return weighted_moving_average(diff, sqrt_window)

data['Датум'] = pd.to_datetime(data['Датум'], format='%d.%m.%Y')  # Convert to datetime
data = data.sort_values('Датум')  # Sort by date

# Convert necessary columns to numeric, handle errors (non-numeric) by coercing to NaN
data['Цена на последна трансакција'] = pd.to_numeric(data['Цена на последна трансакција'], errors='coerce')
data['Мак.'] = pd.to_numeric(data['Мак.'], errors='coerce')
data['Мин.'] = pd.to_numeric(data['Мин.'], errors='coerce')
data['Количина'] = pd.to_numeric(data['Количина'], errors='coerce')

# Fill missing values in 'Количина' with the mean
data['Количина'].fillna(data['Количина'].mean(), inplace=True)

for company in data['Име'].unique():
    company_data =data[data['Име'] == company].copy()

    company_data['SMA_1_day'] = company_data['Цена на последна трансакција'].rolling(window=1).mean()
    company_data['SMA_1_week'] = company_data['Цена на последна трансакција'].rolling(window=7).mean()
    company_data['SMA_1_month'] = company_data['Цена на последна трансакција'].rolling(window=30).mean()

    # Exponential Moving Averages (EMA)
    company_data['EMA_1_day'] = company_data['Цена на последна трансакција'].ewm(span=1, adjust=False).mean()
    company_data['EMA_1_week'] = company_data['Цена на последна трансакција'].ewm(span=7, adjust=False).mean()
    company_data['EMA_1_month'] = company_data['Цена на последна трансакција'].ewm(span=30, adjust=False).mean()

    # Weighted Moving Averages (WMA)
    company_data['WMA_1_day'] = weighted_moving_average(company_data['Цена на последна трансакција'], 1)
    company_data['WMA_1_week'] = weighted_moving_average(company_data['Цена на последна трансакција'], 7)
    company_data['WMA_1_month'] = weighted_moving_average(company_data['Цена на последна трансакција'], 30)

    # Triple Exponential Moving Averages (TEMA)
    company_data['TEMA_1_day'] = tema(company_data['Цена на последна трансакција'], 1)
    company_data['TEMA_1_week'] = tema(company_data['Цена на последна трансакција'], 7)
    company_data['TEMA_1_month'] = tema(company_data['Цена на последна трансакција'], 30)

    # Hull Moving Averages (HMA)
    company_data['HMA_1_day'] = hma(company_data['Цена на последна трансакција'], 1)
    company_data['HMA_1_week'] = hma(company_data['Цена на последна трансакција'], 7)
    company_data['HMA_1_month'] = hma(company_data['Цена на последна трансакција'], 30)




    # Relative Strength Index (RSI)
    company_data['RSI_1_day'] = ta.momentum.RSIIndicator(company_data['Цена на последна трансакција'], window=1).rsi()
    company_data['RSI_1_week'] = ta.momentum.RSIIndicator(company_data['Цена на последна трансакција'], window=7).rsi()
    company_data['RSI_1_month'] = ta.momentum.RSIIndicator(company_data['Цена на последна трансакција'], window=30).rsi()

    # Stochastic Oscillator
    company_data['stoch_1_day'] = ta.momentum.StochasticOscillator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=1, smooth_window=3).stoch()
    company_data['stoch_1_week'] = ta.momentum.StochasticOscillator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=7, smooth_window=3).stoch()
    company_data['stoch_1_month'] = ta.momentum.StochasticOscillator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=30, smooth_window=3).stoch()

    # MACD (Moving Average Convergence Divergence)
    company_data['macd'] = ta.trend.MACD(company_data['Цена на последна трансакција']).macd()
    company_data['macd_signal'] = ta.trend.MACD(company_data['Цена на последна трансакција']).macd_signal()

    # Commodity Channel Index (CCI)
    company_data['CCI_1_day'] = ta.trend.CCIIndicator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=1).cci()
    company_data['CCI_1_week'] = ta.trend.CCIIndicator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=7).cci()
    company_data['CCI_1_month'] = ta.trend.CCIIndicator(company_data['Мак.'], company_data['Мин.'], company_data['Цена на последна трансакција'], window=30).cci()

    company_data['ROC_1_day'] = ta.momentum.ROCIndicator(close=company_data['Цена на последна трансакција'], window=1).roc()
    company_data['ROC_1_week'] = ta.momentum.ROCIndicator(close=company_data['Цена на последна трансакција'], window=7).roc()
    company_data['ROC_1_month'] = ta.momentum.ROCIndicator(close=company_data['Цена на последна трансакција'], window=30).roc()


