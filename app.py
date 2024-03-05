from flask import Flask, render_template, request, url_for, redirect
import requests
from geopy import distance
import polyline
app = Flask(__name__)

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

def get_distance(lat1, lon1, lat2, lon2):
        url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"

        querystring = {"origins":f"{lat1},{lon1}","destinations":f"{lat2},{lon2}"}

        headers = {
            "X-RapidAPI-Key": "8f0cfc0a75msh9764cf6ddb7cd1fp1f7851jsnc19bc89592da",
            "X-RapidAPI-Host": "trueway-matrix.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            results = response.json()
            distance = results['distances'][0][0]
            duration = results['durations'][0][0]
            return distance/1000 , round(duration/3600, 2)

@app.route("/", methods=["GET", "POST"])
def lat_lon():
    lat1, lon1, lat2, lon2 = 0, 0, 0, 0
    DISTANCE = (0, 0)
    start_address,end_address = "",""
    if request.method == "POST":
        start_address = request.form.get("start_address")
        end_address = request.form.get("end_address")

        lat1, lon1 = geocode_address(start_address)
        lat2, lon2 = geocode_address(end_address)
        print(lat1, lon1, lat2, lon2)
        DISTANCE = get_distance(lat1, lon1, lat2, lon2)
    return render_template("index.html",start=(lat1, lon1,), end=(lat2, lon2,), distance = DISTANCE, start_add = start_address, end_add = end_address)


@app.route('/get_directions', methods=['POST', 'GET'])
def get_direction():
    if request.method == 'POST':
        source = request.form.get('start_address')
        destination = request.form.get('end_address')

        # Convert addresses to coordinates (optional)
        # You may need to use a geocoding service for this step
        # ... (code to convert addresses to coordinates)

        src_corr = geocode_address(source)
        des_corr = geocode_address(destination)
        body = {
            "coordinates": [[src_corr[0], src_corr[1]], [des_corr[0], des_corr[1]]],
        }

        # Set headers with your API key
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': '5b3ce3597851110001cf624858f0340ff04a4eaa9a0d9fc20803e0bb',
            'Content-Type': 'application/json; charset=utf-8'
        }

        # Send request and handle response
        try:
            response = requests.get(f'https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf624858f0340ff04a4eaa9a0d9fc20803e0bb&start={src_corr[1]},{src_corr[0]}&end={des_corr[1]},{des_corr[0]}',headers=headers)
            response.raise_for_status()  # Raise an exception for error codes
            directions_data = response.json()
            print(directions_data)
            # Extract relevant data for markers and path (adapt based on API response structure)
            # Assuming markers are embedded in the "geometry" property
            markers = directions_data['features'][0]['geometry']['coordinates']
            path = directions_data['features'][0]['geometry']['coordinates']
            print(markers)
            return render_template('map.html', markers=markers, path=path , source = source, destination = destination)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            # Handle errors appropriately (e.g., return error message to user)
            return redirect("/")
    return render_template("map.html",markers=markers, path=path , source = source, destination = destination)

if __name__ == "__main__":
    app.run(debug=True)
