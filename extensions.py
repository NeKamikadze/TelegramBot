import requests
import json
from config import keys


class APIException(Exception):
    pass


class CashConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести одну и ту же валюту "{base}"!')

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту "{base}"!')

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту "{quote}"!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Невозможно обработать количество "{amount}"!')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}'

        headers = {'apikey': 'd9B1ahHEuhgcBNlWmHtZ95dMCoqpYFjN'}
        r = requests.get(url, headers=headers)
        result = json.loads(r.content)['result']

        return round(result, 2)
