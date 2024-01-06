from flask import Flask, redirect, url_for, render_template, request
import requests

app = Flask(__name__)

nasa_api = "https://api.nasa.gov/planetary/apod"
nasa_key = "KOuiNuaE2x2mM7bjpgVleP5m9EhYTjs5fkPCnUk8"
mars_api = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

def get_apod(date):
    params = {
        "api_key" : nasa_key
    }
    if date != "today":
        params["date"] = date
    response = requests.get(nasa_api, params)
    if response.status_code != 200:
        if response.status_code == 404:
            error_apod = {
                "title": f"API Error - {response.status_code}",
                "explanation": "image not found",
                "url" : url_for('static', filename="404.jpeg")
            }
        elif response.status_code == 500:
            error_apod = {
                "title": f"API Error - {response.status_code}",
                "explanation": "server failed to send a response to a valid request",
                "url" : url_for('static', filename="500.jpeg")
            }
        return error_apod
    return response.json()

def get_rover_photos(sol, camera):
    params = {
        "api_key": nasa_key,
        "sol": sol,
        "camera": camera,
        "page": 1
    }
    res = requests.get(mars_api, params)
    return res.json()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/mars", methods=["GET", "POST"])
def mars():
    if request.method == "POST":
        sol = request.form["sol"]
        camera = request.form["camera"]
    else:
        sol = 0
        camera = "fhaz"
    data = get_rover_photos(sol, camera)
    return render_template("mars.html", photos=data["photos"])

@app.route("/apod")
@app.route("/apod/")
@app.route("/apod/<date>")
def apod(date="today"):
    data = get_apod(date)
    return render_template("apod.html", apod=data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404