from pprint import pprint
import requests

def get_address_info_v4(address):
    address = "dydx1ghxuwdf4dean5eccrsgw9f94rhc2kpvx4cyg3u"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(f'https://indexer.v4testnet.dydx.exchange/v4/addresses/{address}', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des informations de l'adresse: {e}")
        return None

# Utilisez cette fonction en remplacement de certaines fonctionnalités de dydx3
address_info = get_address_info_v4("votre_adresse_ici")
pprint(address_info)
