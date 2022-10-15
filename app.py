from flask import Flask, render_template
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import api_key as ak


app = Flask(__name__)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '10',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': ak.api_key,
}

session = Session()
session.headers.update(headers)

currency_name = []
currency_price = []

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    for i in range(0, 10):
        crypto_name = data['data'][i]['name']
        currency_name.append(crypto_name)
        crypto_price = round(data['data'][i]['quote']['USD']['price'], 4)
        currency_price.append(crypto_price)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

crypto_dict = dict(zip(currency_name, currency_price))
print(crypto_dict)


@app.route('/')
def index():
    return render_template('index.html', crypto_dict=crypto_dict)


if __name__ == '__main__':
    app.run()
