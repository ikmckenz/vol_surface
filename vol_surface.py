import pandas as pd
import requests
import json

def yahoo_opt_clean(x, type):
    x = pd.io.json.json_normalize(x['optionChain']['result'][0]['options'][0][type])
    x = x[['ask', 'bid', 'expiration', 'strike']]
    if type == 'calls':
        x['type'] = 'C'
    elif type == 'puts':
        x['type'] = 'P'
    else:
        raise ValueError('Unknown option type')
    return x


def vol_surface():
    url = 'https://query2.finance.yahoo.com/v7/finance/options/SPY'
    content = requests.get(url).text
    content = json.loads(content)
    current_price = content['optionChain']['result'][0]['quote']['regularMarketPrice']
    current_date = content['optionChain']['result'][0]['quote']['regularMarketTime']
    dates = content['optionChain']['result'][0]['expirationDates']
    options = yahoo_opt_clean(content, 'calls')
    df = yahoo_opt_clean(content, 'puts')
    options = options.append(df, ignore_index=True)
    for i in range(1, 10):
        content = requests.get(url + '?date=' + str(dates[i])).text
        content = json.loads(content)
        df = yahoo_opt_clean(content, 'calls')
        options = options.append(df, ignore_index=True)
        df = yahoo_opt_clean(content, 'puts')
        options = options.append(df, ignore_index=True)
    # Middle = ask - bid
    # Calculate implied vol, damn.

vol_surface()


