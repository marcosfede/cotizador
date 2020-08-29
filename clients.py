import requests
from cachecontrol import CacheControl
import calendar
from cachecontrol.heuristics import BaseHeuristic
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate
import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode

# from cryptomarket.exchange.client import Client
from config import CMKT_API_KEY, CMKT_SECRET, PAXFUL_API_KEY, PAXFUL_SECRET


class TimeoutHeuristic(BaseHeuristic):
    def __init__(self, timeout):
        self.timeout = timeout

    def update_headers(self, response):
        expires = datetime.now() + timedelta(minutes=self.timeout)
        return {
            'expires' : formatdate(calendar.timegm(expires.timetuple())),
            'cache-control' : 'public',
        }

    def warning(self, response):
        msg = 'Automatically cached! Response is Stale.'
        return '110 - "%s"' % msg


class CMKTClient:
    def __init__(self, cache=True):
        self.client = requests.session()
        if cache:
            self.client = CacheControl(self.client, heuristic=TimeoutHeuristic(5))

    def get_price(self):
        response = self.client.get("https://criptoya.com/api/cryptomkt/btc/ars/1")
        sell_price = response.json()['ask']
        return sell_price


class SatoshiClient:
    def __init__(self, cache=True):
        self.client = requests.session()
        if cache:
            self.client = CacheControl(self.client, heuristic=TimeoutHeuristic(5))

    def get_price(self):
        response = self.client.get("https://criptoya.com/api/satoshitango/btc/ars/1")
        sell_price = response.json()['ask']
        return sell_price


class PaxfulClient:

    def __init__(self, cache=True):
        self.client = requests.session()
        if cache:
            self.client = CacheControl(self.client, heuristic=TimeoutHeuristic(5))

        self.client.headers.update({
            "Accept": "application/json",
            "Content-Type": "text/plain"
        })

    def get_price(self):
        # nonce = int(time.time())
        # payload = {"apikey": PAXFUL_API_KEY, "nonce": nonce}
        # payload = urlencode(sorted(payload.items()))
        # apiseal = hmac.new(PAXFUL_API_SECRET.encode(), payload.encode(), sha256).hexdigest()
        # data_with_apiseal = payload + "&apiseal=" + apiseal
        payload = {'offer_type': 'buy', 'payment_method': 'payoneer', 'currency_code': 'usd', 'fiat_min': 100}
        resp = self.client.post("https://paxful.com/api/offer/all", data=payload).json()
        results = resp['data']['offers']
        top = sorted(results, key=lambda x: x['fiat_price_per_crypto'])
        btc_price = top[0]['fiat_price_per_crypto']

        return btc_price
