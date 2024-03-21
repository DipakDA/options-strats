import math
import scipy
from scipy.stats import norm

# Source Addition pending
def BlackScholes(S,K,t,sigma,r=10,q=0.0,td=365):

    S,K,sigma,r,q,t = float(S),float(K),float(sigma/100),float(r/100),float(q/100),float(t/td)

    d1 = (math.log(S/K)+(r-q+0.5*sigma**2)*t)/(sigma*math.sqrt(t))

    Nd1 = (math.exp((-d1**2)/2))/math.sqrt(2*math.pi)
    d2 = d1-sigma*math.sqrt(t)
    Nd2 = norm.cdf(d2)
    call_theta =(-((S*sigma*math.exp(-q*t))/(2*math.sqrt(t))*(1/(math.sqrt(2*math.pi)))*math.exp(-(d1*d1)/2))-(r*K*math.exp(-r*t)*norm.cdf(d2))+(q*math.exp(-q*t)*S*norm.cdf(d1)))/td
    put_theta =(-((S*sigma*math.exp(-q*t))/(2*math.sqrt(t))*(1/(math.sqrt(2*math.pi)))*math.exp(-(d1*d1)/2))+(r*K*math.exp(-r*t)*norm.cdf(-d2))-(q*math.exp(-q*t)*S*norm.cdf(-d1)))/td
    call_premium =math.exp(-q*t)*S*norm.cdf(d1)-K*math.exp(-r*t)*norm.cdf(d1-sigma*math.sqrt(t))
    put_premium =K*math.exp(-r*t)*norm.cdf(-d2)-math.exp(-q*t)*S*norm.cdf(-d1)
    call_delta =math.exp(-q*t)*norm.cdf(d1)
    put_delta =math.exp(-q*t)*(norm.cdf(d1)-1)
    gamma =(math.exp(-r*t)/(S*sigma*math.sqrt(t)))*(1/(math.sqrt(2*math.pi)))*math.exp(-(d1*d1)/2)
    vega = ((1/100)*S*math.exp(-r*t)*math.sqrt(t))*(1/(math.sqrt(2*math.pi))*math.exp(-(d1*d1)/2))
    call_rho =(1/100)*K*t*math.exp(-r*t)*norm.cdf(d2)
    put_rho =(-1/100)*K*t*math.exp(-r*t)*norm.cdf(-d2)
    
    return {'Call Premium': call_premium, 
            'Put Premium':put_premium,
            'Call Theta':call_theta,
            'Put Theta':put_theta,
            'Call Delta':call_delta,
            'Put Delta':put_delta,
            'Gamma':gamma,
            'Vega':vega,
            'Call Rho':call_rho,
            'Put Rho':put_rho}


def getIV(c_p, S, K, t, market_price, MAX_TRY=1000,sigma=50):
    for i in range(MAX_TRY):
        bs = BlackScholes(S, K, t, sigma)
        if c_p == 'CE': bs_price = bs['Call Premium']
        elif c_p == 'PE': bs_price = bs['Put Premium']
        else: 
            print('Incorrect Option Type')
            return None
        diff = market_price - bs_price
        #print('DIFF: ', diff)
        vega = bs['Vega']
        #print('VEGA: ', vega)
        if abs(diff) < 1.5: return sigma
        sigma += diff/vega
        #print('SIGMA: ', sigma)
    return sigma