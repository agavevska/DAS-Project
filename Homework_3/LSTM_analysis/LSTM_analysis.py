import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.src.layers import LSTM
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
import tensorflow as tf

# Читање и препроцесирање на податоците
data = pd.read_csv('companies.csv', delimiter=',')
data['Датум'] = pd.to_datetime(data['Датум'], format='%d.%m.%Y')
data = data.sort_values(by='Датум')

np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=200, freq='D')
price = np.sin(np.linspace(0, 20, 200)) + np.random.normal(0, 0.1, 200)
data = pd.DataFrame({'Датум': dates, 'Цена на последна трансакција': price})

# Креирање лагови
n_lags = 5
for lag in range(1, n_lags + 1):
    data[f'Price_Lag_{lag}'] = data['Цена на последна трансакција'].shift(lag)

data.dropna(inplace=True)
data.reset_index(drop=True, inplace=True)

# Скалирање
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data.drop('Датум', axis=1))

# Одредување карактеристики X и таргет Y
X = scaled_data[:, 1:]
Y = scaled_data[:, 0]

# Преобликување на X во 3D за влез LSTM (примероци, временски чекори, карактеристики)
# # Го користиме бројот на заостанувања како временски чекори
X = X.reshape((X.shape[0], n_lags, 1))

# Поделба во сетови за тренирање и тестирање во однос 70:30
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Создавања LSTM модел
model = Sequential([
    Input(shape=(n_lags, 1)),
    LSTM(50, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# Create sequences
def create_sequences(data, sequence_length):
    x, y = [], []
    for i in range(len(data) - sequence_length):
        x.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(x), np.array(y)


# Промена на X_train од 3D во 2D
X_train_flat = X_train.reshape(X_train.shape[0], -1)

# Комбинација на X_train_flat со y_train (се преобликува во 2D доколку е потребно)
train_data_combined = np.hstack((X_train_flat, y_train.reshape(-1, 1)))

# Истото се случува и со сетот за тестирање
X_test_flat = X_test.reshape(X_test.shape[0], -1)
test_data_combined = np.hstack((X_test_flat, y_test.reshape(-1, 1)))

# Создавање LSTM модел
model = Sequential([
    Input(shape=(X_train.shape[1], 1)),
    LSTM(50, return_sequences=True),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Тренирање модел
history = model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test), verbose=1)

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')

# Прикажување резултати
plt.figure(figsize=(10, 6))
plt.plot(data['Датум'][-len(y_test):], y_test, label='Вистински цени', color='blue')
plt.plot(data['Датум'][-len(predictions):], predictions, label='Предвидени цени', color='red')
plt.title('Предвидување на цената на акциите')
plt.xlabel('Датум')
plt.ylabel('Цена на последна трансакција')
plt.legend()
plt.show()
