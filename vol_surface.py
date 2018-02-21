import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import datetime as dt
from src.yahoo_options import get_options
from src.black_scholes import bs_estimate, vega_estimate


# First, grab the options data and save it
options, current_price, date = get_options()
pathname = 'saved_data/options_' + str(date) + '.csv'
options.to_csv(pathname, index=False)

# Then, let's do some data chopping
options.drop(options[options.inTheMoney == True].index, inplace=True)

options.drop(['inTheMoney'], axis=1, inplace=True)
options.reset_index(drop=True, inplace=True)
# Also, let's save the date the data was collected
date = dt.datetime.fromtimestamp(int(date))
# and also keep a rounded current price
round_price = round(current_price/5)*5

# Pivot
options = options.pivot(index='expiration', columns='strike', values='lastPrice')

# Drop low and high columns
options = options[[c for c in options.columns if c <= (round_price + 50)]]
options = options[[c for c in options.columns if c >= (round_price - 50)]]

# Drop columns which aren't divisible by 5
options = options[[c for c in options.columns if c % 5 == 0]]
# Drop rows with many nans
options.dropna(axis=0, thresh=options.shape[1] - 3, inplace=True)
# Drop columns with any nans
options.dropna(axis=1, how='any', inplace=True)
# Convert the index to number of days from today
options.index = pd.to_datetime(options.index, unit='s')
options.index = (options.index - date).days
# Drop days farther than one year
options = options[options.index < 366]

# Now, for the real calculations and things
# Start with a huge vol estimate to stop small values from going NaN
iv = np.full(options.shape, 3.0)
bs_price = bs_estimate(iv, options, current_price)
res = bs_price - options.values
vega = vega_estimate(iv, options, current_price)

counter = 0
while max(-1*res.min(), res.max()) > 0.001:
    iv = iv - (res/vega)/200
    # Divide by 500 as a cheap hack to stop Newton's method from exploding
    # Should probably switch to bisection or secant or similar
    bs_price = bs_estimate(iv, options, current_price)
    res = bs_price - options.values
    vega = vega_estimate(iv, options, current_price)
    counter += 1
    if counter > 500:
        break
# Should probably log the number of iterations here
print("Took %d iterations" % counter)
print("Max price residual is %d" % res.max())

# Now, let's create the nice plot
X = list(options)
Y = options.index.values
X, Y = np.meshgrid(X, Y)
fig = plt.figure(figsize=(10,8))
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, iv, cmap=cm.coolwarm)
ax.xaxis.set_label_text('Strike')
ax.yaxis.set_label_text('Days until expiry')
date = dt.datetime.strftime(date, "%Y-%m-%d")
title_text = 'Implied volatility on %s' % date
ax.set_title(title_text)
plt.savefig('pictures/iv_%s' % date, bbox_inches='tight')
