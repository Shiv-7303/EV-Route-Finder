from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def lat_lon():
    lat1, lon1 = 0, 0
    lat2, lon2 = 0, 0

    def geocode_address(address):
        url = "https://trueway-geocoding.p.rapidapi.com/Geocode"

        querystring = {"address": address, "language": "en"}

        headers = {
            "X-RapidAPI-Key": "8f0cfc0a75msh9764cf6ddb7cd1fp1f7851jsnc19bc89592da",
            "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                location = results[0].get('location', {})
                return location.get('lat', 0), location.get('lng', 0)

        return 0, 0

    if request.method == "POST":
        start_address = request.form.get("start_address")
        end_address = request.form.get("end_address")

        lat1, lon1 = geocode_address(start_address)
        lat2, lon2 = geocode_address(end_address)

    return render_template("index.html", start=(lat1, lon1, start_address), end=(lat2, lon2, end_address))



if __name__ == "__main__":
    app.run(debug=True)
