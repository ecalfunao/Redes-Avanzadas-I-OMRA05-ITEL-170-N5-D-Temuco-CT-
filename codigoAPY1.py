import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "6e26b0cd-c83c-429a-8a1c-e32ac7ef822d" ###clave de API

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data["hits"]) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        if state and country:
            location_info = f"{name}, {state}, {country}"
        elif state:
            location_info = f"{name}, {state}"
        else:
            location_info = name
        print(f"Geocoding API URL for {location_info} (Location Type: {value})\n{url}")
    else:
        lat = "null"
        lng = "null"
        location_info = "No se pudo encontrar la ubicación"
    return json_status, lat, lng, location_info
loc1 = input("Ingrese la ubicación de origen: ")
loc2 = input("Ingrese la ubicación de destino: ")

orig = geocoding(loc1, key)
print(orig)
print("-------------------------------------------------------------------------------------------------------------")
dest = geocoding(loc2, key)
print(dest)
