S_0 = 30
n = 1000
T = 1
r = 0.035
sigma = 0.20
K = 30 #Strike Price

# hw6 testing
#S_0 = 50
#T = 0.25
#r = 0.02
#K = 50 #Strike Price
#p_target = 2.75
#n = 1000
#sigma = 0.24999999701976777

#Define your payoff function 
def payoff(stock_price, strike):
    y = []
    for s in stock_price:
        x = strike-s
        y.append(x)

    
    for i in range(len(y)):  
        y[i] = max(y[i],0)    
        
    return y
    

deltaT = T/n 
import math
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
#martingale = []
while (n+1-step) != 0:
    binny = []
    binary_temp = []
    #martingale_temp = []

    partition = partition + (n+1-step)
    #print('new')
    for i in range(n+1-step):
        down = newestStep[i]
        up = newestStep[i+1]
        calc_E = (1/(1+r_n))*(p*up+(1-p)*down)
        #martingale_temp.append(calc_E)
        #print(partition-i) 
        if calc_E > payoffs[-(partition-i)]:
            binny.append(calc_E)
            binary_temp.append(0)
        else:
            binny.append(payoffs[-(partition-i)])
            binary_temp.append(1)
    newestStep = binny
    values.insert(0,binny)
    binary.insert(0,binary_temp)
    #martingale.insert(0,martingale_temp)
    step = step +1

#print(binary)
max_i = [None] * len(binary)
for i in range(len(binary)):
    k = binary[i]
    for c in range(len(k)):
        if k[c] == 1:
            max_i[i] = c+1

#last value of None
for i in range(len(max_i)):
    if max_i[i] == None:
        start = i+1 #you want to print after it
max_i = max_i[start:]

stockMax = [None] * len(max_i)
for k in range(len(max_i)):
    t = k + start
    i = max_i[k]
    stockMax[k] = S_0*u_n**i*d_n**(t-i)

#print(start)
print(round(values[0][0], 2))
#print(stockMax)

