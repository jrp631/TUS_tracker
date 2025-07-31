import requests
import time
import logging
import itertools
import threading
import sys 
# from pyproj import Proj, transform

"""
json example

{"summary":{"items":40336,"items_per_page":50,"pages":807,"current_page":1},"resources":[
    {
      "wgs84_pos:long":"-3.8131307728304242",
      "ayto:instante":"2025-07-30T06:01:08.563Z",
      "gn:coordY":"4813062",
      "gn:coordX":"434332",
      "ayto:linea":"51",
      "ayto:velocidad":"16",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.4657099670395",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2586.json"},
    {
      "wgs84_pos:long":"-3.8107067736201556",
      "ayto:instante":"2025-07-30T06:01:33.567Z",
      "gn:coordY":"4813052",
      "gn:coordX":"434528",
      "ayto:linea":"51",
      "ayto:velocidad":"27",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.465637122210495",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2587.json"},
    {
      "wgs84_pos:long":"-3.8080201987373314",
      "ayto:instante":"2025-07-30T06:01:58.560Z",
      "gn:coordY":"4813017",
      "gn:coordX":"434745",
      "ayto:linea":"51",
      "ayto:velocidad":"31",
      "dc:modified":"2025-07-30T09:50:58.009Z",
      "ayto:vehiculo":"77",
      "wgs84_pos:lat":"43.46534097281779",
      "ayto:estado":"5",
      "uri":"http://datos.santander.es/api/datos/control_flotas_posiciones/2588.json"} 
      
      
CAMPOS 
- ayto:linea: Linea a la que da servicio el autobus identificado en cada registro.
- ayto:gem2d:x: Coordenada X de la posición del vehículo. Formato UTM (ED50)
- ayto:gem2d:y: Coordenada Y de la posición del vehículo. Formato UTM (ED50)
- ayto:indice: representa un identificador y un orden para cada una de las 5 capturas de posición del vehículo. Siendo el valor 0 la captura de posición más reciente y 4 la más lejana
- ayto:instante: fecha y hora en la que se ha tomado el valor de la posición
- ayto:velocidad: Velocidad a la que se desplaza el vehículo (Km/h)
- ayto:vehiculo: Numero de identificación fisico del vehículo
- ayto:coche: Numero de identificación logico del vehículo que se asigna en función de la línea y tarjeta que realiza; por ejemplo el coche 11 corresponde con la línea 1 y Servicio de Informática tarjeta 1, el coche 53 es la línea 5c1 (impar) y la tarjeta 3, el coche 64 es la línea 6c2 (par) y la tarjeta 4, el 162 es la línea 16 y tarjeta 2.
- ayto:estado: define la situación en la que se encuentra un vehículo. Por ejemplo el estado 4 indica que el Vehículo está en el trayecto de retirada a cocheras, mientras que el estado 5 indica que está sirviendo la línea que tiene asignada. La codificación del ESTADO es: 1 - No asignado 2 - Asignado 3 - Incorporación 4 - Retirada 5 - En línea 6 - Fuera de línea 7 - Deslocalizado 8 - En vacío 9 - Desvío
"""


URL="https://datos.santander.es/api/rest/datasets/control_flotas_posiciones.json"


linas = [] # list to store bus lines that we gather as the program runs

log_file = "lineas.log"

done = False

def utm_to_latlon(este, norte, zona_utm, hemisferio='n'):
    """
    Convierte coordenadas UTM a latitud y longitud.
    
    Parámetros:
    - este (float): Coordenada Este (X) en metros
    - norte (float): Coordenada Norte (Y) en metros
    - zona_utm (int or str): Zona UTM (ej. 30 para España peninsular)
    - hemisferio (str): 'n' para hemisferio norte, 's' para hemisferio sur
    
    Retorna:
    - (latitud, longitud) en grados decimales
    """
    try:
        # Definir el sistema de coordenadas UTM
        utm_proj = Proj(proj='utm', zone=zona_utm, ellps='WGS84', south=(hemisferio.lower() == 's'))
        
        # Definir el sistema de coordenadas geográficas (lat/lon WGS84)
        wgs84_proj = Proj(proj='latlong', datum='WGS84')
        
        # Realizar la transformación
        longitud, latitud = transform(utm_proj, wgs84_proj, este, norte)
        
        return latitud, longitud
    
    except Exception as e:
        print(f"Error en la conversión: {e}")
        return None, None

