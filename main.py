
from IPython import embed
from google_trends import get_GT_data
from twitter import get_twitter_data
from chatgpt import use_chatgpt
from coin_api import get_coin_data
from reddit import get_reddit_data
from sentiment_analysis import compute_sentiment_analysis
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from sklearn.preprocessing import MinMaxScaler


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
reddit_data_full = get_reddit_data()

# Sentiment Analysis - WORK - F$
compute_sentiment_analysis(reddit_data_full)


# data_GT.set_index('date', inplace=True)
# data_coin.set_index('timestamp', inplace=True)

# Normalisation des données

#data_GT.set_index('date', inplace=True)
data_coin.set_index('timestamp', inplace=True)
scaler = MinMaxScaler()

data_GT['bitcoin_normalized'] = scaler.fit_transform(data_GT[['bitcoin']])
data_coin['open_normalized'] = scaler.fit_transform(data_coin[['open']])

# Alignement des dates
common_dates = data_GT.index.intersection(data_coin.index)
data_GT_aligned = data_GT.loc[common_dates]
data_coin_aligned = data_coin.loc[common_dates]

# Tracer les données
plt.figure(figsize=(14, 7))

plt.plot(data_GT_aligned.index, data_GT_aligned['bitcoin_normalized'], label='Bitcoin (Google Trends)', color='blue')
plt.plot(data_coin_aligned.index, data_coin_aligned['open_normalized'], label='Bitcoin (Open Price)', color='red')

plt.xlabel('Date')
plt.ylabel('Normalized Value')
plt.title('Normalized Bitcoin Values (Google Trends and Open Price)')
plt.legend()
plt.grid(True)
plt.show()