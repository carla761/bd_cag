# PR0403: Análisis de logs con MapReduce

Para esta práctica vamos a utilizar el *dataset* que puedes encontrar en Kaggle llamado [Server Logs ](https://www.kaggle.com/datasets/vishnu0399/server-logs). Ahí encontrarás un *dataset* sintético con datos con los datos de log de un servidor Apache.

Lo primero que tendrás que hacer es conocer los datos con los que vas a trabajar, como pista, cada línea tiene este formato aproximado:

`IP - - [Fecha:Hora Zona] "MÉTODO URL PROTOCOLO" Código Bytes "Referer" "User-Agent" Tiempo_Respuesta`

Como consejo, crea un fichero de **tamaño reducido** para las pruebas ya que el fichero original es bastante grande.

Realiza las siguientes tareas utilizando MapReduce.



```python
!hdfs dfs -mkdir /logs
```


```python
!hdfs dfs -put logfiles.log /logs
```


```python
!head -n 50 logfiles.log > logfiles_reduced.log
```

## 1. Estadísticas básicas

### Contador de Códigos de Estado HTTP

Queremos saber cuántas peticiones resultaron exitosas (200), cuántas no encontradas (404), errores de servidor (500), etc.

Para conseguirlo, tienes que hacer lo siguiente:

- **Mapper:**
    - Lee la línea.
    - Busca el código de estado (el número después de `"HTTP/1.0"`). En tu ejemplo son: `502`, `200`, `404`, `304`, etc.
    - Emite `(código, 1)`.
- **Reducer:** Suma los contadores.
- **Salida esperada:** `200: 50, 404: 10, 500: 5...`



```python
%%writefile mapper_ej1.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    print(f"{words[8]}\t1")
```

    Writing mapper_ej1.py



```python
%%writefile reducer_ej1.py
#!/usr/bin/env python3

import sys

current_code = 0
current_count = 0

for line in sys.stdin:
    code, count = line.strip().split("\t")
    code = int(code)

    if code == current_code:
        current_count += 1
    else:
        if current_code:
            print(f"{current_code}: {current_count}")
        current_code = code
        current_count = 0

if current_code:
     print(f"{current_code}: {current_count}")
```

    Writing reducer_ej1.py



```python
!cat logfiles_reduced.log | python3 mapper_ej1.py | sort | python3 reducer_ej1.py
```

    200: 8
    303: 4
    304: 8
    403: 3
    404: 5
    500: 5
    502: 10


### Tráfico Total por IP

En este segundo ejercicio el objetivo será identificar qué direcciones IP están consumiendo más ancho de banda.

- **Mapper:**
    - Extrae la IP (el primer campo).
    - Extrae el tamaño de la respuesta en bytes (el número después del código de estado). *Nota: a veces es un guion "-" si es 0*.
    - Emite `(IP, bytes)`.
- **Reducer:** Suma los bytes para cada IP.
- **Salida:** `162.253.4.179: 5041 bytes`



```python
%%writefile mapper_ej12.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    print(f"{words[0]}\t{words[9]}")
```

    Writing mapper_ej12.py



```python
%%writefile reducer_ej12.py
#!/usr/bin/env python3

import sys

current_ip = None
current_byte_count = 0

for line in sys.stdin:
    ip, byte_count = line.strip().split("\t")
    
    byte_count = float(byte_count)
    
    if current_ip == ip:
        current_byte_count += byte_count
    else:
        if current_ip:
            print(f"{current_ip}\t{current_byte_count} bytes")
            
        current_ip = ip
        current_byte_count = byte_count

print(f"{current_ip}\t{current_byte_count} bytes")
```

    Overwriting reducer_ej12.py



```python
!cat logfiles_reduced.log | python3 mapper_ej12.py | sort | python3 reducer_ej12.py
```

    102.247.49.87	4959.0 bytes
    115.101.165.251	4965.0 bytes
    119.170.1.203	5011.0 bytes
    125.87.60.188	4961.0 bytes
    127.72.62.237	4955.0 bytes
    137.196.118.126	4960.0 bytes
    144.140.97.239	4934.0 bytes
    148.5.169.251	5044.0 bytes
    149.194.199.18	5017.0 bytes
    154.131.45.155	5059.0 bytes
    159.238.93.133	4959.0 bytes
    160.36.208.51	4979.0 bytes
    162.253.4.179	5041.0 bytes
    172.175.150.80	4986.0 bytes
    182.215.249.159	4936.0 bytes
    183.129.168.199	4990.0 bytes
    202.8.213.171	4957.0 bytes
    203.40.76.61	4922.0 bytes
    207.194.20.187	4989.0 bytes
    211.69.213.210	4992.0 bytes
    213.90.185.182	4926.0 bytes
    217.20.3.105	4951.0 bytes
    223.254.74.157	4989.0 bytes
    228.181.201.16	4936.0 bytes
    23.162.51.3	4940.0 bytes
    230.230.213.17	5024.0 bytes
    233.223.117.90	4963.0 bytes
    238.204.144.175	5056.0 bytes
    238.217.83.154	5152.0 bytes
    252.156.232.172	5028.0 bytes
    254.54.186.144	5044.0 bytes
    255.231.52.33	5054.0 bytes
    255.27.84.112	5089.0 bytes
    26.167.128.186	5060.0 bytes
    26.44.136.193	4925.0 bytes
    41.193.26.139	4917.0 bytes
    55.25.7.93	5016.0 bytes
    58.30.103.184	5024.0 bytes
    59.107.116.6	5008.0 bytes
    66.181.188.94	4966.0 bytes
    71.158.198.139	5077.0 bytes
    71.8.223.77	4950.0 bytes
    73.91.150.125	5028.0 bytes
    78.88.250.115	4986.0 bytes
    81.23.229.106	5019.0 bytes
    84.89.201.191	4997.0 bytes
    86.194.222.239	4881.0 bytes
    90.64.62.239	4947.0 bytes
    93.47.162.191	4967.0 bytes
    97.15.37.214	4980.0 bytes


## 2. Análisis de comportamiento

### URLs más populares 

El objetivo en este ejercicio será encontrar las las rutas (`/usr/admin`, `/usr/register`) más solicitadas.

- **Mapper:**
    - Analiza la cadena de petición `DELETE /usr/admin HTTP/1.0`.
    - Extrae la URL (el segundo elemento entre las comillas).
    - Emite `(url, 1)`.
- **Reducer:** Suma las visitas.
- **Salida**: Muestra todas las URLs y el número de accesos a cada una
- **Opcional:** ¿Cómo mostrarías sólo las top 10? (Requiere un segundo paso de ordenación o un reducer inteligente).


```python
%%writefile mapper_ej2.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    print(f"{words[5]}{words[6]}{words[7]}\t1")
```

    Writing mapper_ej2.py



```python
%%writefile reducer_ej2.py
#!/usr/bin/env python3

import sys

current_url = None
current_count = 0

for line in sys.stdin:
    url, count = line.strip().split("\t")

    if current_url == url:
        current_count += 1
    else:
        if current_url:
            print(f"{current_url}: {current_count}")
        
        current_url = url
        current_count = 0

print(f"{current_url}: {current_count}")
```

    Writing reducer_ej2.py



```python
!cat logfiles_reduced.log | python3 mapper_ej2.py | sort | python3 reducer_ej2.py
```

    "DELETE/usr/admin/developerHTTP/1.0": 0
    "DELETE/usr/adminHTTP/1.0": 3
    "DELETE/usr/loginHTTP/1.0": 0
    "DELETE/usr/registerHTTP/1.0": 1
    "GET/usr/admin/developerHTTP/1.0": 0
    "GET/usr/adminHTTP/1.0": 2
    "GET/usr/loginHTTP/1.0": 2
    "GET/usr/registerHTTP/1.0": 3
    "GET/usrHTTP/1.0": 2
    "POST/usr/admin/developerHTTP/1.0": 0
    "POST/usr/adminHTTP/1.0": 0
    "POST/usr/loginHTTP/1.0": 1
    "POST/usr/registerHTTP/1.0": 1
    "POST/usrHTTP/1.0": 4
    "PUT/usr/admin/developerHTTP/1.0": 3
    "PUT/usr/adminHTTP/1.0": 1
    "PUT/usr/loginHTTP/1.0": 3
    "PUT/usr/registerHTTP/1.0": 2
    "PUT/usrHTTP/1.0": 3


### Distribución por Método HTTP

Aquí queremos saber qué tipo de acciones hacen los usuarios (GET vs POST vs DELETE).

- **Mapper:** Extrae el verbo HTTP (`GET`, `POST`, `PUT`, `DELETE`). Emite `(método, 1)`.
- **Reducer:** Suma contadores.



```python
%%writefile mapper_ej21.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    print(f"{words[5]}\t1")
```

    Writing mapper_ej21.py



```python
%%writefile reducer_ej21.py
#!/usr/bin/env python3

import sys

current_http = None
current_count = 0

for line in sys.stdin:
    http, count = line.strip().split("\t")

    if current_http == http:
        current_count += 1
    else:
        if current_http:
            print(f"{current_http}: {current_count}")
        
        current_http = http
        current_count = 0

print(f"{current_http}: {current_count}")
```

    Writing reducer_ej21.py



```python
!cat logfiles_reduced.log | python3 mapper_ej21.py | sort | python3 reducer_ej21.py
```

    "DELETE: 7
    "GET: 13
    "POST: 10
    "PUT: 16


### Análisis de navegadores

El objetivo aquí es saber si los usuarios usan Chrome, Firefox, o si son bots/móviles.

- **Mapper:**
    - Extrae la cadena larga del final (User-Agent).
    - Busca palabras clave simples: si contiene "Chrome" emite `("Chrome", 1)`, si "Firefox" emite `("Firefox", 1)`, etc.
- **Reducer:** Suma totales por navegador.



```python
%%writefile mapper_ej22.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    
    # Comprobamos que la linea tenga suficientes campos para evitar errores
    if len(words) > 11:
        # Reconstruimos el texto del agente uniendo desde la palabra 11 al final
        user_agent = " ".join(words[11:])
        
        if "Chrome" in user_agent:
            print("Chrome\t1")
        elif "Firefox" in user_agent:
            print("Firefox\t1")
        elif "Safari" in user_agent:
            print("Safari\t1")
        elif "bot" in user_agent or "Bot" in user_agent:
            print("Bot\t1")
        else:
            print("Otros\t1")
```

    Writing mapper_ej22.py



```python
%%writefile reducer_ej22.py
#!/usr/bin/env python3

import sys

current_browser = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        browser, count = line.split("\t")
        count = int(count)
    except ValueError:
        continue
        
    if current_browser == browser:
        current_count += count
    else:
        if current_browser:
            print(f"{current_browser}: {current_count}")
            
        current_browser = browser
        current_count = count

if current_browser:
    print(f"{current_browser}: {current_count}")
```

    Writing reducer_ej22.py



```python
!cat logfiles_reduced.log | python3 mapper_ej22.py | sort | python3 reducer_ej22.py
```

    Chrome: 33
    Firefox: 8
    Safari: 9


## 3. Análisis temporal y de sesión

### Picos de tráfico por hora

Queremos descubrir a qué hora del día el servidor recibe más carga.

- **Mapper:**
    - Parsea el campo de fecha `[27/Dec/2037:12:00:00 +0530]`.
    - Extrae la hora (`12`).
    - Emite `(hora, 1)`.
- **Reducer:** Suma las peticiones por hora.


```python
%%writefile mapper_ej3.py
#!/usr/bin/env python3

from datetime import datetime
import sys

for line in sys.stdin:
    words = line.strip().split()
    datetime_string = words[3][1:]
    date_time = datetime.strptime(datetime_string, "%d/%b/%Y:%H:%M:%S")
    
    print(f"{date_time.hour}\t1")
```

    Writing mapper_ej3.py



```python
%%writefile reducer_ej3.py
#!/usr/bin/env python3

import sys

current_hour = None
current_count = 0

for line in sys.stdin:
    hour, count = line.strip().split("\t")

    if current_hour == hour:
        current_count += 1
    else:
        if current_hour:
            print(f"{current_hour}: {current_count}")
        
        current_hour = hour
        current_count = 0

print(f"{current_hour}: {current_count}")
```

    Writing reducer_ej3.py



```python
!cat logfiles_reduced.log | python3 mapper_ej3.py | sort | python3 reducer_ej3.py
```

    12: 49


### Tasa de error por endpoint

En este ejercicio queremos descubrir qué URLs están fallando más.

- **Mapper:**
    - Extrae la URL y el código de estado.
    - Si el código es >= 400, emite `(url, "error")`.
    - Si el código es < 400, emite `(url, "ok")`.
    - O mejor: emite `(url, (1, 0))` para éxito y `(url, (0, 1))` para error.
- **Reducer:** Suma totales y errores. Calcula el % de error: `(errores / total) * 100`.


```python
%%writefile mapper_ej31.py
#!/usr/bin/env python3

import sys

for line in sys.stdin:
    words = line.strip().split()
    url, http_code = words[6], int(words[8])

    status = None
    if http_code >= 400:
        status = "0,1"
    elif http_code < 400:
        status = "1,0"
    
    print(f"{url}\t{status}")
```

    Writing mapper_ej31.py



```python
%%writefile reducer_ej31.py
#!/usr/bin/env python3

import sys

# Entrada -> /usr/admin 0,1

current_url = None
total_success = 0
total_errors = 0
error_percent = 0

for line in sys.stdin:
        url, status = line.strip().split("\t") 
        status_success, status_error = status.split(",")

        status_success = int(status_success)
        status_error = int(status_error)

        if current_url == url:
            total_success += status_success
            total_errors += status_error
        else:
            if current_url:
                error_percent = (total_errors / (total_errors + total_success)) * 100
                print(f"{current_url}: {error_percent}%")
            
            current_url = url
            total_success = 0
            total_errors = 0
            error_percent = 0

print(f"{current_url}: {error_percent}%")
```

    Overwriting reducer_ej31.py



```python
!cat logfiles_reduced.log | python3 mapper_ej31.py | sort | python3 reducer_ej31.py
```

    /usr: 27.27272727272727%
    /usr/admin: 44.44444444444444%
    /usr/admin/developer: 66.66666666666666%
    /usr/login: 66.66666666666666%
    /usr/register: 0%



```python

```
