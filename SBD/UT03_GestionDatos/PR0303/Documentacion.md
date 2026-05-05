# PR0303: Obtención de datos de una API REST

# Práctica: Ingesta de Datos con Star Wars API (SWAPI)

El objetivo de esta práctica será desarrollar un script en Python que extraiga información de [swapi.dev](https://swapi.dev/) y la transforme en DataFrames de Pandas listos para el análisis.



```python
!pip install requests
```

    Requirement already satisfied: requests in /opt/conda/lib/python3.11/site-packages (2.31.0)
    Requirement already satisfied: charset-normalizer<4,>=2 in /opt/conda/lib/python3.11/site-packages (from requests) (3.3.0)
    Requirement already satisfied: idna<4,>=2.5 in /opt/conda/lib/python3.11/site-packages (from requests) (3.4)
    Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/conda/lib/python3.11/site-packages (from requests) (2.0.7)
    Requirement already satisfied: certifi>=2017.4.17 in /opt/conda/lib/python3.11/site-packages (from requests) (2023.7.22)


## 1.- Conexión básica y primer dataFrame

En esta fase, debes conectar con el endpoint de **Vehículos** y extraer la primera página de resultados (10 elementos).

Los pasos a realizar son:

1. Realizaruna petición `GET` al endpoint `https://swapi.dev/api/vehicles/`.
2. Extrae la clave `results` del JSON de respuesta.
3. Convierte esa lista de diccionarios en un dataframe de Pandas.
4. Muestra las primeras 5 filas y el nombre de las columnas obtenidas.


```python
import requests

# 1. Petición GET al endpoint
url ='https://swapi.dev/api/vehicles'

response = requests.get(url)

if response.status_code == 200:
    print("Conexión establecida")
    datos = response.json()
else:
    print(f"Error:{response.status_code}")
```

    Conexión establecida



```python
import pandas as pd
results = datos['results']
df = pd.DataFrame(results)
```


```python
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
      <th>name</th>
      <th>model</th>
      <th>manufacturer</th>
      <th>cost_in_credits</th>
      <th>length</th>
      <th>max_atmosphering_speed</th>
      <th>crew</th>
      <th>passengers</th>
      <th>cargo_capacity</th>
      <th>consumables</th>
      <th>vehicle_class</th>
      <th>pilots</th>
      <th>films</th>
      <th>created</th>
      <th>edited</th>
      <th>url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sand Crawler</td>
      <td>Digger Crawler</td>
      <td>Corellia Mining Corporation</td>
      <td>150000</td>
      <td>36.8</td>
      <td>30</td>
      <td>46</td>
      <td>30</td>
      <td>50000</td>
      <td>2 months</td>
      <td>wheeled</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>2014-12-10T15:36:25.724000Z</td>
      <td>2014-12-20T21:30:21.661000Z</td>
      <td>https://swapi.dev/api/vehicles/4/</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T-16 skyhopper</td>
      <td>T-16 skyhopper</td>
      <td>Incom Corporation</td>
      <td>14500</td>
      <td>10.4</td>
      <td>1200</td>
      <td>1</td>
      <td>1</td>
      <td>50</td>
      <td>0</td>
      <td>repulsorcraft</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/films/1/]</td>
      <td>2014-12-10T16:01:52.434000Z</td>
      <td>2014-12-20T21:30:21.665000Z</td>
      <td>https://swapi.dev/api/vehicles/6/</td>
    </tr>
    <tr>
      <th>2</th>
      <td>X-34 landspeeder</td>
      <td>X-34 landspeeder</td>
      <td>SoroSuub Corporation</td>
      <td>10550</td>
      <td>3.4</td>
      <td>250</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>unknown</td>
      <td>repulsorcraft</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/films/1/]</td>
      <td>2014-12-10T16:13:52.586000Z</td>
      <td>2014-12-20T21:30:21.668000Z</td>
      <td>https://swapi.dev/api/vehicles/7/</td>
    </tr>
    <tr>
      <th>3</th>
      <td>TIE/LN starfighter</td>
      <td>Twin Ion Engine/Ln Starfighter</td>
      <td>Sienar Fleet Systems</td>
      <td>unknown</td>
      <td>6.4</td>
      <td>1200</td>
      <td>1</td>
      <td>0</td>
      <td>65</td>
      <td>2 days</td>
      <td>starfighter</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>2014-12-10T16:33:52.860000Z</td>
      <td>2014-12-20T21:30:21.670000Z</td>
      <td>https://swapi.dev/api/vehicles/8/</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Snowspeeder</td>
      <td>t-47 airspeeder</td>
      <td>Incom corporation</td>
      <td>unknown</td>
      <td>4.5</td>
      <td>650</td>
      <td>2</td>
      <td>0</td>
      <td>10</td>
      <td>none</td>
      <td>airspeeder</td>
      <td>[https://swapi.dev/api/people/1/, https://swap...</td>
      <td>[https://swapi.dev/api/films/2/]</td>
      <td>2014-12-15T12:22:12Z</td>
      <td>2014-12-20T21:30:21.672000Z</td>
      <td>https://swapi.dev/api/vehicles/14/</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.columns
```




    Index(['name', 'model', 'manufacturer', 'cost_in_credits', 'length',
           'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity',
           'consumables', 'vehicle_class', 'pilots', 'films', 'created', 'edited',
           'url'],
          dtype='object')



## 2.- Gestión de paginación

La API de Star Wars devuelve los resultados de 10 en 10. Pero necesitamos el dataset completo de **personajes (people)**.

En este apartado debes:

1. Implementar un bucle (`while`) que verifique la existencia de la clave `next` en el JSON.
2. Iterar por todas las páginas (aprox. 82 personajes) recolectando los datos en una lista global.
3. Crear un DataFrame único con todos los registros.
4. Verifica que el DataFrame resultante tenga el mismo número de filas que el valor indicado en la clave `count` de la API.



```python
# Endpoint inicial
url = "https://swapi.dev/api/people/"

# Lista donde acumularemos todos los personajes
all_people =[]

# Bucle While
while url is not None:
    response = requests.get(url)
    data = response.json()

    # Añadir los resultados 
    all_people.extend(data["results"])

    # Actualizar la url 
    url = data["next"]
```


```python
df_people = pd.DataFrame(all_people)

# Verificar el DataFrame
print("Filas del DataFrame:",len(df_people))
print("Valor de Count en la API:",data['count'])

df_people.head(5)
```

    Filas del DataFrame: 82
    Valor de Count en la API: 82





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
      <th>name</th>
      <th>height</th>
      <th>mass</th>
      <th>hair_color</th>
      <th>skin_color</th>
      <th>eye_color</th>
      <th>birth_year</th>
      <th>gender</th>
      <th>homeworld</th>
      <th>films</th>
      <th>species</th>
      <th>vehicles</th>
      <th>starships</th>
      <th>created</th>
      <th>edited</th>
      <th>url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C-3PO</td>
      <td>167</td>
      <td>75</td>
      <td>n/a</td>
      <td>gold</td>
      <td>yellow</td>
      <td>112BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:10:51.357000Z</td>
      <td>2014-12-20T21:17:50.309000Z</td>
      <td>https://swapi.dev/api/people/2/</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R2-D2</td>
      <td>96</td>
      <td>32</td>
      <td>n/a</td>
      <td>white, blue</td>
      <td>red</td>
      <td>33BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/8/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:11:50.376000Z</td>
      <td>2014-12-20T21:17:50.311000Z</td>
      <td>https://swapi.dev/api/people/3/</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Darth Vader</td>
      <td>202</td>
      <td>136</td>
      <td>none</td>
      <td>white</td>
      <td>yellow</td>
      <td>41.9BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/starships/13/]</td>
      <td>2014-12-10T15:18:20.704000Z</td>
      <td>2014-12-20T21:17:50.313000Z</td>
      <td>https://swapi.dev/api/people/4/</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Leia Organa</td>
      <td>150</td>
      <td>49</td>
      <td>brown</td>
      <td>light</td>
      <td>brown</td>
      <td>19BBY</td>
      <td>female</td>
      <td>https://swapi.dev/api/planets/2/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/30/]</td>
      <td>[]</td>
      <td>2014-12-10T15:20:09.791000Z</td>
      <td>2014-12-20T21:17:50.315000Z</td>
      <td>https://swapi.dev/api/people/5/</td>
    </tr>
  </tbody>
