
S_0 = 30
n = 1000
T = 1
r = 0.035
sigma = 0.20
#B = 15 #Barrier Price

#Define your payoff function 
def payoff(stock_price, barrier):
    y = [None]*len(stock_price)
    for i in range(len(stock_price)): # fills in 0 for only barrier trips
        if stock_price[i] < barrier:
            y[i] = 0 
    for k in range(1, n+2): # fills the last branch with 1 if empty
        if y[-k] == None:
            y[-k] = 1
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

for s in range(11):
    B = s*2+10
    payoffs = payoff(treeStock, B)

    newestStep = payoffs[-(n+1):]
    values = []
    values.append(newestStep)
    partition = n+1
    step = 1
    while (n+1-step) != 0:
        binny = []
        partition = partition + (n+1-step)
        for i in range(n+1-step):
            if payoffs[-(partition-i)] == None:
                down = newestStep[i]
                up = newestStep[i+1]
                calc_E = (1/(1+r_n))*(p*up+(1-p)*down)
                binny.append(calc_E)
            else:
                binny.append(0)
        newestStep = binny
        values.insert(0,binny)


        step = step +1
    #print(B)
    #print(round(values[0][0], 2))
    print(-math.log(values[0][0]))

B = 15
payoffs = payoff(treeStock, B)

newestStep = payoffs[-(n+1):]
values = []
values.append(newestStep)
partition = n+1
step = 1
while (n+1-step) != 0:
    binny = []
    partition = partition + (n+1-step)
    for i in range(n+1-step):
        if payoffs[-(partition-i)] == None:
            down = newestStep[i]
            up = newestStep[i+1]
            calc_E = (1/(1+r_n))*(p*up+(1-p)*down)
            binny.append(calc_E)
        else:
            binny.append(0)
    newestStep = binny
    values.insert(0,binny)


    step = step +1
print("B=15")
print("Value")
print(round(values[0][0], 2))
print("RB")
print(-math.log(values[0][0]))