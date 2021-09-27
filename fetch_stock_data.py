# Inbuilt python module yfinance is used to fetch stock data from Yahoo Finance website.
# Processes the fetched data and gives it to ML model

# Importing required modules
import pandas as pd
import numpy as np
import yfinance as yf
import datetime

class FetchData():
    # Function   :- initializes DataFrame
    def __init__(self):
        self.__df = pd.DataFrame()

    # Function   :- fetches data using yfinance
    #
    # Parameters :- stock_name - name of the stock 
    #               start_date/end_date - timeframe for which we want to fetch data
    #
    # Returns    :- DataFrame containing stock data
    def __getdata(self, stock_name, start_date, end_date):
        t = yf.download(stock_name, start_date, end_date)
        return t

    # Function   :- adds features to data
    #
    # Parameters :- isTrain - True if fetching train data for ML model
    #                         False if fetching data for backtesting
    def __addfeatures(self, isTrain):
        # adding target to train data for training ML model 
        if isTrain:
            self.__df['Open_next'] = self.__df['Open'].shift(-1)
            self.__df['target'] = np.where(self.__df['Open_next'] > self.__df['Close'], 1, 0)

        # adding technical indicators in data
        self.__df['SMA30'] = self.__df['Adj Close'].rolling(window=30).mean()
        self.__df['SMA60'] = self.__df['Adj Close'].rolling(window=60).mean()
        self.__df['SMA90'] = self.__df['Adj Close'].rolling(window=90).mean()
        self.__df['SMA180'] = self.__df['Adj Close'].rolling(window=180).mean()
        
        # droping NULL values in DataFrame
        self.__df.dropna(inplace = True)

    # Function   :- called from train and pred to fetch data
    #
    # Parameters :- stock_name - name of the stock 
    #               start_date/end_date - timeframe for which we want to fetch data
    #               isTrain - True if fetching train data for ML model
    #                         False if fetching data for backtesting
    #
    # Returns    :- DataFrame containing stock data
    def execute(self, stock_name = "AAPL", start_date = datetime.date(2017, 1, 1), end_date = datetime.date(2018, 1, 1), isTrain = False):
        self.__df = self.__getdata(stock_name, start_date, end_date)
        self.__addfeatures(isTrain)
        return self.__df