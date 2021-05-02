
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def getRatesFromBaseCurrency(baseCurrency):
    url = os.environ.get('FIXER_URL') + '?access_key=' + os.environ.get('FIXER_API_KEY')
    url += "&base=" + baseCurrency
    response = requests.get(url)
    return response.json()


def currencyConverter(amount, fromCurrency, toCurrency):
    url = os.environ.get('FIXER_URL') + '?access_key=' + os.environ.get('FIXER_API_KEY')
    url += "&from=" + fromCurrency + "&to=" + toCurrency + "&amount=" + str(amount)
    response = requests.get(url)
    return response.json()
