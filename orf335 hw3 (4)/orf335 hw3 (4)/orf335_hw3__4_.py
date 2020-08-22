
S_0 = float(50)
n = int(3)
r = float(0)

#Define your payoff function 
def payoff(stock_price, strike):
    y = []
    for s in stock_price:
        x = s-strike
        y.append(x)

    j=0
    for i in y:  
        if i < 0:
            y[j] = 0
        else:
            y[j] = i
        j = j+1
    return y[-(n+1):]


r_n = r

u_n = 1.05
d_n = .95

p = ((1+r_n)-d_n)/(u_n-d_n) 

treeStock = []

for t in range(n+1):
    for i in range(t+1):
        treeStock.append(S_0*u_n**i*d_n**(t-i))

K = 50 #Strike Price
values = payoff(treeStock, K)
newestStep = values

while len(newestStep) != 1:
    binny = []
    for i in range(len(newestStep)-1):
        down = newestStep[i]
        up = newestStep[i+1]
        calc_v = (1/(1+r_n))*(p*up+(1-p)*down)
        binny.append(calc_v)
    values.append(binny)
    newestStep = binny

print(values)

