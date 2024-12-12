
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
import seaborn as sns
import pandas_ta as ta

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
#data_GT = get_GT_data()
#print('Data GT', data_GT)

# ChatGPT - WORK - $$$
# answer = use_chatgpt()

# Twitter - DONT WORK - $$$
#data_Twitter = get_twitter_data()
#print('Data GT', data_GT)
#embed()

# Coin data - WORK - F$
# Import actual value
#data_BTC = get_coin_data("BTCUSDT", "BTC")
#data_ETH = get_coin_data("ETHUSDT", "ETH")

# Save loaded value
#data_BTC.to_csv('btc_hourly_data.csv', index=False)
#data_ETH.to_csv('eth_hourly_data.csv', index=False)

# Open previously saved value
data_BTC = pd.read_csv('btc_hourly_data.csv', index_col='timestamp', parse_dates=True)
data_ETH = pd.read_csv('eth_hourly_data.csv', index_col='timestamp', parse_dates=True)



#Reddit- WORK - F$
#reddit_data_full = get_reddit_data()

# Sentiment Analysis - WORK - F$
#compute_sentiment_analysis(reddit_data_full)

# HOT WALLETS data
# get_top_whales()
ETHERSCAN_API_KEY = "V7HQQVDRZRA18F197P5CDEJIE446EMHHSG"
#whales, best_performers = get_whales_and_best_performers(ETHERSCAN_API_KEY)
#print("Top 100 Whales (By Balance):")
#print(whales)
#print("\nTop 100 Best Performers (By Profit):")
#print(best_performers)
#data_GT.set_index('date', inplace=True)
#data_BTC.set_index('timestamp', inplace=True)



# NORMALIZED DATA
scaler = MinMaxScaler()
#data_GT['bitcoin_normalized'] = scaler.fit_transform(data_GT[['bitcoin']])
data_BTC['open_normalized'] = scaler.fit_transform(data_BTC[['open']])
data_ETH['open_normalized'] = scaler.fit_transform(data_ETH[['open']])

## ANALYZE
# Alignement des dates
#common_dates = data_GT.index.intersection(data_BTC.index)
#data_GT_aligned = data_GT.loc[common_dates]
#data_coin_aligned = data_BTC.loc[common_dates]

# Correlation 
merged_data = pd.concat([data_BTC['close'].rename('close_BTC'), data_ETH['close'].rename('close_ETH')], axis=1)
correlation_matrix = merged_data.corr()


# Correlation glissante
# Calcul de la corrélation glissante sur une fenêtre de 30 jours (720 heures)
rolling_corr = merged_data['close_BTC'].rolling(window=720).corr(merged_data['close_ETH'])


data_BTC['rsi'] = ta.rsi(data_BTC['close'])
data_ETH['rsi'] = ta.rsi(data_ETH['close'])

data_BTC['macd'] = ta.macd(data_BTC['close'])['MACD_12_26_9']
data_ETH['macd'] = ta.macd(data_ETH['close'])['MACD_12_26_9']


## PLOTS
# Correlation - heatmap
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Matrice de Corrélation des Cryptos")

# Tracé de la corrélation glissante
plt.figure(figsize=(12, 6))
rolling_corr.plot(color='blue', label='Corrélation Glissante (30 jours)')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8, label='Corrélation = 0')
plt.title('Corrélation Glissante Hebdomadaire entre BTC et ETH')
plt.xlabel('Temps')
plt.ylabel('Corrélation')
plt.legend()
plt.grid()
plt.show()


# Création d'une figure avec 4 sous-graphiques
fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True)
fig.suptitle("RSI et MACD pour BTC et ETH", fontsize=16)

# Graphique RSI pour BTC
axes[0, 0].plot(data_BTC.index, data_BTC['rsi'], color='blue', label='RSI BTC')
axes[0, 0].axhline(70, color='red', linestyle='--', linewidth=0.8, label='Seuil de surachat (70)')
axes[0, 0].axhline(30, color='green', linestyle='--', linewidth=0.8, label='Seuil de survente (30)')
axes[0, 0].set_title("RSI BTC")
axes[0, 0].set_ylabel("RSI")
axes[0, 0].legend()
axes[0, 0].grid()

# Graphique RSI pour ETH
axes[0, 1].plot(data_ETH.index, data_ETH['rsi'], color='orange', label='RSI ETH')
axes[0, 1].axhline(70, color='red', linestyle='--', linewidth=0.8, label='Seuil de surachat (70)')
axes[0, 1].axhline(30, color='green', linestyle='--', linewidth=0.8, label='Seuil de survente (30)')
axes[0, 1].set_title("RSI ETH")
axes[0, 1].set_ylabel("RSI")
axes[0, 1].legend()
axes[0, 1].grid()

# Graphique MACD pour BTC
axes[1, 0].plot(data_BTC.index, data_BTC['macd'], color='blue', label='MACD BTC')
axes[1, 0].axhline(0, color='black', linestyle='--', linewidth=0.8, label='Ligne neutre')
axes[1, 0].set_title("MACD BTC")
axes[1, 0].set_ylabel("MACD")
axes[1, 0].legend()
axes[1, 0].grid()

# Graphique MACD pour ETH
axes[1, 1].plot(data_ETH.index, data_ETH['macd'], color='orange', label='MACD ETH')
axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=0.8, label='Ligne neutre')
axes[1, 1].set_title("MACD ETH")
axes[1, 1].set_ylabel("MACD")
axes[1, 1].legend()
axes[1, 1].grid()

# Ajuster les espaces entre les graphiques
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Google trends et BTC aligned
#plt.figure(figsize=(14, 7))
#plt.plot(data_GT_aligned.index, data_GT_aligned['bitcoin_normalized'], label='Bitcoin (Google Trends)', color='blue')
#plt.plot(data_coin_aligned.index, data_coin_aligned['open_normalized'], label='Bitcoin (Open Price)', color='red')
#plt.xlabel('Date')
#plt.ylabel('Normalized Value')
#plt.title('Normalized Bitcoin Values (Google Trends and Open Price)')
#plt.legend()
#plt.grid(True)
#plt.show()
