from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETHEREUM_ADDRERSS,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER,
    ETH_PRIVATE_KEY,
)
'''
import time
import requests

# Get server time
def get_server_time(api_url):
    response = requests.get(api_url)
    return response.json()['serverTime']

api_url = "https://eth-goerli.g.alchemy.com/v2/n8FkOvVL4TNqL8en2nPZxS2NMayMejIY"#config('HTTP_PROVIDER')  # Remplacez ceci par l'URL réelle
server_time = get_server_time(api_url)
local_time = time.time()

time_difference = server_time - local_time

def get_adjusted_time():
    return time.time() + time_difference
'''
# Connect to DYDX
def connect_dydx():

    # Create Client Connection
    client = Client(
        host=HOST,
        api_key_credentials={
            "key": DYDX_API_KEY,
            "secret": DYDX_API_SECRET,
            "passphrase": DYDX_API_PASSPHRASE,
        },
        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=ETH_PRIVATE_KEY,
        default_ethereum_address=ETHEREUM_ADDRERSS,
        web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    )

    # Confirm client
    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    quote_balance = account.data["account"]["quoteBalance"]
    print("Connection Successful")
    print("Account ID: ", account_id)
    print("Quote Balance: ", quote_balance)

    # Return Client
    return client