# Ejemplo de uso
# if __name__ == "__main__":
#     # Coordenadas UTM de ejemplo (Madrid, España - zona 30N)
#     este = 440000
#     norte = 4475000
#     zona = 30
#     hemisferio = 'n'
    
#     lat, lon = utm_to_latlon(este, norte, zona, hemisferio)
#     print(f"Latitud: {lat:.6f}, Longitud: {lon:.6f}")


class linea_tus:
  def __init__(self, linea, vehiculo, lat, lon, coordx, coordy):
     self.linea = linea
     self.vehiculo = vehiculo
     self.lat = lat
     self.lon = lon
     self.coordx = coordx
     self.coordy = coordy

def load_animation(): 
  for c in itertools.cycle(['|', '/', '-', '\\']):
    if done:
        break
    sys.stdout.write(f'\rLoading... {c}')
    sys.stdout.flush()
    time.sleep(0.1)
  sys.stdout.write('\rDone!          \n')

def main():
    print("TUS tracker...")
    
    logger = logging.getLogger("TUS Tracker")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Start the loading animation in a separate thread
    # animation_thread = threading.Thread(target=load_animation)
    # animation_thread.start()
    
    found_vehicles = []
    
    # make a request to the URL every second 
    while (True):
        try:
            # print("Fetching data...")
            response = requests.get(URL)
            if response.status_code == 200:
                data = response.json()
                resources = data.get("resources", [])
                
                #DATA PROCESSING
                linea_coords = {}
                linea_last_coords = {}
                for resource in resources:
                    linea = resource.get("ayto:linea", "")
                    vehiculo = resource.get("ayto:vehiculo", "")
                    lat = resource.get("wgs84_pos:lat", "")
                    lon = resource.get("wgs84_pos:long", "")
                    coordx = resource.get("gn:coordX", "")
                    coordy = resource.get("gn:coordY", "")
                    
                    #create a linea_tus object with the gathered data
                    linea_obj = linea_tus(linea, vehiculo, lat, lon, coordx, coordy)
                    # print(f"Linea: {linea_obj.linea}, Vehiculo: {linea_obj.vehiculo}, Lat: {linea_obj.lat}, Lon: {linea_obj.lon}, CoordX: {linea_obj.coordx}, CoordY: {linea_obj.coordy}")
                    #check if the vehiculo is already in the dictionary
                    if vehiculo not in found_vehicles:
                        found_vehicles.append(vehiculo)
                        # print(f"New vehicle detected: {vehiculo}")
                        logger.info(f"New vehicle detected: {vehiculo} on line {linea}")
                        print(f"New vehicle detected: {vehiculo} on line {linea}")
                        

                
                # for resource in resources:
                #     # cheak if the line is already in the list if it is not add it
                #     line = resource.get("ayto:linea", "")
                #     if line not in linas:
                #         linas.append(line)
                #         print(f"New line detected: {line}")
                #         logger.info(f"New line detected: {line}")



                    # print(f"{'Linea':<6} {'Vehiculo':<9} {'Velocidad':<10} {'Estado':<6}")
                    # print("-" * 36)
                    # for resource in resources:
                    #   print(f"{resource.get('ayto:linea', ''):<6} {resource.get('ayto:vehiculo', ''):<9} {resource.get('ayto:velocidad', ''):<10} {resource.get('ayto:estado', ''):<6}")
                    # break  # Print table once per request
            else:
                print(f"Error fetching data: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
            done = True
        
        time.sleep(0.5)
        

if __name__ == "__main__":
  main()