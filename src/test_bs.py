import unittest
import black_scholes

class TestOptionsCalcs(unittest.TestCase):
    
    # Tested against http://www.option-price.com/
    def test_default_options(self):
        S = 100
        K = 100
        T = 30
        r = 0.05
        sigma = 0.25
        call_price = black_scholes.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 3.0626021306 < 0.00001)
        put_price = black_scholes.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 2.652486507 < 0.00001)
        vega = black_scholes.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.1138778071 < 0.00001)

    def test_low_strike(self):
        S = 100
        K = 80
        T = 30
        r = 0.05
        sigma = 0.25
        call_price = black_scholes.price_call(S, K, r, sigma, T)
        self.assertTrue(call_price - 20.3294113527 < 0.00001)
        put_price = black_scholes.price_put(S, K, r, sigma, T)
        self.assertTrue(put_price - 0.0013188538 < 0.00001)
        vega = black_scholes.option_vega(S, K, r, sigma, T)
        self.assertTrue(vega - 0.0006693263 < 0.00001)

    # Add high strike, low vol, high vol, short time, high time tests


if __name__ == '__main__':
    unittest.main()