</table>
</div>



## 3.- Cruce de datos

En este punto vamos a combinar datos de diferentes endpoints, en concreto, enriqueceremos los datos de personajes obtenidos en el punto anterior con información de su planeta de origen.

Tienes que hacer lo siguiente:

1. La columna `homeworld` de cada personaje es una URL (ej: `https://swapi.dev/api/planets/1/`).
2. Crea una función que reciba esa URL y devuelva una tupla con el **nombre, terreno y población del planeta** (haciendo una nueva petición a la API).
3. Aplica esta función a los primeros 20 personajes del DataFrame (para no saturar la API) y añade al dataframe de personajes los datos correspondientes a su planeta.




```python
# Funcion para obtener datos del planeta
def obtener_planeta(url):
    response = requests.get(url)
    data = response.json()
    return(
        data.get('name'),
        data.get('terrain'),
        data.get('population')
    )
```


```python
# Hacer una copia del dataset más corta
df_subset = df_people.head(20).copy()

# Aplicar la función en la columna 'homeworld'
df_subset['planeta_info'] = df_subset['homeworld'].apply(obtener_planeta)
df_subset['planeta_info'].head(5)
```




    0                           (Tatooine, desert, 200000)
    1                           (Tatooine, desert, 200000)
    2    (Naboo, grassy hills, swamps, forests, mountai...
    3                           (Tatooine, desert, 200000)
    4        (Alderaan, grasslands, mountains, 2000000000)
    Name: planeta_info, dtype: object




```python
# Convertir a lista la tupla que tenemos poniendo los nombres de cada columna
df_subset[['nombre_planeta','terreno_planeta','poblacion_planeta']] = df_subset['planeta_info'].tolist()

# Eliminar la columna 'planeta_info'
df_subset.drop(columns=['planeta_info'], inplace=True)
```


```python
df_subset.head()
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
      <th>name</th>
      <th>height</th>
      <th>mass</th>
      <th>hair_color</th>
      <th>skin_color</th>
      <th>eye_color</th>
      <th>birth_year</th>
      <th>gender</th>
      <th>homeworld</th>
      <th>films</th>
      <th>species</th>
      <th>vehicles</th>
      <th>starships</th>
      <th>created</th>
      <th>edited</th>
      <th>url</th>
      <th>nombre_planeta</th>
      <th>terreno_planeta</th>
      <th>poblacion_planeta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C-3PO</td>
      <td>167</td>
      <td>75</td>
      <td>n/a</td>
      <td>gold</td>
      <td>yellow</td>
      <td>112BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:10:51.357000Z</td>
      <td>2014-12-20T21:17:50.309000Z</td>
      <td>https://swapi.dev/api/people/2/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R2-D2</td>
      <td>96</td>
      <td>32</td>
      <td>n/a</td>
      <td>white, blue</td>
      <td>red</td>
      <td>33BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/8/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:11:50.376000Z</td>
      <td>2014-12-20T21:17:50.311000Z</td>
      <td>https://swapi.dev/api/people/3/</td>
      <td>Naboo</td>
      <td>grassy hills, swamps, forests, mountains</td>
      <td>4500000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Darth Vader</td>
      <td>202</td>
      <td>136</td>
      <td>none</td>
      <td>white</td>
      <td>yellow</td>
      <td>41.9BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/starships/13/]</td>
      <td>2014-12-10T15:18:20.704000Z</td>
      <td>2014-12-20T21:17:50.313000Z</td>
      <td>https://swapi.dev/api/people/4/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Leia Organa</td>
      <td>150</td>
      <td>49</td>
      <td>brown</td>
      <td>light</td>
      <td>brown</td>
      <td>19BBY</td>
      <td>female</td>
      <td>https://swapi.dev/api/planets/2/</td>
      <td>[https://swapi.dev/api/films/1/, https://swapi...</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/30/]</td>
      <td>[]</td>
      <td>2014-12-10T15:20:09.791000Z</td>
      <td>2014-12-20T21:17:50.315000Z</td>
      <td>https://swapi.dev/api/people/5/</td>
      <td>Alderaan</td>
      <td>grasslands, mountains</td>
      <td>2000000000</td>
    </tr>
  </tbody>
</table>
</div>



## 4.- Expansión de filas (opcional)

Seguro que te has fijado que la consulta de personajes devuelve un JSON en el que hay un campo que contiene una lista de películas en que aparece dicho personaje. Ese campo combinado es poco útil si queremos realizar operaciones para extraer información de los datos (por ejemplo, cuántos personajes de media hay en cada película?).

Vas a usar la función `explode()` de Pandas, que expande un registro con un campo con una lista en varios registros, uno por cada elemento que tenga la lista.

Por ejemplo, si tenemos los siguientes datos en un dataframe:
```
Luke Skywalker	172	['film1', 'film2', 'film3']
```

Y ejecutamos `df.explode('films')` obtendremos lo siguiente:

```
Luke Skywalker	172	film1
Luke Skywalker	172	film2
Luke Skywalker	172	film3
```

Realiza esta operación sobre el dataframe del ejercicio anterior para expandir la lista de películas de cada personaje (hazlo sobre un subconjunto de los datos para no sobrecargar la API) y reemplaza el identificador de la película por su título.


```python
# Expandir un campo con una lista
df_exploded = df_subset.explode("films")
```


```python
# Función para obtener el nombre de la película
def obtener_titulo_pelicula(url):
    datos = requests.get(url).json()
    return datos.get("title")

```


```python
# Aplicar la funcion en una nueva columna
df_exploded["film_title"] = df_exploded["films"].apply(obtener_titulo_pelicula)

# Eliminar la columna de la url de 'films'
df_exploded.drop(columns=["films"], inplace=True)

# Mostrar resultado
df_exploded.head(5)
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
      <th>name</th>
      <th>height</th>
      <th>mass</th>
      <th>hair_color</th>
      <th>skin_color</th>
      <th>eye_color</th>
      <th>birth_year</th>
      <th>gender</th>
      <th>homeworld</th>
      <th>species</th>
      <th>vehicles</th>
      <th>starships</th>
      <th>created</th>
      <th>edited</th>
      <th>url</th>
      <th>nombre_planeta</th>
      <th>terreno_planeta</th>
      <th>poblacion_planeta</th>
      <th>film_title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
      <td>A New Hope</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
      <td>The Empire Strikes Back</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
      <td>Return of the Jedi</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Luke Skywalker</td>
      <td>172</td>
      <td>77</td>
      <td>blond</td>
      <td>fair</td>
      <td>blue</td>
      <td>19BBY</td>
      <td>male</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[]</td>
      <td>[https://swapi.dev/api/vehicles/14/, https://s...</td>
      <td>[https://swapi.dev/api/starships/12/, https://...</td>
      <td>2014-12-09T13:50:51.644000Z</td>
      <td>2014-12-20T21:17:56.891000Z</td>
      <td>https://swapi.dev/api/people/1/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
      <td>Revenge of the Sith</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C-3PO</td>
      <td>167</td>
      <td>75</td>
      <td>n/a</td>
      <td>gold</td>
      <td>yellow</td>
      <td>112BBY</td>
      <td>n/a</td>
      <td>https://swapi.dev/api/planets/1/</td>
      <td>[https://swapi.dev/api/species/2/]</td>
      <td>[]</td>
      <td>[]</td>
      <td>2014-12-10T15:10:51.357000Z</td>
      <td>2014-12-20T21:17:50.309000Z</td>
      <td>https://swapi.dev/api/people/2/</td>
      <td>Tatooine</td>
      <td>desert</td>
      <td>200000</td>
      <td>A New Hope</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
