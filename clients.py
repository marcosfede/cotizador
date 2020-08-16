import requests
from cryptomarket.exchange.client import Client
from config import CMKT_API_KEY, CMKT_SECRET


class CMKTClient:
    def __init__(self):
        self.client = Client(CMKT_API_KEY,CMKT_SECRET)

    def get_price(self):
        response = self.client.get_ticker("BTCARS")
        data = response['data'][0]
        sell_price = float(data['ask'])
        return sell_price


class SatoshiClient:
    def __init__(self):
        client = requests.Session()
