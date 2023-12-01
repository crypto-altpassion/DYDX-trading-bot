import requests
import time
import numpy as np

def get_candles_v4(market, resolution='1MIN', limit=100):
    # Définition de l'URL de base et des headers pour la requête
    base_url = 'https://indexer.v4testnet.dydx.exchange/v4/candles/perpetualMarkets/{}'
    headers = {'Accept': 'application/json'}

    # Protection de l'API
    time.sleep(1)

    # Construction de l'URL avec les paramètres
    url = base_url.format(market)
    params = {'resolution': resolution, 'limit': limit}

    # Requête GET
    response = requests.get(url, params=params, headers=headers)

    # Vérification de la réponse
    if response.status_code != 200:
        raise Exception("Erreur API: Réponse HTTP ", response.status_code)

    # Extraction des données
    data = response.json()
    close_prices = [float(candle['close']) for candle in data['candles']]

    # Retourne les prix de fermeture
    close_prices.reverse()
    return np.array(close_prices)

# Exemple d'utilisation
market = "BTC-USD"  # Remplacez par le marché désiré
close_prices = get_candles_v4(market)
print(close_prices)
