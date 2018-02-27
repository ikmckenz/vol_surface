import pandas as pd
import requests
import json

def yahoo_opt_clean(x, type):
    x = pd.io.json.json_normalize(x['optionChain']['result'][0]['options'][0][type])
    x = x[['lastPrice', 'expiration', 'strike', 'inTheMoney']]
    if type == 'calls':
        x['type'] = 'C'
    elif type == 'puts':
        x['type'] = 'P'
    else:
        raise ValueError('Unknown option type')
    return x


def get_options():
    url = 'https://query2.finance.yahoo.com/v7/finance/options/SPY'
    content = requests.get(url).text
    content = json.loads(content)
    current_price = content['optionChain']['result'][0]['quote']['regularMarketPrice']
    current_date = content['optionChain']['result'][0]['quote']['regularMarketTime']
    dates = content['optionChain']['result'][0]['expirationDates']
    options = yahoo_opt_clean(content, 'calls')
    df = yahoo_opt_clean(content, 'puts')
    options = options.append(df, ignore_index=True)
    for i in range(1, len(dates)):
        content = requests.get(url + '?date=' + str(dates[i])).text
        content = json.loads(content)
        num_strikes = len(content['optionChain']['result'][0]['strikes'])
        if num_strikes > 1:
            df = yahoo_opt_clean(content, 'calls')
            options = options.append(df, ignore_index=True)
            df = yahoo_opt_clean(content, 'puts')
            options = options.append(df, ignore_index=True)
        else:
            break
    return options, current_price, current_date

if __name__ == '__main__':
    options, current_price, date = get_options()
    pathname = 'saved_data/options_' + str(date) + '.csv'
    options.to_csv(pathname, index=False)
