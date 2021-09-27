# Takes output predicted by ML model 
# Outputs how much profit user would have made if he/she would have used model to trade

# Importing required modules
import pandas as pd
from pred import *
import matplotlib.pyplot as plt


# Function   :- fetches output predicted by ML model
# Returns    :- DataFrame containing output predicted by model
def get_pred(symbol,syear,eyear):
    return calls(symbol,syear,eyear)

# Function   :- calculates and finds how much profit or loss would have happened if user invested according ML model
# Parameters :- t - DataFrame containing output of ML model
def simulator(t,amount):
    # m - amount which user want to invest
    # c - count of stock
    m = amount
    dm=amount
    c = 0
    print(f'Default Money = {m}')
    print("\n")
    # calculating profit or loss according output predicted by ML model
    for i in range(len(t)):
        if (t['pred'][i] > 0):
            if m > t['Close'][i]:
                m = m - t['Close'][i]
                c = c + 1

        else:
            if c > 0:
                m = m + t['Close'][i]
                c = c - 1
    profit=c*t["Open"][-1] + m
    print(f'Money = {m}')
    print(f'Stock = {c}')
    print(f'Profit = {c*t["Open"][-1] + m}')
    return m,c,profit,dm

# Function   :- fetches output predicted by ML model and give it to simulator()
def sexecute(symbol,syear,eyear,amount):
    df = get_pred(symbol,syear,eyear)
    m,c,profit,dm= simulator(df,amount)
    return m,c,profit,dm
