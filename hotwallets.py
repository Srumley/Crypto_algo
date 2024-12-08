from IPython import embed
import requests
import pandas as pd
import calendar
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup



def get_whales_and_best_performers(ETHERSCAN_API_KEY):
    # Étape 1 : Récupérer les 100 plus gros portefeuilles
    whales = get_top_wallets_by_balance()
    
    # Étape 2 : Récupérer les portefeuilles ayant réalisé les meilleurs bénéfices
    best_performers = get_top_wallets_by_profit(ETHERSCAN_API_KEY)
    
    return whales, best_performers


def get_top_wallets_by_balance(ETHERSCAN_API_KEY):
    """
    Obtenir les 100 plus gros portefeuilles en fonction de leur solde.
    """
    url = f"https://api.etherscan.io/api?module=account&action=balancemulti&address={get_top_wallets_addresses()}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    
    response = requests.get(url).json()
    
    if response["status"] != "1":
        raise ValueError(f"Erreur Etherscan : {response['message']}")

    wallets = response["result"]
    
    # Trier les portefeuilles par solde décroissant
    sorted_wallets = sorted(wallets, key=lambda x: int(x["balance"]), reverse=True)
    
    # Prendre les 100 premiers
    top_100_whales = sorted_wallets[:100]
    
    # Convertir en DataFrame pour une meilleure lisibilité
    df_whales = pd.DataFrame(top_100_whales)
    df_whales["balance"] = df_whales["balance"].astype(float) / (10**18)  # Convertir Wei en ETH
    
    return df_whales


def get_top_wallets_by_profit(ETHERSCAN_API_KEY):
    """
    Trouver les 100 portefeuilles ayant réalisé les meilleurs bénéfices sur la dernière année.
    """
    # Définir une période d'analyse : dernière année
    one_year_ago = int((datetime.now() - timedelta(days=365)).timestamp())
    now = int(datetime.now().timestamp())
    
    # Utiliser des transactions pour estimer les bénéfices
    wallets_profit = []
    
    for wallet in get_top_wallets_addresses():
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey={ETHERSCAN_API_KEY}"
        response = requests.get(url).json()
        
        if response["status"] != "1":
            continue

        transactions = response["result"]
        
        # Filtrer les transactions de l'année passée
        filtered_transactions = [
            tx for tx in transactions
            if one_year_ago <= int(tx["timeStamp"]) <= now
        ]
        
        # Calculer les bénéfices
        profit = 0
        for tx in filtered_transactions:
            value = int(tx["value"]) / (10**18)  # Convertir Wei en ETH
            if tx["to"].lower() == wallet.lower():
                profit += value
            else:
                profit -= value
        
        wallets_profit.append({"wallet": wallet, "profit": profit})
    
    # Trier les portefeuilles par profit décroissant
    sorted_profits = sorted(wallets_profit, key=lambda x: x["profit"], reverse=True)
    top_100_profits = sorted_profits[:100]
    
    # Convertir en DataFrame
    df_profits = pd.DataFrame(top_100_profits)
    
    return df_profits




def get_top_whales(limit=100):
    """
    Scrape la Rich List d'Etherscan pour obtenir les plus gros portefeuilles.
    """
    url = "https://etherscan.io/accounts"

    # Configuration des options pour Selenium avec User-Agent
    options = Options()
    options.add_argument("--headless")  # Mode sans tête
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Lancer le navigateur avec Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Accéder à la page
    driver.get(url)
    
    # Attente explicite pour le tableau
    driver.implicitly_wait(10)
    
    # Récupérer le HTML de la page après le rendu complet de JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Localiser le tableau des portefeuilles
    table_div = soup.find("div", {"id": "ContentPlaceHolder1_divTable"})
    table = table_div.find("table", {"class": "table table-hover table-align-middle mb-0"})
    
    
    # Récupérer les lignes du tableau, en évitant l'en-tête
    rows = table.find_all("tr")[1:limit + 1]  # Limiter à 'limit' lignes
    
    wallets = []
    for row in rows:
        cols = row.find_all("td")
        
        # Extraction des informations pour chaque portefeuille
        rank = cols[0].text.strip()
        address = cols[1].find("a").text.strip()
        name_tag = cols[2].text.strip()
        balance = cols[3].text.strip()  # Le solde de crypto
        percentage = cols[4].text.strip()  # Le pourcentage du total
        txn_count = cols[5].text.strip()  # Nombre de transactions
        
        wallets.append({
            "rank": rank,
            "address": address,
            "name_tag": name_tag,
            "balance": balance,
            "percentage": percentage,
            "txn_count": txn_count
        })
    # Convertir les données dans un DataFrame
    df_whales = pd.DataFrame(wallets)
    # Fermer le navigateur Selenium après récupération des données
    driver.quit()
    embed()
    return df_whales








   