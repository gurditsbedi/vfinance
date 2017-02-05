
import requests
from bs4 import BeautifulSoup

# An API to extract current stock price from the in.finance.yahoo.com
# :param symbol The symbol of the stock
# :return details A dictionary with symbol, name, price of the stock

def lookup(symbol, country='USA'):
    symbol = str(symbol).upper()
    # To keep data of the stock
    details = {}
    details['exists'] = False
    details['symbol'] = symbol
    details['name'] = None
    details['price'] = 0

    # accessing the required page
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 '
                             'Chrome/55.0.2883.87 Safari/537.36'}
    try:
        r = requests.get('http://download.finance.yahoo.com/d/quotes.csv',
                         params={'s': symbol, 'f': 'sl1n', 'e': '.csv'},
                         headers=headers)
    except:
        return details

    data = r.content.decode('utf-8')
    theta = data.replace('\n', '').split(',')
    # if such a stock exists
    if theta[1] != 'N/A':
        details['exists'] = True
        details['symbol'] = symbol
        details['price'] = float(theta[1])
        details['name'] = (''.join(theta[2:]))[1:-1]

    # print(details)
    return details


