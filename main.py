
from IPython import embed
import calendar
from google_trends import get_GT_data
from hotwallets import get_top_whales
#from twitter import get_twitter_data
from chatgpt import use_chatgpt
from coin_api import get_coin_data
from reddit import get_reddit_data
from sentiment_analysis import compute_sentiment_analysis
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from sklearn.preprocessing import MinMaxScaler
import requests
from datetime import datetime, timedelta

"""
import numpy as np  
import tensorflow as tf  
import pandas as pd  
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import MinMaxScaler  
import matplotlib.pyplot as plt 
"""

## IMPORT DATA
# Google Trends - F$
data_GT = get_GT_data()
print('Data GT', data_GT)

# ChatGPT - WORK - $$$
# answer = use_chatgpt()

# Twitter - DONT WORK - $$$
#data_Twitter = get_twitter_data()
#print('Data GT', data_GT)
#embed()

# Coin data - WORK - F$
data_coin = get_coin_data()

#Reddit- WORK - F$
#reddit_data_full = get_reddit_data()

# Sentiment Analysis - WORK - F$
#compute_sentiment_analysis(reddit_data_full)

# HOT WALLETS data
get_top_whales()
ETHERSCAN_API_KEY = "V7HQQVDRZRA18F197P5CDEJIE446EMHHSG"
#whales, best_performers = get_whales_and_best_performers(ETHERSCAN_API_KEY)
#print("Top 100 Whales (By Balance):")
#print(whales)
#print("\nTop 100 Best Performers (By Profit):")
#print(best_performers)


# NORMALIZED DATA
#data_GT.set_index('date', inplace=True)
data_coin.set_index('timestamp', inplace=True)
scaler = MinMaxScaler()

data_GT['bitcoin_normalized'] = scaler.fit_transform(data_GT[['bitcoin']])
data_coin['open_normalized'] = scaler.fit_transform(data_coin[['open']])


## ANALYZE
# Alignement des dates
common_dates = data_GT.index.intersection(data_coin.index)
data_GT_aligned = data_GT.loc[common_dates]
data_coin_aligned = data_coin.loc[common_dates]






## PLOTS
plt.figure(figsize=(14, 7))

plt.plot(data_GT_aligned.index, data_GT_aligned['bitcoin_normalized'], label='Bitcoin (Google Trends)', color='blue')
plt.plot(data_coin_aligned.index, data_coin_aligned['open_normalized'], label='Bitcoin (Open Price)', color='red')

plt.xlabel('Date')
plt.ylabel('Normalized Value')
plt.title('Normalized Bitcoin Values (Google Trends and Open Price)')
plt.legend()
plt.grid(True)
#plt.show()
"""

 

# Création des séquences temporelles  
def create_sequences(data, seq_length):  
    sequences, targets = [], []  
    for i in range(len(data) - seq_length):  
        seq = data[i:i + seq_length]  
        target = data[i + seq_length]  
        sequences.append(seq)  
        targets.append(target)  
    return np.array(sequences), np.array(targets)  

# Récupération et normalisation des données  
data_GT = get_GT_data()  
data_coin = get_coin_data()  
data_GT.set_index('date', inplace=True)  
data_coin.set_index('timestamp', inplace=True)  
scaler = MinMaxScaler()  
data_GT['bitcoin_normalized'] = scaler.fit_transform(data_GT[['bitcoin']])  
data_coin['open_normalized'] = scaler.fit_transform(data_coin[['open']])  

# Alignement des données et création des séquences  
common_dates = data_GT.index.intersection(data_coin.index)  
merged_data = pd.concat([data_GT.loc[common_dates]['bitcoin_normalized'], data_coin.loc[common_dates]['open_normalized']], axis=1)  
SEQ_LENGTH = 30  
X, y = create_sequences(merged_data.values, SEQ_LENGTH)  

# Division en ensembles d'entraînement et de test  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)  

# Modèle Transformer  
def build_transformer_model(input_shape):  
    inputs = tf.keras.Input(shape=input_shape)  
    x = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=16)(inputs, inputs)  
    x = tf.keras.layers.GlobalAveragePooling1D()(x)  
    x = tf.keras.layers.Dense(64, activation='relu')(x)  
    x = tf.keras.layers.Dropout(0.2)(x)  
    outputs = tf.keras.layers.Dense(1)(x)  
    model = tf.keras.Model(inputs, outputs)  
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])  
    return model  

model = build_transformer_model((SEQ_LENGTH, 2))  

# Entraînement du modèle  
history = model.fit(X_train, y_train, validation_split=0.1, epochs=50, batch_size=32)  

# Prédictions et visualisation  
y_pred = model.predict(X_test)  
plt.figure(figsize=(14, 7))  
plt.plot(y_test, label="True Price")  
plt.plot(y_pred, label="Predicted Price")  
plt.legend()  
plt.title("Bitcoin Price Prediction")  
plt.show()


"""