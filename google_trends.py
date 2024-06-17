from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

def get_GT_data():
    # Initialiser l'objet TrendReq avec le fuseau horaire de Zurich (GMT+1)
    pytrends = TrendReq(hl='en-US', tz=60)  # GMT+1 correspond à 60 minutes

    # Définir la liste des mots-clés et construire la charge utile
    kw_list = ["bitcoin"]
    pytrends.build_payload(kw_list, timeframe='today 5-y')

    # Récupérer les données d'intérêt au fil du temps
    data = pytrends.interest_over_time()

    # Vérifier si les données ont été correctement récupérées
    if not data.empty:
        # Supprimer la colonne isPartial si elle existe
        if 'isPartial' in data.columns:
            data = data.drop(columns=['isPartial'])

        # Visualiser les données
        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['bitcoin'], label='Bitcoin', color='blue')
        plt.title('Tendances de recherche de "bitcoin" au fil du temps')
        plt.xlabel('Date')
        plt.ylabel('Intérêt de recherche')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()
    else:
        print("Les données n'ont pas été récupérées correctement.")

    return data
