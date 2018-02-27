import numpy as np
import pandas as pd
import unittest
import src.black_scholes as bs
from src.iv_calc import calc_iv

class TestOptionsCalcs(unittest.TestCase):
    
    # Tested against http://www.option-price.com/
    def test_default_options(self):
        S = 100
        K = 100
        T = 30
        r = 0.05
        sigma = 0.25
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 3.0626021306 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 2.652486507 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.1138778071 < 0.00001)

    def test_low_strike(self):
        S = 100
        K = 80
        T = 30
        r = 0.05
        sigma = 0.25
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 20.3294113527 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 0.0013188538 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.0006693263 < 0.00001)

    def test_high_strike(self):
        S = 100
        K = 121
        T = 30
        r = 0.05
        sigma = 0.25
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 0.0114269163 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 20.5151870118 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.0042470161 < 0.00001)

    def test_low_vol(self):
        S = 100
        K = 100
        T = 30
        r = 0.05
        sigma = 0.05
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 0.7990391624 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 0.3889235388 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.1138778071 < 0.00001)

    def test_high_vol(self):
        S = 100
        K = 100
        T = 30
        r = 0.05
        sigma = 0.95
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 11.0160397281 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 10.6059241046 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.1130721223 < 0.00001)

    def test_high_time(self):
        S = 100
        K = 100
        T = 600
        r = 0.05
        sigma = 0.25
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 16.5718871058 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 8.6814164401 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.4689601647 < 0.00001)

    def test_low_time(self):
        S = 100
        K = 100
        T = 5
        r = 0.05
        sigma = 0.25
        call_price = bs.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 1.2014338506 < 0.00001)
        put_price = bs.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 1.1329641511 < 0.00001)
        vega = bs.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.0466588942 < 0.00001)


class TestVolSurface(unittest.TestCase):

    def test_vol_surface(self):
        # First, create a dataframe of option prices
        options = pd.DataFrame(np.zeros((5,5)),
                               columns=[90, 95, 100, 105, 110],
                               index=[5, 30, 60, 90, 200])
        
        r = 0.05
        sigma = 0.25
        current_price = 99
        iv = np.full(options.shape, sigma)
        my_prices = bs.bs_estimate(iv, options, current_price, r)
        # From http://www.option-price.com
        real_prices = np.array([[0.0003776097, 0.0966921635, 0.7542385399, 0.0261784483, 0.0001306334],
                                [0.2545493901, 1.1085012585, 2.5533592318, 0.9338706699, 0.2660176248],
                                [0.761418395, 1.9716164601, 3.9151604326, 2.036228008, 0.9486972331],
                                [1.240451066, 2.6269037172, 5.0077479445, 3.0072764828, 1.6886487282],
                                [2.613315363, 4.2510351116, 8.1186981076, 5.9403630979, 4.2426525761]])
        res = my_prices - real_prices
        self.assertTrue(max(-1*res.min(), res.max()) < 0.0001)

        # Then, try and reverse engineer the vol
        options = pd.DataFrame(my_prices, columns=options.columns, index=options.index)
        iv = calc_iv(options, current_price, r)
        res = iv - sigma
        self.assertTrue(max(-1*res.min(), res.max()) < 0.00001)


if __name__ == '__main__':
    unittest.main()

