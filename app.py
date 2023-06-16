from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from cs50 import SQL
import os
import gdown

ruta_archivo_local = 'WDI.db'

if not os.path.exists(ruta_archivo_local):
    url_archivo_drive = 'https://drive.google.com/uc?id=1zM2DSi0Wh5cNYmkxl4iffe1W_bBOiBlE'
    gdown.download(url_archivo_drive, ruta_archivo_local, quiet=False)
else:
    print("El archivo ya existe localmente. No se realizará ninguna descarga.")


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

        datakeys = list(data[0].keys())[4:]
        datakeys = [int(i) for i in datakeys]

        datavalues = []

        for i, x in enumerate(list(data[0].values())):

            if x == None:
                pass
            else:
                datavalues.append(x)

        return render_template("/results.html", data=data, datakeys=datakeys, datavalues=datavalues[4:])




@app.route("/about", methods=["GET", "POST"])
def about():

    if request.method == "GET":

        return render_template("/about.html")

if __name__ == '__main__':

   app.run(debug=True)