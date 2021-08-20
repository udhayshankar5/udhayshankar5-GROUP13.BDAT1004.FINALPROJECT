import atexit
import os
import json
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, session
from pymongo import MongoClient
import urllib.request as urllib2 
import time

app = Flask(__name__)
@app.route('/')
# whenever the Home is clicked the database will refresh and adds new dataset in it.
def home():
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    response = urllib2.urlopen('http://data.fixer.io/api/latest?access_key=645d88662f2dfcc8b7b2df2d09f21c69')
    data = response.read()
    rdata = json.loads(data, parse_float=float)
    rate1 = dict(rdata["rates"])

    heading = ["currency","rates"]

    currency = []
    rates = []

    for key in rate1.keys():
        currency.append(key)
    for value in rate1.values():
        rates.append(value)
            
    upload_data = list(dict(zip(currency, rates)))
    upload_data = [{'currency': currency, 'rate': rates} for currency,rates in zip(currency,rates)]
    db.currency.drop()
    result = db.currency.insert_many(upload_data)
    return render_template('index.html')

@app.route('/Fitgap')
def ques():
    return render_template('Fitgap.html')     #questions contains the fitgap analysis

@app.route('/Top')
def google_bar_chart():
    data=barchart1()          # barchart1() function does the query and returns the data in list of dict format
    return render_template('Top.html',data=data)

@app.route('/Least')
def google_bar_chart1():
    data=barchart2()         # barchart1() function does the query and returns the data in list of dict format
    return render_template('Least.html',data=data)

@app.route('/CAD_chart')
def google_pie_chart():
    data=barchart3()         # barchart1() function does the query and returns the data in list of dict format
    return render_template('CAD_chart.html',data=data)

@app.route('/Rates/all')
def api_all():
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    pipeline = [
    { '$match'  : { 'rate' : {'$gte': 1000}}},
    { '$sort' : { 'rate' : +1 } },
    {'$project' : { '_id' : 0 } }
    ]

    c=[]
    r=[]
    data=list(client.Cyrpto.currency.aggregate(pipeline))
    for dt in data:
        for key in dt.keys():
            if(key=='currency'):
                c.append(dt[key])
            elif(key=='rate'):
                r.append(dt[key])
    combi=dict(zip(c, r))
    data={'Task':'All the rates'}
    data.update(combi)
    return jsonify(data)
# Whenever upload is running the new dataset will be loaded for every 24 hrs
@app.route('/upload')
def checking():
    upload()

def upload(): 
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    while True:
        response = urllib2.urlopen('http://data.fixer.io/api/latest?access_key=645d88662f2dfcc8b7b2df2d09f21c69')
        data = response.read()
        rdata = json.loads(data, parse_float=float)
        rate1 = dict(rdata["rates"])

        heading = ["currency","rates"]

        currency = []
        rates = []

        for key in rate1.keys():
            currency.append(key)
        for value in rate1.values():
            rates.append(value)
                
        upload_data = list(dict(zip(currency, rates)))
        upload_data = [{'currency': currency, 'rate': rates} for currency,rates in zip(currency,rates)]
        db.currency.drop()
        result = db.currency.insert_many(upload_data)
        print("Uploaded sucessfully")
        time.sleep(1440)
        
    
def barchart1():
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    pipeline = [
        { '$sort' : { 'rate' : -1 } },
        {'$limit':5}
    ]
    c=[]
    r=[]
    data=list(client.Cyrpto.currency.aggregate(pipeline))
    for dt in data:
        for key in dt.keys():
            if(key=='currency'):
                c.append(dt[key])
            elif(key=='rate'):
                r.append(dt[key])
    print(r)
    print(c)
    combi=dict(zip(c, r))
    data={'Task':'Top 5 Exchange Rates'}
    data.update(combi)
    return data

def barchart2():
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    pipeline = [
        { '$sort' : { 'rate' : +1 } },
        {'$limit':5}
    ]
    c=[]
    r=[]
    data=list(client.Cyrpto.currency.aggregate(pipeline))
    for dt in data:
        for key in dt.keys():
            if(key=='currency'):
                c.append(dt[key])
            elif(key=='rate'):
                r.append(dt[key])
    print(r)
    print(c)
    combi=dict(zip(c, r))
    data={'Task':'Least exhange rates'}
    data.update(combi)
    return data

def barchart3():
    dbConnectionString = 'mongodb+srv://Mohan:sfgZWA2oPsCf6NI5@cluster0.ejo1e.mongodb.net/Cyrpto?retryWrites=true&w=majority'
    client = MongoClient(dbConnectionString)
    db = client.get_database('Cyrpto')
    records = db.currency
    pipeline = [
        { '$match' : { 'rate' : {'$lt': 1.478445}}},
         { '$sort' : { 'rate' : +1 } }
    ]
    c=[]
    r=[]
    data=list(client.Cyrpto.currency.aggregate(pipeline))
    for dt in data:
        for key in dt.keys():
            if(key=='currency'):
                c.append(dt[key])
            elif(key=='rate'):
                r.append(dt[key])
    print(r)
    print(c)
    combi=dict(zip(c, r))
    data={'Task':'Exchange rates less than CAD'}
    data.update(combi)
    return data

if __name__ == "__main__":
    app.run()