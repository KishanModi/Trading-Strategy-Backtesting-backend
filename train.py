# Takes train data and give it to model_knn to train ML model and saves trained ML model

# Importing required modules
import pickle
import pandas as pd
import json
import datetime
#from app import symbol,s_year,e_year,amount
from model_knn import Model
from fetch_stock_data import FetchData

# file path to save trained ML model 
MODEL_PATH = 'model.pkl'

# Function   :- takes train data from FetchData class 
# Returns    :- DataFrame containing train data
def get_train_data(symbol):
    #stock_name = input("Enter Stock Name :---  ")
    stock_name = symbol
    start_date = datetime.date(2001, 1, 1)
    end_date = datetime.date(2015, 1, 1)
    train = FetchData().execute(stock_name, start_date, end_date, True)

    return train

# Function   :- saves trained ML model 
# Parameters :- model - trained ML model
#               model_path = file path to save trained model
def saveModel(model, model_path=MODEL_PATH):
    with open(MODEL_PATH, 'wb') as f:
        model = pickle.dump(model, f)
        return model

# Function   :- takes data from get_train_data function and calls train function to train Ml model
# Parameters :- model - object of Model class
# Returns    :- trained ML model
def texecute(model,symbol):
    # TODO get training data
    train = get_train_data(symbol)

    # deviding features and target into X and y
    X = train.drop(['target', 'Open_next', 'Volume'], axis=1)
    y = train.target

    # TODO train model
    model.train(X, y)
    return model
