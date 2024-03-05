from flask import Flask, render_template, request, url_for, redirect
import requests
from geopy import distance
import polyline

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

src_corr = geocode_address("Thane,Mumbai")
des_corr = geocode_address("Ghansoli,Mumbai")
response = (f'https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf624858f0340ff04a4eaa9a0d9fc20803e0bb&start={src_corr[1]},{src_corr[0]}&end={des_corr[1]},{des_corr[0]}',)
print(response)
print(f"{src_corr[0]}, {src_corr[1]}")
print(f"{des_corr[0]}, {des_corr[1]}")