
import os
import requests

def currencyConverter(self, amount, fromCurrency, toCurrency):
    url = os.environ['FIXER_URL'] + '?access_key=' + os.environ['FIXER_API_KEY'] 
    url += "&from=" + fromCurrency + "&to=" + toCurrency + "&amount=" + amount
    response = requests.get(url)
    print(response)
    return response.json()
