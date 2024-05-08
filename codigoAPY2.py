import requests
import urllib.parse

# URL base para la geocodificación y enrutamiento
url_geocodificacion = "https://graphhopper.com/api/1/geocode?"
url_ruta = "https://graphhopper.com/api/1/route?"
clave_api = "6e26b0cd-c83c-429a-8a1c-e32ac7ef822d" # Reemplaza con tu clave API

def geocodificar(direccion, clave):
    while direccion == "":
        direccion = input("Ingrese la ubicación nuevamente: ")
    url = url_geocodificacion + urllib.parse.urlencode({"q": direccion, "limit": "1", "key": clave})
    respuesta = requests.get(url)
    datos_json = respuesta.json()
    estado_json = respuesta.status_code
    
    if estado_json == 200 and len(datos_json["hits"]) != 0:
        latitud = datos_json["hits"][0]["point"]["lat"]
        longitud = datos_json["hits"][0]["point"]["lng"]
        nombre = datos_json["hits"][0]["name"]
        valor = datos_json["hits"][0]["osm_value"]

        pais = datos_json["hits"][0].get("country", "")
        estado = datos_json["hits"][0].get("state", "")
        
        nueva_loc = nombre
        if estado and pais:
            nueva_loc += ", " + estado + ", " + pais
        elif estado:
            nueva_loc += ", " + estado
        
        print("URL de geocodificación para " + nueva_loc + " (Tipo de Ubicación: " + valor + ")\n" + url)
    else:
        latitud = "null"
        longitud = "null"
        nueva_loc = direccion
        if estado_json != 200:
            print("Estado de la API de Geocodificación: " + str(estado_json) + "\nMensaje de Error: " + datos_json["message"])
    return estado_json, latitud, longitud, nueva_loc

    
while True:
    print("\n+-----------------------------------------")
    print("Tipos de transporte en Graphhopper:")
    print("--------------------------------------------")
    print("car, bike, foot")
    print("--------------------------------------------")
    perfiles = ["car", "bike", "foot"]
    vehiculo = input("Seleccione el medio de transporte: ")
    if vehiculo == "salir" or vehiculo == "s":
        break
    elif vehiculo in perfiles:
        vehiculo = vehiculo
    else:
        vehiculo = "car" 
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de carro.") 
    loc_inicio = input("Ubicación de inicio: ")
    if loc_inicio == "salir" or loc_inicio == "s":
        break 
    inicio = geocodificar(loc_inicio, clave_api)
    print(inicio)
    loc_destino = input("Destino: ")
    if loc_destino == "salir" or loc_destino == "s":
        break 
    destino = geocodificar(loc_destino, clave_api)
    print("-----------------------------------------------")
    if inicio[0] == 200 and destino[0] == 200: 
        op = "&point=" + str(inicio[1]) + "%2C" + str(inicio[2])
        dp = "&point=" + str(destino[1]) + "%2C" + str(destino[2])
        url_rutas = url_ruta + urllib.parse.urlencode({"key": clave_api, "vehicle": vehiculo, "locale": "es"}) + op + dp 
        estado_rutas = requests.get(url_rutas).status_code
        datos_rutas = requests.get(url_rutas).json()
        print("Estado de la API de Enrutamiento: " + str(estado_rutas) + "\nURL de la API de Enrutamiento:\n" + url_rutas) 
        print("-----------------------------------------------------------")
        print("Direcciones desde " + inicio[3] + " hasta " + destino[3] + " en " + vehiculo) 
        print("=-------------------------------------------------------------")
        if estado_rutas == 200: 
            millas = (datos_rutas["paths"][0]["distance"]) / 1000 / 1.61
            km = (datos_rutas["paths"][0]["distance"]) / 1000  
            sec = int(datos_rutas["paths"][0]["time"] / 1000 % 60)
            min = int(datos_rutas["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(datos_rutas["paths"][0]["time"] / 1000 / 60 / 60) 
            print("Distancia Recorrida: {0:.1f} millas / {1:.1f} km".format(millas, km))   
            print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec)) 
            print("----------------------------------------------------------") 
            for i in range(len(datos_rutas["paths"][0]["instructions"])):
                instruccion = datos_rutas["paths"][0]["instructions"][i]["text"]
                distancia = datos_rutas["paths"][0]["instructions"][i]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(instruccion, distancia / 1000, distancia / 1000 / 1.61))