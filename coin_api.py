
import matplotlib.pyplot as plt
import pandas as pd
from binance.client import Client
from IPython import embed

def get_coin_data(coin_symbol, coin_name):
    ## Binance
    # Remplacez par vos propres clés API
    api_key = 'Rp8pxiHSFqSxlD1pvUjb2czLifDUoQdEVtzxnTztCRBs63chv5WY3Z1qNt5SAYTz'
    api_secret = 'nghpTVsUkv7xRr4maVBsJcSVjHvF3YtChcHzyVAJumyG7Jy1c6CbGSW0j43XIRCv'

    # Initialisation du client
    client = Client(api_key, api_secret)

    # Récupérer les prix historiques de BTC/USDT en utilisant l'intervalle journalier
    symbol = coin_symbol
    interval = '1h'#Client.KLINE_INTERVAL_1DAY
    start_str = '2021-01-01'

    # Fonction pour obtenir les prix historiques de BTC/USDT
    klines = client.get_historical_klines(symbol, interval, start_str)

    # Convertir les données en DataFrame pandas
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                                        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                                        'taker_buy_quote_asset_volume', 'ignore'])

    # Convertir les timestamps en datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    # Convertir les colonnes de prix en flottants
    data['close'] = data['close'].astype(float)

    # # Créer le graphique
    label = coin_name+"/USDT"
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['close'], label=label)
    plt.xlabel('Date')
    plt.ylabel('Prix (USD)')
    plt.title('Prix de '+ coin_name + ' en fonction du dollar américain (USD)')
    plt.legend()
    plt.grid(True)
    
    #plt.show()
    return data