from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from cs50 import SQL
import os
import gdown

ruta_archivo_local = 'WDI.db'

if not os.path.exists(ruta_archivo_local):
    url_archivo_drive = 'https://drive.usercontent.google.com/download?id=112-ox_3811pQ6KeiVTe8hq7scscsePFC&export=download&authuser=0&confirm=t&uuid=1a48ecf2-7652-446e-9cf1-decc37608413&at=APZUnTVa9PAmtDhUDzd9afz7Ye6v:1700775698277'
    gdown.download(url_archivo_drive, ruta_archivo_local, quiet=False)


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///WDI.db")


selectedcountry = ""


@app.route('/', methods=["GET", "POST"])
def hello_world():

   if  request.method == "GET":

        print("success")


        return render_template("/index.html")

   elif request.method == "POST":

       inputform = request.form.get("inputform")

       print(inputform)

       return render_template("/index.html")

@app.route("/trycountries", methods=["GET", "POST"])
def trycountries():

    if request.method == "GET":

        countries = []

        getcountries = db.execute("SELECT ShortName FROM WDICountry")

        for i in getcountries:
            i = i["ShortName"]
            countries.append(i)

        return render_template("/trycountries.html", countries=countries)

    if request.method == "POST":

        selectedcountry = request.form.get("selectedcountry")
        session["country"] = selectedcountry

        getcountrycode = db.execute("SELECT CountryCode FROM WDICountry WHERE ShortName = ?", session["country"])[0]["CountryCode"]
        session["countrycode"] = getcountrycode

        print(session["country"])
        print(session["countrycode"])

        return redirect("/tryseries")

@app.route("/tryseries", methods=["POST","GET"])
def tryseries():

    if request.method == "GET":

        series = []

        getseries = db.execute("SELECT IndicatorName FROM WDIData WHERE CountryCode = ?", session["countrycode"])

        for i in getseries:
            series.append(i["IndicatorName"])

        serieskeys = list(getseries[0].keys())

        return render_template("/tryseries.html", series=series, serieskeys=serieskeys)

    if request.method == "POST":

        gettheseries = request.form.get("selectedseries")
        getdata = db.execute("SELECT * FROM WDIData WHERE CountryCode = ? AND IndicatorName = ?", session["countrycode"], gettheseries)

        session["data"] = getdata

        return redirect("/results")


@app.route("/results", methods=["GET", "POST"])
def results():

    if request.method == "GET":

        data = session["data"]
        data = data[0]

        newdata = {}

        for key, value in data.items():
            if value is not None:
                newdata[key] = value

        datakeys = list(newdata.keys())[4:]
        datakeys = [int(i) for i in datakeys]

        datavalues = list(newdata.values())[4:]


        return render_template("/results.html", data=newdata, datakeys=datakeys, datavalues=datavalues)

if __name__ == '__main__':

   app.run(debug=True)
