import numpy as np
from src.black_scholes import bs_estimate, vega_estimate

def calc_iv(options, current_price):
    # Start with a huge vol estimate to stop small values from going NaN
    iv = np.full(options.shape, 3.0)
    bs_price = bs_estimate(iv, options, current_price)
    res = bs_price - options.values
    vega = vega_estimate(iv, options, current_price)
    
    counter = 0
    while max(-1*res.min(), res.max()) > 0.00000001:
        iv = iv - (res/vega)/500
        # Divide by 500 as a cheap hack to stop Newton's method from exploding
        # Should probably switch to bisection or secant or similar
        bs_price = bs_estimate(iv, options, current_price)
        res = bs_price - options.values
        vega = vega_estimate(iv, options, current_price)
        counter += 1
        if counter > 5000:
            break

    # Should probably log the number of iterations here
    print("Took %d iterations" % counter)
    print("Max price residual is %d" %  max(-1*res.min(), res.max()))
    return iv
