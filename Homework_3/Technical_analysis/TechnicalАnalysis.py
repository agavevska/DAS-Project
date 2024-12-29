import base64
import sys
from io import BytesIO

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ta

sys.stdout.reconfigure(encoding='utf-8')
import warnings

warnings.filterwarnings("ignore")

if len(sys.argv) < 2:
    print("Недостасува аргумент за името на компанијата.")
    sys.exit(1)  # Прекини ја програмата ако нема доволно аргументи

company_name = sys.argv[1]

data = pd.read_csv("C:/Users/User/DAS-Project/Homework_1/companies.csv")




def visualization(company_data):
    plt.figure(figsize=(12, 6))

    # Линеарен графикон за цените
    plt.plot(company_data.index, company_data['Цена на последна трансакција'], label='Цена на последна трансакција', color='blue')

    # Обележување на сигналите за купување (зелена точка)
    buy_signals = company_data[company_data['final_signal'] == 'buy']
    plt.scatter(buy_signals.index, buy_signals['Цена на последна трансакција'], marker='^', color='green', label='Сигнал за купување', alpha=1)

    # Обележување на сигналите за продавање (црвена точка)
    sell_signals = company_data[company_data['final_signal'] == 'sell']
    plt.scatter(sell_signals.index, sell_signals['Цена на последна трансакција'], marker='v', color='red', label='Сигнал за продавање', alpha=1)

    # Додавање на наслов и ознаки
    plt.title('Визуализација на сигнали за купување и продавање на ' + company_data['Име'].iloc[0])
    plt.xlabel('Дата')
    plt.ylabel('Цена на последна трансакција')

    # Форматирање на датите на оската X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    plt.gcf().autofmt_xdate()

    # Додавање легенда
    plt.legend()

    # Поставување на графиконот
    plt.tight_layout()
    # plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Кодирање на сликата во Base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Враќање на Base64 кодираниот резултат
    print(img_base64)




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

# for company in data['Име'].unique():
company_data =data[data['Име'] == company_name ].copy()

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

company_data['SMA_signal'] = np.where(company_data['SMA_1_day'] > company_data['SMA_1_week'], 'buy', 'sell')
company_data['EMA_signal'] = np.where(company_data['EMA_1_day'] > company_data['Цена на последна трансакција'],
                                          'buy', 'sell')
company_data['WMA_signal'] = np.where(company_data['WMA_1_day'] > company_data['Цена на последна трансакција'],
                                          'buy', 'sell')
company_data['TEMA_signal'] = np.where(company_data['TEMA_1_day'] > company_data['Цена на последна трансакција'],
                                           'buy', 'sell')
company_data['HMA_signal'] = np.where(company_data['HMA_1_day'] > company_data['Цена на последна трансакција'],
                                          'buy', 'sell')
company_data['RSI_signal'] = np.where(company_data['RSI_1_day'] < 30, 'buy', 'sell')
company_data['stoch_signal'] = np.where(company_data['stoch_1_day'] < 20, 'buy', 'sell')
company_data['macd_signal'] = np.where(company_data['macd'] > company_data['macd_signal'], 'buy', 'sell')
company_data['CCI_signal'] = np.where(company_data['CCI_1_day'] > 100, 'buy', 'sell')

    # Генерирање на финален сигнал врз основа на комбинација од сите индикатори
company_data['final_signal'] = np.select(
        [
            (company_data['SMA_signal'] == 'buy') | (company_data['EMA_signal'] == 'buy') | (
                        company_data['WMA_signal'] == 'buy') |
            (company_data['TEMA_signal'] == 'buy') | (company_data['HMA_signal'] == 'buy') | (
                        company_data['RSI_signal'] == 'buy') |
            (company_data['stoch_signal'] == 'buy') | (company_data['macd_signal'] == 'buy') | (
                        company_data['CCI_signal'] == 'buy'),
            (company_data['SMA_signal'] == 'sell') | (company_data['EMA_signal'] == 'sell') | (
                        company_data['WMA_signal'] == 'sell') |
            (company_data['TEMA_signal'] == 'sell') | (company_data['HMA_signal'] == 'sell') | (
                        company_data['RSI_signal'] == 'sell') |
            (company_data['stoch_signal'] == 'sell') | (company_data['macd_signal'] == 'sell') | (
                        company_data['CCI_signal'] == 'sell')
        ],
        ['buy', 'sell'],
        default='hold'

)


visualization(company_data)


