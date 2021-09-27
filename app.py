from flask import Flask, render_template, url_for
from flask.globals import request
from subprocess import Popen
from train import *
from simulator import *
import time, os
import matplotlib.pyplot as plt
app = Flask(__name__)
symbol= "MSFT"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getdata', methods=["GET","POST"])
def getdata():
    global symbol
    if request.method == "GET":
        return render_template('dashboard.html')

    if request.method == "POST":
        name =request.form.get("symbol")
        s_year=int(request.form.get("syear"))
        e_year=int(request.form.get('eyear'))
        amount=int(request.form.get("amount"))

        from data import data
        def get_keys_from_value(data, name):
            return [symbol for symbol, v in data.items() if v == name]

        symbol = get_keys_from_value(data, name)
        print(symbol)

        model = Model()
        model = texecute(model, symbol)
        saveModel(model)
        time.sleep(2)

        m,c,profit,dm = sexecute(symbol,s_year,e_year,amount)
        profit=profit-dm

        data = {}
        data["wallet"]=m
        data["Stocks"]=c
        data["profit"]=profit
        data["money"]=dm
        keys = list(data.keys())
        values = list(data.values())

        plt.bar(keys, values, color ='maroon',
        width = 0.4)

        plt.xlabel("Investment Chart")
        plt.ylabel("Amount")
        plt.title("Profit Loss")
        new_graph_name = "graph" + str(time.time()) + ".png"
        for filename in os.listdir('static/'):
            if filename.startswith('graph_'):  # not to remove other images
                os.remove('static/' + filename)

        plt.savefig('static/' + new_graph_name)
        return render_template('dashboard.html', m=m, c=c, profit=profit,dm=dm,graph=new_graph_name)


if __name__ == "__main__":
    app.run()