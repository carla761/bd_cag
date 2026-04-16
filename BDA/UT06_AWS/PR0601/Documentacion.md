# PR0601. Capa bronce en Amazon AWS

## 1. Contexto

La Secretaría de Estado de Turismo quiere desarrollar un sistema de inteligencia de datos para optimizar la gestión de las playas españolas. Para ello, necesitan centralizar en un **Data Lake en AWS (Capa Bronce)** dos fuentes de información críticas:

1.  **Catálogo Nacional de Playas:** un dataset detallado con servicios, accesibilidad y características físicas.
2.  **Predicción Meteorológica:** datos en tiempo real para las zonas costeras (fuente AEMET).

Tu misión es automatizar la ingesta de estos datos hacia **Amazon S3** utilizando Python.




## 2. Objetivos de la práctica

- **Consumo de API:** gestionar la autenticación y descarga de archivos JSON desde AEMET OpenData.
- **Gestión de datos maestros:** procesar un dataset complejo en formato CSV sobre la infraestructura de las playas.
- **Arquitectura Cloud:** implementar una estructura de almacenamiento profesional y escalable en S3.
- **Seguridad:** administrar secretos y claves de acceso mediante variables de entorno.


## 3. Fuentes de datos

### A. Catálogo de playas (CSV)

Se proporciona un [archivo](./data/Playas_espa%25C3%25B1olas.csv) con información exhaustiva de las playas. También lo puedes descargar del [Portal de Datos Abiertos de ESRI](https://opendata.esri.es/datasets/84ddbc8cf4104a579d579f6441fcaa8a_0).

Los campos clave para futuras analíticas son:

- `Nombre`, `Provincia` y `Término_M` (Municipio).
- **Servicios:** `Duchas`, `Aseos`, `Acceso_dis`, `Bandera_az`.
- **Ubicación:** `Latitud`, `Longitud` y las coordenadas `X`, `Y`.
- **Estado:** `Grado_ocup` y `Grado_urba`.


### B. API AEMET OpenData (API REST)

- **Servicio:** predicción para playas (específicamente el endpoint de predicción diaria).
- **Requisito:** obtener el JSON de predicción para las provincias presentes en el CSV.
- **Nota técnica:** el alumno deberá manejar el flujo de la API (la API de AEMET devuelve un JSON con una URL, de la cual se descarga el dato final).


## 4. Requerimientos técnicos

### Fase 1: Estructura de la Capa Bronce en S3

Debes crear un bucket y organizar los datos siguiendo un esquema de **particionamiento y versionado**:

- `bronce/catalogos/guia_playas/v1/playas.csv`
- `bronce/meteorologia/prediccion_playas/year=YYYY/month=MM/day=DD/`




### Fase 2: Desarrollo del ingestor (Python)

Desarrolla un script modular que realice lo siguiente:

1.  **Módulo de carga local:** leer el CSV de playas y subirlo a S3 asegurando que el nombre del archivo incluya el origen de los datos.
2.  **Módulo API AEMET:** conectar con la API, extraer la predicción del día y guardarla directamente en S3 como un archivo JSON.

# Practica


Primero iniciamos el laboratorio de AWS.
Después descargamos las credenciales y las copiamos en el contenedor donde estamos trabajando.Luego crearemos(si no existe) un bucket en S3.

![alt](./img/PR0601.png)


```python
import boto3

try:
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    print("Conexion exitosa")
    print(f"Tienes {len(buckets['Buckets'])} buckets en tu cuenta")
except Exception as e:
    print("Error de conexión. Revisa tus credenciales.")
    print(e)
```

    Conexion exitosa
    Tienes 3 buckets en tu cuenta



```python
respuesta= s3.list_buckets()

# Recorremos la lista de diccionarios que nos da AWS
for bucket in respuesta['Buckets']:
    nombre = bucket['Name']
    print(f"Nombre del bucket: {nombre}")
```

    Nombre del bucket: cag-bd-iessanandres-practicas
    Nombre del bucket: cag-bd-iessanandres-practicas-ut6
    Nombre del bucket: cag-bd-iessanandres-practicas-ut6-pr01



```python
bucket_name="cag-bd-iessanandres-practicas-ut6-pr01"
```


```python
s3.create_bucket(Bucket=bucket_name)
```




    {'ResponseMetadata': {'RequestId': 'HRDX4CQ4G49WM8ZS',
      'HostId': 'acT2VfDxdYp/Wo95wMcSwgWPkbDE4cNEopHacM0rFgB1qV5vZqFrUlNkni6wLZfoSlasDe3BzQdX98ON/LVP4bfDn3TMZAksptcni+mcufo=',
      'HTTPStatusCode': 200,
      'HTTPHeaders': {'x-amz-id-2': 'acT2VfDxdYp/Wo95wMcSwgWPkbDE4cNEopHacM0rFgB1qV5vZqFrUlNkni6wLZfoSlasDe3BzQdX98ON/LVP4bfDn3TMZAksptcni+mcufo=',
       'x-amz-request-id': 'HRDX4CQ4G49WM8ZS',
       'date': 'Thu, 16 Apr 2026 10:46:54 GMT',
       'location': '/cag-bd-iessanandres-practicas-ut6-pr01',
       'x-amz-bucket-arn': 'arn:aws:s3:::cag-bd-iessanandres-practicas-ut6-pr01',
       'content-length': '0',
       'server': 'AmazonS3'},
      'RetryAttempts': 0},
     'Location': '/cag-bd-iessanandres-practicas-ut6-pr01',
     'BucketArn': 'arn:aws:s3:::cag-bd-iessanandres-practicas-ut6-pr01'}




```python
prefix_playas='bronce/catalogos/guia_playas/v1'
prefix_prediccion='bronce/catalogos/prediccion/v1'
```

### Carga del fichero


```python
s3.upload_file('playas.csv',bucket_name,f"{prefix_playas}/playas.csv")
print("Archivo descargado con exito")
```

    Archivo descargado con exito



```python
# Comprobar
res = s3.list_objects_v2(Bucket=bucket_name,Prefix=prefix_playas)

for obj in res.get('Contents', []):
    print(obj['Key'])
```

    bronce/catalogos/guia_playas/v1/playas.csv


### Carga de la API


```python
Key="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjYXJsYWZwMjUyNkBnbWFpbC5jb20iLCJqdGkiOiI2YTVlMjE1Yi1jMDU4LTRjNmEtOGYyNS1kMjU5MDNhY2FlMzciLCJpc3MiOiJBRU1FVCIsImlhdCI6MTc3MzkxNDUxNSwidXNlcklkIjoiNmE1ZTIxNWItYzA1OC00YzZhLThmMjUtZDI1OTAzYWNhZTM3Iiwicm9sZSI6IiJ9.ap8moh41-SDPMk2CSgL5fGtRGhlSM__KS78VuJWrEv8"
```

Descargar un fichero con los codigos de playa y hacer una llamada a la api por cada codigo


```python
import pandas as pd

df = pd.read_csv("Playas_codigos.csv",sep=';',encoding='latin1',decimal=',',dtype={'ID_PLAYA':str})
df.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID_PLAYA</th>
      <th>NOMBRE_PLAYA</th>
      <th>ID_PROVINCIA</th>
      <th>NOMBRE_PROVINCIA</th>
      <th>ID_MUNICIPIO</th>
      <th>NOMBRE_MUNICIPIO</th>
      <th>LATITUD</th>
      <th>LONGITUD</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0301101</td>
      <td>Raco de l'Albir</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3011</td>
      <td>l'Alfàs del Pi</td>
      <td>38º 34' 31"</td>
      <td>-00º 03' 52"</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0301401</td>
      <td>Sant Joan / San Juan</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 22' 48"</td>
      <td>-00º 24' 32"</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0301408</td>
      <td>El Postiguet</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 20' 46"</td>
      <td>-00º 28' 38"</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0301410</td>
      <td>Saladar</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3014</td>
      <td>Alicante/Alacant</td>
      <td>38º 17' 02"</td>
      <td>-00º 31' 08"</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0301808</td>
      <td>La Roda</td>
      <td>3</td>
      <td>Alacant/Alicante</td>
      <td>3018</td>
      <td>Altea</td>
      <td>38º 36' 29"</td>
      <td>-00º 02' 16"</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = df.head(5)
```


```python
import requests
import time
import json 
from datetime import datetime

ahora = datetime.now()
year = ahora.strftime("%Y")
month = ahora.strftime("%m")
day = ahora.strftime("%d")

# Ruta de la api
base_url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/playa/"

# ruta aws
base_path = f"{prefix_prediccion}/playas.csv"

for row in df.itertuples(index=False):
    id_playa = row.ID_PLAYA
    nombre_playa = row.NOMBRE_PLAYA.replace("/", "-")
    
    url = f"{base_url}{id_playa}?api_key={Key}"

    try:
        response = requests.get(url, headers={"Accept": "application/json"}, timeout=20)

        if response.status_code == 200:
            datos = response.json()

            url_datos = datos['datos']

            # Pausa para evitar error por hacer llamadas muy seguidas
            time.sleep(5)
            
            response_data = requests.get(url_datos, headers={"Accept": "application/json"}, timeout=20)

            if response_data.status_code == 200:
                beach_datos = response_data.json()

                file_name = f"{prefix_prediccion}/year={year}/month={month}/day={day}/{nombre_playa}.json"

                # Subir JSON a S3
                s3.put_object(
                    Bucket=bucket_name,
                    Key=file_name,
                    Body=json.dumps(beach_datos, ensure_ascii=False),
                    ContentType="application/json"
                )

                print(f"{nombre_playa} subida")

            else:
                print(f"Error descargando datos finales: {response_data.status_code}")

        else:
            print(f"Error {response.status_code} en playa {nombre_playa}")

    except Exception as e:
        print(f"Error en {nombre_playa}: {e}")

```

    Raco de l'Albir subida
    Sant Joan - San Juan subida
    Error descargando datos finales: 500
    Error 429 en playa Saladar
    Error 429 en playa La Roda


Pueden aparecer errores como el 429 debido a las limitaciones de la API de AEMET, que restringe el número de llamadas permitidas en un periodo de tiempo. Estos fallos son propios del servicio externo y no del funcionamiento del código. 
![alt](./img/error.png)


```python

```
