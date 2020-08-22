
import numpy as np
from scipy.stats import norm
import math

S_0 = 50
T = 0.25
r = 0.02
K = 50 #Strike Price
p_target = 2.75
n = 1000
threshold = 0.00000001

sigma_guess = 0.2

def payoff(stock_price, strike):
    y = []
    for s in stock_price:
        x = strike-s
        y.append(x)

    
    for i in range(len(y)):  
        y[i] = max(y[i],0)    
        
    return y

def americanPrice(S_0, n, T, r, sigma, K):
    deltaT = T/n 
    r_n = math.e**(r*deltaT)-1

    u_n = math.e**(sigma*math.sqrt(deltaT))
    d_n = 1/u_n
    p = ((1+r_n)-d_n)/(u_n-d_n) 

    treeStock = []

    for t in range(n+1):
        for i in range(t+1):
            treeStock.append(S_0*u_n**i*d_n**(t-i))

    payoffs = payoff(treeStock, K)


    newestStep = payoffs[-(n+1):]
    values = []
    values.append(newestStep)
    binary = []
    step = 1
    partition = n+1
    while (n+1-step) != 0:
        binny = []
        binary_temp = []

        partition = partition + (n+1-step)
        for i in range(n+1-step):
            down = newestStep[i]
            up = newestStep[i+1]
            calc_E = (1/(1+r_n))*(p*up+(1-p)*down)
            if calc_E > payoffs[-(partition-i)]:
                binny.append(calc_E)
                binary_temp.append(0)
            else:
                binny.append(payoffs[-(partition-i)])
                binary_temp.append(1)
        newestStep = binny
        values.insert(0,binny)
        binary.insert(0,binary_temp)
        step = step +1

    max_i = [None] * len(binary)
    for i in range(len(binary)):
        k = binary[i]
        for c in range(len(k)):
            if k[c] == 1:
                max_i[i] = c+1

    for i in range(len(max_i)):
        if max_i[i] == None:
            start = i+1 
    max_i = max_i[start:]

    stockMax = [None] * len(max_i)
    for k in range(len(max_i)):
        t = k + start
        i = max_i[k]
        stockMax[k] = S_0*u_n**i*d_n**(t-i)

    return values[0][0]

def europeanPrice(S_0, T, r, sigma, K):
    d1 = ((r+(sigma**2)/2)*T+np.log(S_0/K))/(sigma*math.sqrt(T))
    d2 = ((r-(sigma**2)/2)*T+np.log(S_0/K))/(sigma*math.sqrt(T))
    p_e = math.e**(-r*T)*K*(1-norm.cdf(d2))-S_0*(1-norm.cdf(d1))
    return p_e

# Hao Gong's precept  midpoint convergence method 

# step 2.1
p_guess = europeanPrice(S_0, T, r, sigma_guess, K)
if p_guess < p_target:
    sigma_low = sigma_guess
    p_low = p_guess
    k = 1
    p_high = p_guess # dummy intialization
    while p_high < p_target:
        sigma_high = 2**k*sigma_guess
        p_high = europeanPrice(S_0, T, r, sigma_high, K)
        k = k + 1 
else:
    sigma_high = sigma_guess
    p_high = p_guess
    k=1
    p_low = p_guess # dummy intialization
    while p_low > p_target:
        sigma_low = 2**(-k*sigma_guess)
        p_low = europeanPrice(S_0, T, r, sigma_low, K)
        k = k + 1 

while sigma_high-sigma_low > threshold: #if the interval length is too big
    sigma_mid = 0.5*(sigma_high+sigma_low)
    p_mid = europeanPrice(S_0, T, r, sigma_mid, K)
    if p_mid < p_target:
        sigma_low = sigma_mid
    else:
        sigma_high = sigma_mid
print("european")
print(0.5*(sigma_high+sigma_low))
print(europeanPrice(S_0, T, r, 0.5*(sigma_high+sigma_low), K))

#american version
p_guess = americanPrice(S_0, n, T, r, sigma_guess, K)
if p_guess < p_target:
    sigma_low = sigma_guess
    p_low = p_guess
    k = 1
    p_high = p_guess # dummy intialization
    while p_high < p_target:
        sigma_high = 2**k*sigma_guess
        p_high = americanPrice(S_0, n, T, r, sigma_high, K)
        k = k + 1 
else:
    sigma_high = sigma_guess
    p_high = p_guess
    k=1
    p_low = p_guess # dummy intialization
    while p_low > p_target:
        sigma_low = 2**(-k*sigma_guess)
        p_low = americanPrice(S_0, n, T, r, sigma_low, K)
        k = k + 1 
i = 0
while sigma_high-sigma_low > threshold: #if the interval length is too big
    i = i+1
    sigma_mid = 0.5*(sigma_high+sigma_low)
    p_mid = americanPrice(S_0, n, T, r, sigma_mid, K)
    if p_mid < p_target:
        sigma_low = sigma_mid
    else:
        sigma_high = sigma_mid

print("American")
print(0.5*(sigma_high+sigma_low))
print(americanPrice(S_0, n, T, r, 0.5*(sigma_high+sigma_low), K))
print(["iteration: ", str(i)])