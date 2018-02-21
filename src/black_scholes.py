import numpy as np
import pandas as pd
from scipy.stats import norm


# First, all the helper functions
def d1d2(S, K, r, sigma, T):
    # Takes T in years
    d1 = (np.log(S / K) + ((r + ((sigma**2)/2))*T)) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    return d1, d2


def price_call(S, K, r, sigma, T):
    T /= 365  # Converts T from days to years
    d1, d2 = d1d2(S, K, r, sigma, T)
    c = (S * norm.cdf(d1)) - (K * np.exp(-1 * r * T) * norm.cdf(d2))
    return c


def price_put(S, K, r, sigma, T):
    T /= 365  # Converts T from days to years
    d1, d2 = d1d2(S, K, r, sigma, T)
    c = (K * np.exp(-1 * r * T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))
    return c


def option_vega(S, K, r, sigma, T):
    T /= 365  # Converts T from days to years
    d1, d2 = d1d2(S, K, r, sigma, T)
    v = S*np.sqrt(T)*norm.pdf(d1)/100 # IDK why I have to divide here
    return v


# Now the more serious functions
def bs_estimate(iv, frame, current_price, r=0.0188):
    df = frame.copy(deep=True)
    bs_price = np.zeros(df.shape)
    i = 0
    j = 0
    for rowval, row in df.iterrows():
        for colval, col in df.iteritems():
            if colval <= current_price:
                bs_price[i,j] = price_put(current_price, colval, r, iv[i, j], rowval)
            else:
                bs_price[i,j] = price_call(current_price, colval, r, iv[i, j], rowval)
            j += 1
        j = 0
        i += 1
    # Replace 0 with 1 penny to stop blowing up
    bs_price[bs_price <= 0.000001] = 0.01
    return bs_price


def vega_estimate(iv, frame, current_price, r=0.0188):
    df = frame.copy(deep=True)
    vega = np.zeros(df.shape)
    i = 0
    j = 0
    for rowval, row in df.iterrows():
        for colval, col in df.iteritems():
            vega[i,j] = option_vega(current_price, colval, r, iv[i, j], rowval)
            j += 1
        j = 0
        i += 1
    # Replace 0 with 0.1% to stop blowing up
    vega[vega <= 0.000001] = 0.001
    return vega
