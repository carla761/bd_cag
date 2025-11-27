## Tarea 1: Carga de datos
El objetivo de esta tarea será poblar la base de datos Redis con los puntos de interés.

Los requisitos son:

Crear un script load_locations.py.
Utiliza la estructura de datos que está en el fichero locations.py con POIs de Madrid
El script debe conectarse a Redis y, en un bucle: - Añadir la ubicación: usa r.geoadd("poi:locations", (longitud, latitud, id)) - Guardar el nombre: usa r.hset("poi:info", id, "Nombre del POI")
Imprimir un mensaje de “Datos cargados” al finalizar.

### Script load_locations.py

```python
import redis
from locations import POIS   # Importamos la lista de POIs
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
print("ping:", r.ping())

# -------------------------------
# Tarea 1: Carga de datos (GEO + HASH)
# -------------------------------

def load_locations():
    print("\n[Carga] Insertando POIs en Redis...")
    for poi in POIS:
        poi_id = poi["id"]
        name   = poi["name"]
        lon    = poi["lon"]
        lat    = poi["lat"]

        # Guardar ubicación en el Sorted Set geoespacial
        r.geoadd("poi:locations", (lon, lat, poi_id))

        # Guardar relación id -> nombre en el Hash
        r.hset("poi:info", poi_id, name)

        print(f" [OK] {name} ({poi_id}) -> ({lat}, {lon})")

    print("\n Datos cargados correctamente")

if __name__ == "__main__":
    load_locations()
``` 


## Tarea 2: Búsqueda por radio
El objetivo de esta función es encontrar todos los POIs dentro de un radio específico desde la ubicación del usuario.

Los pasos a realizar son:

Crea un script find_by_radius.py(lat, lon, distance=2000).
Define una ubicación de “Usuario” (p.ej., lat=40.41677, lon=-3.70379, que es la Puerta del Sol).
Usa el comando GEOSERACH para encontrar todos los POIs en un radio.
Para cada POI encontrado (que será un id) consulta el HASH poi:info para obtener su nombre.
Imprime un informe: Encontrados X POIs en 2 km:
-> Museo del Prado (id_001)
-> Palacio Real (id_003)

### Script find_by_radius.py(lat, lon, distance=2000)

```python
import redis
from locations import POIS   # Importamos la lista de POIs
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
print("ping:", r.ping())

# -------------------------------
# Tarea 2: Búsqueda por radio (GEOSERACH)
# -------------------------------

def find_by_radius(lat=40.416775, lon=-3.703790, distance=2000):
    print(f"\n[Busqueda] Centro usuario: ({lat}, {lon}) | Radio: {distance} m")

    # GEOSERACH: obtener ids dentro del radio
    poi_ids = r.geosearch(
        "poi:locations",
        longitude=lon,
        latitude=lat,
        radius=distance,
        unit="m"
    )

    if not poi_ids:
        print(f"Encontrados 0 POIs en {distance/1000:.1f} km.")
        return []

    # Resolver nombres desde el HASH poi:info
    results = []
    for poi_id in poi_ids:
        name = r.hget("poi:info", poi_id)
        results.append((poi_id, name))

    # Informe
    print(f"Encontrados {len(results)} POIs en {distance/1000:.1f} km:")
    for poi_id, name in results:
        print(f" -> {name} ({poi_id})")

    return results

if __name__ == "__main__":
    find_by_radius()
```

## Tarea 3 (Opcional): Búsqueda del “más cercano”
El objetivo será encontrar el punto de interés único más cercano al usuario, sin importar la distancia.

Debes de:

Crear un script find_nearest.py(lat, lon) que recogerá la ubicación del usuario.
Usa el comando GEOSERACH para encontrar el POI más cercano (solo 1).
Asegúrate de pedir también la distancia.
Imprime el resultado: El POI más cercano es "Nombre del POI", que está a X.XX km.