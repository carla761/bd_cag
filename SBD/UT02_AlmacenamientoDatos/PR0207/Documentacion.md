# PR0207: Consultas con Flux


```python
# -------------------------------
# Importación de librerias
# -------------------------------

import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
from influxdb_client import Point , WriteOptions
from datetime import datetime, timezone
import os
import csv


# -------------------------------
# Configuración de InfluxDB
# -------------------------------

INFLUX_URL = "http://influxdb2:8086"
INFLUX_TOKEN = "AdminToken123="
INFLUX_ORG = "docs"
INFLUX_BUCKET = "crypto_raw"

print("--- Iniciando conexión a InfluxDB ---")


client = None
try:
    # 1. Inicializar el cliente y la API de consulta
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )
    print("Conexion exitosa")
    query_api = client.query_api()
except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")
```

    --- Iniciando conexión a InfluxDB ---
    Conexion exitosa


## PARTE I: Consultas de filtrado y estructura

El objetivo es familiarizarse con el inicio de la *pipeline* y el uso de Tags para filtrar.

### Tarea 1.1: Precio de cierre de Bitcoin

Escribe una consulta en Flux que:

1.  Use el bucket **`crypto_raw`**.
2.  Consulte los datos de de diciembre de 2020 (`range`).
3.  Filtre solo el activo **`BTC`** (usando el Tag `symbol`).
4.  Filtre solo el campo **`close`** (usando el Field `_field`).



```python
query = """
from(bucket: "crypto_raw")
  |> range(start: 2020-12-01T00:00:00Z, stop: 2021-01-01T00:00:00Z)
  |> filter(fn: (r) => r.symbol == "BTC")
  |> filter(fn: (r) => r._field == "close")
"""

result = query_api.query(query=query)

for table in result:
    for record in table.records:
        print(
            f"Time: {record.get_time()} | "
            f"Close: {record.get_value()}"
        )

```

    Time: 2020-12-01 23:59:59+00:00 | Close: 18802.99829969
    Time: 2020-12-02 23:59:59+00:00 | Close: 19201.09115697
    Time: 2020-12-03 23:59:59+00:00 | Close: 19445.39847988
    Time: 2020-12-04 23:59:59+00:00 | Close: 18699.76561337
    Time: 2020-12-05 23:59:59+00:00 | Close: 19154.231131
    Time: 2020-12-06 23:59:59+00:00 | Close: 19345.12095871
    Time: 2020-12-07 23:59:59+00:00 | Close: 19191.63128698
    Time: 2020-12-08 23:59:59+00:00 | Close: 18321.14491611
    Time: 2020-12-09 23:59:59+00:00 | Close: 18553.91537685
    Time: 2020-12-10 23:59:59+00:00 | Close: 18264.99210672
    Time: 2020-12-11 23:59:59+00:00 | Close: 18058.90334725
    Time: 2020-12-12 23:59:59+00:00 | Close: 18803.65687045
    Time: 2020-12-13 23:59:59+00:00 | Close: 19142.3825335
    Time: 2020-12-14 23:59:59+00:00 | Close: 19246.64434137
    Time: 2020-12-15 23:59:59+00:00 | Close: 19417.07603342
    Time: 2020-12-16 23:59:59+00:00 | Close: 21310.59813054
    Time: 2020-12-17 23:59:59+00:00 | Close: 22805.16149213
    Time: 2020-12-18 23:59:59+00:00 | Close: 23137.96056165
    Time: 2020-12-19 23:59:59+00:00 | Close: 23869.83196434
    Time: 2020-12-20 23:59:59+00:00 | Close: 23477.29519711
    Time: 2020-12-21 23:59:59+00:00 | Close: 22803.0814087
    Time: 2020-12-22 23:59:59+00:00 | Close: 23783.02850288
    Time: 2020-12-23 23:59:59+00:00 | Close: 23241.34486501
    Time: 2020-12-24 23:59:59+00:00 | Close: 23735.94972763
    Time: 2020-12-25 23:59:59+00:00 | Close: 24664.79027412
    Time: 2020-12-26 23:59:59+00:00 | Close: 26437.0375091
    Time: 2020-12-27 23:59:59+00:00 | Close: 26272.29456706
    Time: 2020-12-28 23:59:59+00:00 | Close: 27084.80788628
    Time: 2020-12-29 23:59:59+00:00 | Close: 27362.4365573
    Time: 2020-12-30 23:59:59+00:00 | Close: 28840.95341968
    Time: 2020-12-31 23:59:59+00:00 | Close: 29001.71982218


### Tarea 1.2: Volumen Total del Ethereum (ETHUSDT)

Escribe una consulta que:

1.  Filtre los datos de **`ETH`** de **enero a junio de 2021**.
2.  Filtre el campo **`volume`**.
3.  Use la función de agregación **`sum()`** para calcular el volumen total de transacciones en ese periodo.



```python
query_1 = """
from(bucket: "crypto_raw")
  |> range(start: 2021-01-01T00:00:00Z, stop: 2021-07-01T00:00:00Z)
  |> filter(fn: (r) => r.symbol == "ETH")
  |> filter(fn: (r) => r._field == "volume")
  |> sum()
"""

result = query_api.query(query=query_1)

for table in result:
    for record in table.records:
        print(
            f"Volumen total ETH: {record.get_value()}"
        )

```

    Volumen total ETH: 6239381609386.877


### PARTE II: Agregación temporal

Aquí se introduce el concepto clave de las series de tiempo: la agregación por ventanas de tiempo.


### Tarea 2.1: Precio promedio mensual

Escribe una consulta que:

1.  Filtre los precios de cierre (`close`) de **`BTC`** de **todo el histórico** disponible.
2.  Use la función **`aggregateWindow()`** para calcular el **precio promedio (`fn: mean`)** por **mes (`every: 1mo`)**.
3.  *Resultado esperado:* Una fila por mes, mostrando la media del precio de cierre de BTC en ese mes.


```python
query_2 = """
from(bucket: "crypto_raw")
  |> range(start: 0)
  |> filter(fn: (r) => r.symbol == "BTC")
  |> filter(fn: (r) => r._field == "close")
  |> aggregateWindow(every: 1mo, fn: mean, createEmpty: false)
"""
result = query_api.query(query=query_2)

for table in result:
    for record in table.records:
        print(
            f"Mes: {record.get_time()} | "
            f"Precio promedio: {record.get_value()}"
        )

```

    Mes: 2013-05-01 00:00:00+00:00 | Precio promedio: 141.7699966430664
    Mes: 2013-06-01 00:00:00+00:00 | Precio promedio: 119.99274124637726
    Mes: 2013-07-01 00:00:00+00:00 | Precio promedio: 107.76140670776367
    Mes: 2013-08-01 00:00:00+00:00 | Precio promedio: 90.512206539031
    Mes: 2013-09-01 00:00:00+00:00 | Precio promedio: 113.90548435334236
    Mes: 2013-10-01 00:00:00+00:00 | Precio promedio: 130.0616668701172
    Mes: 2013-11-01 00:00:00+00:00 | Precio promedio: 158.3119359170237
    Mes: 2013-12-01 00:00:00+00:00 | Precio promedio: 550.420664469401
    Mes: 2014-01-01 00:00:00+00:00 | Precio promedio: 800.7809664818549
    Mes: 2014-02-01 00:00:00+00:00 | Precio promedio: 844.1683900894657
    Mes: 2014-03-01 00:00:00+00:00 | Precio promedio: 661.6182163783482
    Mes: 2014-04-01 00:00:00+00:00 | Precio promedio: 592.2003843245968
    Mes: 2014-05-01 00:00:00+00:00 | Precio promedio: 461.36180216471354
    Mes: 2014-06-01 00:00:00+00:00 | Precio promedio: 486.6520031344506
    Mes: 2014-07-01 00:00:00+00:00 | Precio promedio: 615.916737874349
    Mes: 2014-08-01 00:00:00+00:00 | Precio promedio: 618.0250637915826
    Mes: 2014-09-01 00:00:00+00:00 | Precio promedio: 536.0873924993699
    Mes: 2014-10-01 00:00:00+00:00 | Precio promedio: 445.1866007486979
    Mes: 2014-11-01 00:00:00+00:00 | Precio promedio: 364.1488726215978
    Mes: 2014-12-01 00:00:00+00:00 | Precio promedio: 366.09979858398435
    Mes: 2015-01-01 00:00:00+00:00 | Precio promedio: 341.2678705030872
    Mes: 2015-02-01 00:00:00+00:00 | Precio promedio: 248.78254748928933
    Mes: 2015-03-01 00:00:00+00:00 | Precio promedio: 234.15364456176758
    Mes: 2015-04-01 00:00:00+00:00 | Precio promedio: 269.0422589701991
    Mes: 2015-05-01 00:00:00+00:00 | Precio promedio: 235.4915339152018
    Mes: 2015-06-01 00:00:00+00:00 | Precio promedio: 236.9970009096207
    Mes: 2015-07-01 00:00:00+00:00 | Precio promedio: 238.0817657470703
    Mes: 2015-08-01 00:00:00+00:00 | Precio promedio: 279.5637398996661
    Mes: 2015-09-01 00:00:00+00:00 | Precio promedio: 250.73380501039566
    Mes: 2015-10-01 00:00:00+00:00 | Precio promedio: 233.5955332438151
    Mes: 2015-11-01 00:00:00+00:00 | Precio promedio: 264.85535553962956
    Mes: 2015-12-01 00:00:00+00:00 | Precio promedio: 348.8833323160807
    Mes: 2016-01-01 00:00:00+00:00 | Precio promedio: 424.4645474341608
    Mes: 2016-02-01 00:00:00+00:00 | Precio promedio: 410.84448537518904
    Mes: 2016-03-01 00:00:00+00:00 | Precio promedio: 404.4082736311288
    Mes: 2016-04-01 00:00:00+00:00 | Precio promedio: 416.5257735713836
    Mes: 2016-05-01 00:00:00+00:00 | Precio promedio: 434.3393981933594
    Mes: 2016-06-01 00:00:00+00:00 | Precio promedio: 461.9544146137853
    Mes: 2016-07-01 00:00:00+00:00 | Precio promedio: 642.8690612792968
    Mes: 2016-08-01 00:00:00+00:00 | Precio promedio: 661.3561027280746
    Mes: 2016-09-01 00:00:00+00:00 | Precio promedio: 579.585197202621
    Mes: 2016-10-01 00:00:00+00:00 | Precio promedio: 605.8486328125
    Mes: 2016-11-01 00:00:00+00:00 | Precio promedio: 643.5509348223286
    Mes: 2016-12-01 00:00:00+00:00 | Precio promedio: 726.3491007486979
    Mes: 2017-01-01 00:00:00+00:00 | Precio promedio: 828.0603558940272
    Mes: 2017-02-01 00:00:00+00:00 | Precio promedio: 914.9161593529486
    Mes: 2017-03-01 00:00:00+00:00 | Precio promedio: 1062.533671787807
    Mes: 2017-04-01 00:00:00+00:00 | Precio promedio: 1129.365228468372
    Mes: 2017-05-01 00:00:00+00:00 | Precio promedio: 1206.641007486979
    Mes: 2017-06-01 00:00:00+00:00 | Precio promedio: 1895.383529170867
    Mes: 2017-07-01 00:00:00+00:00 | Precio promedio: 2636.204345703125
    Mes: 2017-08-01 00:00:00+00:00 | Precio promedio: 2519.4183861517135
    Mes: 2017-09-01 00:00:00+00:00 | Precio promedio: 3880.9899981098793
    Mes: 2017-10-01 00:00:00+00:00 | Precio promedio: 4064.8363118489583
    Mes: 2017-11-01 00:00:00+00:00 | Precio promedio: 5360.071604082661
    Mes: 2017-12-01 00:00:00+00:00 | Precio promedio: 7813.132975260417
    Mes: 2018-01-01 00:00:00+00:00 | Precio promedio: 15294.270980342742
    Mes: 2018-02-01 00:00:00+00:00 | Precio promedio: 13085.558089717742
    Mes: 2018-03-01 00:00:00+00:00 | Precio promedio: 9472.001150948661
    Mes: 2018-04-01 00:00:00+00:00 | Precio promedio: 9040.557097404233
    Mes: 2018-05-01 00:00:00+00:00 | Precio promedio: 8033.596630859375
    Mes: 2018-06-01 00:00:00+00:00 | Precio promedio: 8450.997731854839
    Mes: 2018-07-01 00:00:00+00:00 | Precio promedio: 6793.507666015625
    Mes: 2018-08-01 00:00:00+00:00 | Precio promedio: 7146.349989919355
    Mes: 2018-09-01 00:00:00+00:00 | Precio promedio: 6700.130000000002
    Mes: 2018-10-01 00:00:00+00:00 | Precio promedio: 6610.675000000001
    Mes: 2018-11-01 00:00:00+00:00 | Precio promedio: 6485.118709677419
    Mes: 2018-12-01 00:00:00+00:00 | Precio promedio: 5404.250163745335
    Mes: 2019-01-01 00:00:00+00:00 | Precio promedio: 3717.4883192654843
    Mes: 2019-02-01 00:00:00+00:00 | Precio promedio: 3701.5549733116122
    Mes: 2019-03-01 00:00:00+00:00 | Precio promedio: 3711.907275630714
    Mes: 2019-04-01 00:00:00+00:00 | Precio promedio: 3976.0690934074196
    Mes: 2019-05-01 00:00:00+00:00 | Precio promedio: 5178.469425008667
    Mes: 2019-06-01 00:00:00+00:00 | Precio promedio: 7309.694113368711
    Mes: 2019-07-01 00:00:00+00:00 | Precio promedio: 9415.900143546
    Mes: 2019-08-01 00:00:00+00:00 | Precio promedio: 10669.33622277516
    Mes: 2019-09-01 00:00:00+00:00 | Precio promedio: 10643.24839313613
    Mes: 2019-10-01 00:00:00+00:00 | Precio promedio: 9814.067782100668
    Mes: 2019-11-01 00:00:00+00:00 | Precio promedio: 8411.929149071937
    Mes: 2019-12-01 00:00:00+00:00 | Precio promedio: 8373.572452042665
    Mes: 2020-01-01 00:00:00+00:00 | Precio promedio: 7284.0130458951635
    Mes: 2020-02-01 00:00:00+00:00 | Precio promedio: 8389.270450449678
    Mes: 2020-03-01 00:00:00+00:00 | Precio promedio: 9630.722210922067
    Mes: 2020-04-01 00:00:00+00:00 | Precio promedio: 6871.016110927743
    Mes: 2020-05-01 00:00:00+00:00 | Precio promedio: 7224.477345241333
    Mes: 2020-06-01 00:00:00+00:00 | Precio promedio: 9263.151880502257
    Mes: 2020-07-01 00:00:00+00:00 | Precio promedio: 9489.227163164333
    Mes: 2020-08-01 00:00:00+00:00 | Precio promedio: 9589.899754957421
    Mes: 2020-09-01 00:00:00+00:00 | Precio promedio: 11652.394214906453
    Mes: 2020-10-01 00:00:00+00:00 | Precio promedio: 10660.276814935667
    Mes: 2020-11-01 00:00:00+00:00 | Precio promedio: 11886.978148203545
    Mes: 2020-12-01 00:00:00+00:00 | Precio promedio: 16645.757397035995
    Mes: 2021-01-01 00:00:00+00:00 | Precio promedio: 21983.13691412839
    Mes: 2021-02-01 00:00:00+00:00 | Precio promedio: 34761.6498821042
    Mes: 2021-03-01 00:00:00+00:00 | Precio promedio: 46306.798799221775
    Mes: 2021-04-01 00:00:00+00:00 | Precio promedio: 54998.00857016419
    Mes: 2021-05-01 00:00:00+00:00 | Precio promedio: 57206.72022674067
    Mes: 2021-06-01 00:00:00+00:00 | Precio promedio: 46443.28605283192
    Mes: 2021-07-01 00:00:00+00:00 | Precio promedio: 35845.15485565401
    Mes: 2021-08-01 00:00:00+00:00 | Precio promedio: 34234.44838624
    Mes: 2026-01-01 00:00:00+00:00 | Precio promedio: 4938.123220062238


#### Tarea 2.2: Rango de volatilidad

Calcula el precio máximo y mínimo por semana para la criptomoneda **`Stellar`**.

1.  Filtra los precios de cierre de **`XLM`** del **año 2019**.
2.  Usa `aggregateWindow()` dos veces (o una vez con dos funciones):
    - Una *pipeline* para calcular el **máximo semanal** (`fn: max`, `every: 1wk`).
    - Una *pipeline* para calcular el **mínimo semanal** (`fn: min`, `every: 1wk`).
3.  Usa `yield()` para emitir ambos resultados.



```python
query_3 = """
// Máximo semanal
max_values = 
    from(bucket: "crypto_raw")
        |> range(start: 2019-01-01T00:00:00Z, stop: 2020-01-01T00:00:00Z)
        |> filter(fn: (r) => r.symbol == "XLM")
        |> filter(fn: (r) => r._field == "close")
        |> aggregateWindow(every: 1w, fn: max, createEmpty: false)
        |> yield(name: "max_semanal")

// Mínimo semanal
min_values = 
    from(bucket: "crypto_raw")
        |> range(start: 2019-01-01T00:00:00Z, stop: 2020-01-01T00:00:00Z)
        |> filter(fn: (r) => r.symbol == "XLM")
        |> filter(fn: (r) => r._field == "close")
        |> aggregateWindow(every: 1w, fn: min, createEmpty: false)
        |> yield(name: "min_semanal")
"""

result = query_api.query(query=query_3)

for table in result:
    print("---- TABLA ----")
    for record in table.records:
        print(
            f"Semana: {record.get_time()} | "
            f"Valor: {record.get_value()}"
        )


```

    ---- TABLA ----
    Semana: 2019-01-03 00:00:00+00:00 | Valor: 0.11593003965
    Semana: 2019-01-10 00:00:00+00:00 | Valor: 0.113824645405
    Semana: 2019-01-17 00:00:00+00:00 | Valor: 0.103608750666
    Semana: 2019-01-24 00:00:00+00:00 | Valor: 0.102576372742
    Semana: 2019-01-31 00:00:00+00:00 | Valor: 0.0839227197999
    Semana: 2019-02-07 00:00:00+00:00 | Valor: 0.0743873347098
    Semana: 2019-02-14 00:00:00+00:00 | Valor: 0.0746880850898
    Semana: 2019-02-21 00:00:00+00:00 | Valor: 0.076635145311
    Semana: 2019-02-28 00:00:00+00:00 | Valor: 0.0842337176392
    Semana: 2019-03-07 00:00:00+00:00 | Valor: 0.0835385127758
    Semana: 2019-03-14 00:00:00+00:00 | Valor: 0.0855406472047
    Semana: 2019-03-21 00:00:00+00:00 | Valor: 0.107271925309
    Semana: 2019-03-28 00:00:00+00:00 | Valor: 0.102469191942
    Semana: 2019-04-04 00:00:00+00:00 | Valor: 0.107359387845
    Semana: 2019-04-11 00:00:00+00:00 | Valor: 0.11878829353
    Semana: 2019-04-18 00:00:00+00:00 | Valor: 0.113628616719
    Semana: 2019-04-25 00:00:00+00:00 | Valor: 0.103259281028
    Semana: 2019-05-02 00:00:00+00:00 | Valor: 0.0964745129392
    Semana: 2019-05-09 00:00:00+00:00 | Valor: 0.0936971600069
    Semana: 2019-05-16 00:00:00+00:00 | Valor: 0.0902320403193
    Semana: 2019-05-23 00:00:00+00:00 | Valor: 0.124257250797
    Semana: 2019-05-30 00:00:00+00:00 | Valor: 0.125166646196
    Semana: 2019-06-06 00:00:00+00:00 | Valor: 0.121283780398
    Semana: 2019-06-13 00:00:00+00:00 | Valor: 0.119915400277
    Semana: 2019-06-20 00:00:00+00:00 | Valor: 0.124301592251
    Semana: 2019-06-27 00:00:00+00:00 | Valor: 0.12150678527
    Semana: 2019-07-04 00:00:00+00:00 | Valor: 0.103390157874
    Semana: 2019-07-11 00:00:00+00:00 | Valor: 0.0950565703023
    Semana: 2019-07-18 00:00:00+00:00 | Valor: 0.0783180471619
    Semana: 2019-07-25 00:00:00+00:00 | Valor: 0.084467858308
    Semana: 2019-08-01 00:00:00+00:00 | Valor: 0.083512564551
    Semana: 2019-08-08 00:00:00+00:00 | Valor: 0.0782121757967
    Semana: 2019-08-15 00:00:00+00:00 | Valor: 0.0691830893629
    Semana: 2019-08-22 00:00:00+00:00 | Valor: 0.0676973150428
    Semana: 2019-08-29 00:00:00+00:00 | Valor: 0.0661375592649
    Semana: 2019-09-05 00:00:00+00:00 | Valor: 0.0621784173174
    Semana: 2019-09-12 00:00:00+00:00 | Valor: 0.0583726083727
    Semana: 2019-09-19 00:00:00+00:00 | Valor: 0.0569399656847
    Semana: 2019-09-26 00:00:00+00:00 | Valor: 0.0545038067121
    Semana: 2019-10-03 00:00:00+00:00 | Valor: 0.0581272753922
    Semana: 2019-10-10 00:00:00+00:00 | Valor: 0.0588752275909
    Semana: 2019-10-17 00:00:00+00:00 | Valor: 0.0596294085884
    Semana: 2019-10-24 00:00:00+00:00 | Valor: 0.0599839569322
    Semana: 2019-10-31 00:00:00+00:00 | Valor: 0.0606116062591
    Semana: 2019-11-07 00:00:00+00:00 | Valor: 0.0652148662313
    Semana: 2019-11-14 00:00:00+00:00 | Valor: 0.071887807681
    Semana: 2019-11-21 00:00:00+00:00 | Valor: 0.0655019886487
    Semana: 2019-11-28 00:00:00+00:00 | Valor: 0.0568813691786
    Semana: 2019-12-05 00:00:00+00:00 | Valor: 0.0554190238714
    Semana: 2019-12-12 00:00:00+00:00 | Valor: 0.0526917948915
    Semana: 2019-12-19 00:00:00+00:00 | Valor: 0.0440530520227
    Semana: 2019-12-26 00:00:00+00:00 | Valor: 0.0434406551581
    Semana: 2020-01-01 00:00:00+00:00 | Valor: 0.0451006564413
    ---- TABLA ----
    Semana: 2019-01-03 00:00:00+00:00 | Valor: 0.119331410154
    Semana: 2019-01-10 00:00:00+00:00 | Valor: 0.123774386729
    Semana: 2019-01-17 00:00:00+00:00 | Valor: 0.109878610051
    Semana: 2019-01-24 00:00:00+00:00 | Valor: 0.108460938657
    Semana: 2019-01-31 00:00:00+00:00 | Valor: 0.102210392352
    Semana: 2019-02-07 00:00:00+00:00 | Valor: 0.0835802499476
    Semana: 2019-02-14 00:00:00+00:00 | Valor: 0.081224003372
    Semana: 2019-02-21 00:00:00+00:00 | Valor: 0.0917350058181
    Semana: 2019-02-28 00:00:00+00:00 | Valor: 0.0942568445555
    Semana: 2019-03-07 00:00:00+00:00 | Valor: 0.0872353323243
    Semana: 2019-03-14 00:00:00+00:00 | Valor: 0.108198619481
    Semana: 2019-03-21 00:00:00+00:00 | Valor: 0.115914392752
    Semana: 2019-03-28 00:00:00+00:00 | Valor: 0.108692806617
    Semana: 2019-04-04 00:00:00+00:00 | Valor: 0.121900837603
    Semana: 2019-04-11 00:00:00+00:00 | Valor: 0.131995967869
    Semana: 2019-04-18 00:00:00+00:00 | Valor: 0.117505252017
    Semana: 2019-04-25 00:00:00+00:00 | Valor: 0.117362975895
    Semana: 2019-05-02 00:00:00+00:00 | Valor: 0.101351137089
    Semana: 2019-05-09 00:00:00+00:00 | Valor: 0.102295013854
    Semana: 2019-05-16 00:00:00+00:00 | Valor: 0.137001655066
    Semana: 2019-05-23 00:00:00+00:00 | Valor: 0.141485197931
    Semana: 2019-05-30 00:00:00+00:00 | Valor: 0.138959876059
    Semana: 2019-06-06 00:00:00+00:00 | Valor: 0.137622959913
    Semana: 2019-06-13 00:00:00+00:00 | Valor: 0.127541536282
    Semana: 2019-06-20 00:00:00+00:00 | Valor: 0.131035168284
    Semana: 2019-06-27 00:00:00+00:00 | Valor: 0.129050324633
    Semana: 2019-07-04 00:00:00+00:00 | Valor: 0.114503902451
    Semana: 2019-07-11 00:00:00+00:00 | Valor: 0.105053888576
    Semana: 2019-07-18 00:00:00+00:00 | Valor: 0.0979634554654
    Semana: 2019-07-25 00:00:00+00:00 | Valor: 0.0951105058824
    Semana: 2019-08-01 00:00:00+00:00 | Valor: 0.0879653185781
    Semana: 2019-08-08 00:00:00+00:00 | Valor: 0.0830260889325
    Semana: 2019-08-15 00:00:00+00:00 | Valor: 0.077841261029
    Semana: 2019-08-22 00:00:00+00:00 | Valor: 0.0717945667003
    Semana: 2019-08-29 00:00:00+00:00 | Valor: 0.0716762386253
    Semana: 2019-09-05 00:00:00+00:00 | Valor: 0.063233045025
    Semana: 2019-09-12 00:00:00+00:00 | Valor: 0.0608816630268
    Semana: 2019-09-19 00:00:00+00:00 | Valor: 0.0831183072597
    Semana: 2019-09-26 00:00:00+00:00 | Valor: 0.0813871907299
    Semana: 2019-10-03 00:00:00+00:00 | Valor: 0.0614401007616
    Semana: 2019-10-10 00:00:00+00:00 | Valor: 0.0633552899625
    Semana: 2019-10-17 00:00:00+00:00 | Valor: 0.064924881188
    Semana: 2019-10-24 00:00:00+00:00 | Valor: 0.0645472454791
    Semana: 2019-10-31 00:00:00+00:00 | Valor: 0.0661851181536
    Semana: 2019-11-07 00:00:00+00:00 | Valor: 0.082164007855
    Semana: 2019-11-14 00:00:00+00:00 | Valor: 0.0798086163683
    Semana: 2019-11-21 00:00:00+00:00 | Valor: 0.074740405351
    Semana: 2019-11-28 00:00:00+00:00 | Valor: 0.0616827581745
    Semana: 2019-12-05 00:00:00+00:00 | Valor: 0.0596409680538
    Semana: 2019-12-12 00:00:00+00:00 | Valor: 0.0561321294528
    Semana: 2019-12-19 00:00:00+00:00 | Valor: 0.0529900639054
    Semana: 2019-12-26 00:00:00+00:00 | Valor: 0.0472958798315
    Semana: 2020-01-01 00:00:00+00:00 | Valor: 0.0462155943798


## PARTE III: Manipulación y Joins

Estas tareas requieren transformar los datos o combinar información de diferentes series de tiempo.

### Tarea 3.1: Cálculo de variación porcentual diaria (Map)

Escribe una consulta que:

1.  Filtre los precios de cierre (`close`) de **Tether ()`USDT`)** de los **años 2016 a 2018**.
2.  Usa la función **`difference()`** para obtener la diferencia absoluta (en dólares) entre los precios de cierre diarios.
3.  Usa la función **`map()`** para transformar el resultado anterior y calcular la **variación porcentual diaria** (Diferencia / Precio del día anterior).



```python
query_4 = """
from(bucket: "crypto_raw")
  |> range(start: 2016-01-01T00:00:00Z, stop: 2018-01-01T00:00:00Z)
  |> filter(fn: (r) => r.symbol == "USDT")
  |> filter(fn: (r) => r._field == "close")
  |> difference()
"""

result = query_api.query(query=query_4)

prev_price = None

for table in result:
    for record in table.records:
        price = record.get_value()

        if prev_price is None:
            prev_price = price
            continue

        if prev_price == 0:
            prev_price = price
            continue

        pct = (price - prev_price) / prev_price

        print(
            f"Fecha: {record.get_time()} | "
            f"Precio: {price} | "
            f"Variación %: {pct}"
        )

        prev_price = price

```

    Fecha: 2016-01-06 23:59:59+00:00 | Precio: -0.0002499818801879883 | Variación %: -2.0
    Fecha: 2016-01-07 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-01-14 23:59:59+00:00 | Precio: -0.0004500150680541992 | Variación %: -2.0
    Fecha: 2016-01-15 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-01-17 23:59:59+00:00 | Precio: -0.0004099607467651367 | Variación %: -2.0
    Fecha: 2016-01-18 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-01-23 23:59:59+00:00 | Precio: 7.998943328857422e-05 | Variación %: 0.14310051107325383
    Fecha: 2016-01-24 23:59:59+00:00 | Precio: -0.0001399517059326172 | Variación %: -2.7496274217585692
    Fecha: 2016-01-25 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-01-27 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-01-29 23:59:59+00:00 | Precio: -2.09808349609375e-05 | Variación %: 19.705882352941178
    Fecha: 2016-01-30 23:59:59+00:00 | Precio: 2.199411392211914e-05 | Variación %: -2.0482954545454546
    Fecha: 2016-01-31 23:59:59+00:00 | Precio: -1.0132789611816406e-06 | Variación %: -1.046070460704607
    Fecha: 2016-02-01 23:59:59+00:00 | Precio: -2.9981136322021484e-05 | Variación %: 28.58823529411765
    Fecha: 2016-02-02 23:59:59+00:00 | Precio: 3.0994415283203125e-05 | Variación %: -2.033797216699801
    Fecha: 2016-02-03 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-02-15 23:59:59+00:00 | Precio: -0.0008800029754638672 | Variación %: -1.988748995446022
    Fecha: 2016-02-16 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-02-18 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-02-25 23:59:59+00:00 | Precio: 0.00015598535537719727 | Variación %: -2.0
    Fecha: 2016-02-26 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-01 23:59:59+00:00 | Precio: -2.9027462005615234e-05 | Variación %: -2.449404761904762
    Fecha: 2016-03-02 23:59:59+00:00 | Precio: -2.9027462005615234e-05 | Variación %: -0.0
    Fecha: 2016-03-03 23:59:59+00:00 | Precio: 3.701448440551758e-05 | Variación %: -2.2751540041067764
    Fecha: 2016-03-04 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -0.9726247987117552
    Fecha: 2016-03-05 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-07 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-09 23:59:59+00:00 | Precio: -0.00010502338409423828 | Variación %: -52.8235294117647
    Fecha: 2016-03-10 23:59:59+00:00 | Precio: 9.900331497192383e-05 | Variación %: -1.9426787741203178
    Fecha: 2016-03-11 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -0.9897652016857315
    Fecha: 2016-03-12 23:59:59+00:00 | Precio: -0.00010001659393310547 | Variación %: -99.70588235294117
    Fecha: 2016-03-13 23:59:59+00:00 | Precio: 2.300739288330078e-05 | Variación %: -1.2300357568533968
    Fecha: 2016-03-14 23:59:59+00:00 | Precio: 7.599592208862305e-05 | Variación %: 2.3031088082901556
    Fecha: 2016-03-15 23:59:59+00:00 | Precio: 6.020069122314453e-06 | Variación %: -0.9207843137254902
    Fecha: 2016-03-16 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-18 23:59:59+00:00 | Precio: 1.4960765838623047e-05 | Variación %: -1.880701754385965
    Fecha: 2016-03-19 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-22 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-03-25 23:59:59+00:00 | Precio: 2.8014183044433594e-05 | Variación %: -2.0375275938189845
    Fecha: 2016-03-26 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-04-07 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-04-09 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-04-12 23:59:59+00:00 | Precio: 0.00013899803161621094 | Variación %: -2.0
    Fecha: 2016-04-13 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-05-14 23:59:59+00:00 | Precio: 0.0003199577331542969 | Variación %: -0.9018539510732438
    Fecha: 2016-05-15 23:59:59+00:00 | Precio: -0.0035799741744995117 | Variación %: -12.188897168405365
    Fecha: 2016-05-16 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-05-25 23:59:59+00:00 | Precio: -2.002716064453125e-05 | Variación %: -2.0
    Fecha: 2016-05-26 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-06-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-06-21 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-06-25 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-06-28 23:59:59+00:00 | Precio: 4.8995018005371094e-05 | Variación %: -1.8303030303030303
    Fecha: 2016-06-29 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-07-08 23:59:59+00:00 | Precio: 7.987022399902344e-06 | Variación %: -1.8874172185430464
    Fecha: 2016-07-09 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-07-12 23:59:59+00:00 | Precio: -0.00015997886657714844 | Variación %: -1.9937060348019253
    Fecha: 2016-07-13 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-07-20 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -2.0
    Fecha: 2016-07-21 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-07-26 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -2.0
    Fecha: 2016-07-27 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-07-30 23:59:59+00:00 | Precio: -6.99758529663086e-05 | Variación %: -1.8748137108792846
    Fecha: 2016-07-31 23:59:59+00:00 | Precio: -4.70280647277832e-05 | Variación %: -0.32793867120954
    Fecha: 2016-08-01 23:59:59+00:00 | Precio: 3.600120544433594e-05 | Variación %: -1.7655259822560203
    Fecha: 2016-08-02 23:59:59+00:00 | Precio: -3.993511199951172e-06 | Variación %: -1.1109271523178808
    Fecha: 2016-08-03 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -1.2537313432835822
    Fecha: 2016-08-04 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-08-06 23:59:59+00:00 | Precio: -0.0002759695053100586 | Variación %: 0.6928702010968921
    Fecha: 2016-08-07 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-08-11 23:59:59+00:00 | Precio: -0.011184990406036377 | Variación %: -0.569759123987179
    Fecha: 2016-08-12 23:59:59+00:00 | Precio: -0.00031697750091552734 | Variación %: -0.9716604583992795
    Fecha: 2016-08-13 23:59:59+00:00 | Precio: 0.03794097900390625 | Variación %: -120.69612636329447
    Fecha: 2016-08-14 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-08-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-09-13 23:59:59+00:00 | Precio: -0.0006899833679199219 | Variación %: -1.9856948228882834
    Fecha: 2016-09-14 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.9854872149274361
    Fecha: 2016-09-15 23:59:59+00:00 | Precio: -6.973743438720703e-06 | Variación %: -0.30357142857142855
    Fecha: 2016-09-16 23:59:59+00:00 | Precio: 5.9604644775390625e-06 | Variación %: -1.8547008547008548
    Fecha: 2016-09-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-09-19 23:59:59+00:00 | Precio: 7.599592208862305e-05 | Variación %: -2.0
    Fecha: 2016-09-20 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-09-22 23:59:59+00:00 | Precio: 1.0967254638671875e-05 | Variación %: -2.0
    Fecha: 2016-09-23 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-09-26 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-10-03 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-10-05 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-10-15 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -2.0
    Fecha: 2016-10-16 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-11-11 23:59:59+00:00 | Precio: 2.9802322387695312e-06 | Variación %: -2.0
    Fecha: 2016-11-12 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-12-04 23:59:59+00:00 | Precio: 0.00015997886657714844 | Variación %: 6.988095238095238
    Fecha: 2016-12-05 23:59:59+00:00 | Precio: -0.00015997886657714844 | Variación %: -2.0
    Fecha: 2016-12-06 23:59:59+00:00 | Precio: -2.002716064453125e-05 | Variación %: -0.8748137108792846
    Fecha: 2016-12-07 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-12-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-12-19 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.5
    Fecha: 2016-12-20 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-12-24 23:59:59+00:00 | Precio: -0.00015997886657714844 | Variación %: -1.94109396914446
    Fecha: 2016-12-25 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2016-12-29 23:59:59+00:00 | Precio: -2.002716064453125e-05 | Variación %: -1.6666666666666667
    Fecha: 2016-12-30 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-01-01 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-01-15 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -1.5
    Fecha: 2017-01-16 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.0
    Fecha: 2017-01-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-01-31 23:59:59+00:00 | Precio: -0.0003229379653930664 | Variación %: -2.041923076923077
    Fecha: 2017-02-01 23:59:59+00:00 | Precio: 1.9669532775878906e-06 | Variación %: -1.0060908084163898
    Fecha: 2017-02-02 23:59:59+00:00 | Precio: -5.0067901611328125e-06 | Variación %: -3.5454545454545454
    Fecha: 2017-02-03 23:59:59+00:00 | Precio: 3.993511199951172e-06 | Variación %: -1.7976190476190477
    Fecha: 2017-02-04 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -0.746268656716418
    Fecha: 2017-02-05 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-02-07 23:59:59+00:00 | Precio: 1.0132789611816406e-06 | Variación %: -2.0
    Fecha: 2017-02-08 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-02-14 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-02-16 23:59:59+00:00 | Precio: -0.0017200708389282227 | Variación %: -1.9717807112068966
    Fecha: 2017-02-17 23:59:59+00:00 | Precio: -2.9921531677246094e-05 | Variación %: -0.9826044770947397
    Fecha: 2017-02-18 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.6653386454183267
    Fecha: 2017-02-19 23:59:59+00:00 | Precio: -0.00011199712753295898 | Variación %: 10.18452380952381
    Fecha: 2017-02-20 23:59:59+00:00 | Precio: 9.900331497192383e-05 | Variación %: -1.8839808408728047
    Fecha: 2017-02-21 23:59:59+00:00 | Precio: -0.00023704767227172852 | Variación %: -3.3943407585791694
    Fecha: 2017-02-22 23:59:59+00:00 | Precio: 0.00020700693130493164 | Variación %: -1.8732713100326879
    Fecha: 2017-02-23 23:59:59+00:00 | Precio: 3.0040740966796875e-05 | Variación %: -0.8548805067664843
    Fecha: 2017-02-24 23:59:59+00:00 | Precio: 9.5367431640625e-07 | Variación %: -0.9682539682539683
    Fecha: 2017-02-25 23:59:59+00:00 | Precio: 4.208087921142578e-05 | Variación %: 43.125
    Fecha: 2017-02-26 23:59:59+00:00 | Precio: -3.0040740966796875e-05 | Variación %: -1.7138810198300283
    Fecha: 2017-02-27 23:59:59+00:00 | Precio: 5.996227264404297e-05 | Variación %: -2.996031746031746
    Fecha: 2017-02-28 23:59:59+00:00 | Precio: -9.995698928833008e-05 | Variación %: -2.6669980119284293
    Fecha: 2017-03-01 23:59:59+00:00 | Precio: 2.7954578399658203e-05 | Variación %: -1.2796660703637448
    Fecha: 2017-03-02 23:59:59+00:00 | Precio: 2.0265579223632812e-06 | Variación %: -0.9275053304904051
    Fecha: 2017-03-03 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-03-05 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-03-07 23:59:59+00:00 | Precio: -3.993511199951172e-05 | Variación %: -1.7995226730310263
    Fecha: 2017-03-08 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.7492537313432835
    Fecha: 2017-03-09 23:59:59+00:00 | Precio: -0.00010401010513305664 | Variación %: 9.386904761904763
    Fecha: 2017-03-10 23:59:59+00:00 | Precio: 8.398294448852539e-05 | Variación %: -1.8074498567335244
    Fecha: 2017-03-11 23:59:59+00:00 | Precio: 5.0067901611328125e-05 | Variación %: -0.4038325053229241
    Fecha: 2017-03-12 23:59:59+00:00 | Precio: 3.993511199951172e-05 | Variación %: -0.20238095238095238
    Fecha: 2017-03-13 23:59:59+00:00 | Precio: -3.993511199951172e-05 | Variación %: -2.0
    Fecha: 2017-03-14 23:59:59+00:00 | Precio: -2.002716064453125e-05 | Variación %: -0.49850746268656715
    Fecha: 2017-03-15 23:59:59+00:00 | Precio: -1.0013580322265625e-05 | Variación %: -0.5
    Fecha: 2017-03-16 23:59:59+00:00 | Precio: 2.002716064453125e-05 | Variación %: -3.0
    Fecha: 2017-03-17 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-03-20 23:59:59+00:00 | Precio: 0.00016009807586669922 | Variación %: 7.041916167664671
    Fecha: 2017-03-21 23:59:59+00:00 | Precio: -0.0001800060272216797 | Variación %: -2.124348473566642
    Fecha: 2017-03-22 23:59:59+00:00 | Precio: 1.0013580322265625e-05 | Variación %: -1.0556291390728476
    Fecha: 2017-03-23 23:59:59+00:00 | Precio: 2.9921531677246094e-05 | Variación %: 1.9880952380952381
    Fecha: 2017-03-24 23:59:59+00:00 | Precio: -0.00017398595809936523 | Variación %: -6.814741035856573
    Fecha: 2017-03-25 23:59:59+00:00 | Precio: 2.002716064453125e-05 | Variación %: -1.1151079136690647
    Fecha: 2017-03-26 23:59:59+00:00 | Precio: 9.399652481079102e-05 | Variación %: 3.693452380952381
    Fecha: 2017-03-27 23:59:59+00:00 | Precio: 0.0 | Variación %: -1.0
    Fecha: 2017-03-30 23:59:59+00:00 | Precio: 3.898143768310547e-05 | Variación %: -1.618732261116367
    Fecha: 2017-03-31 23:59:59+00:00 | Precio: 1.4007091522216797e-05 | Variación %: -0.6406727828746177
    Fecha: 2017-04-01 23:59:59+00:00 | Precio: -0.0004140138626098633 | Variación %: -30.557446808510637
    Fecha: 2017-04-02 23:59:59+00:00 | Precio: 0.001363992691040039 | Variación %: -4.294558019003743
    Fecha: 2017-04-03 23:59:59+00:00 | Precio: -0.0011979937553405762 | Variación %: -1.8782992483831498
    Fecha: 2017-04-04 23:59:59+00:00 | Precio: 0.00026804208755493164 | Variación %: -1.2237424747499877
    Fecha: 2017-04-05 23:59:59+00:00 | Precio: 9.000301361083984e-05 | Variación %: -0.6642205915054481
    Fecha: 2017-04-06 23:59:59+00:00 | Precio: -0.0001710057258605957 | Variación %: -2.9
    Fecha: 2017-04-07 23:59:59+00:00 | Precio: -6.604194641113281e-05 | Variación %: -0.6138027187173231
    Fecha: 2017-04-08 23:59:59+00:00 | Precio: -0.0001569986343383789 | Variación %: 1.3772563176895307
    Fecha: 2017-04-09 23:59:59+00:00 | Precio: 0.00024402141571044922 | Variación %: -2.554290053151101
    Fecha: 2017-04-10 23:59:59+00:00 | Precio: -2.9027462005615234e-05 | Variación %: -1.1189545676599901
    Fecha: 2017-04-11 23:59:59+00:00 | Precio: -8.797645568847656e-05 | Variación %: 2.030800821355236
    Fecha: 2017-04-12 23:59:59+00:00 | Precio: -0.0002809762954711914 | Variación %: 2.193766937669377
    Fecha: 2017-04-13 23:59:59+00:00 | Precio: 4.9948692321777344e-05 | Variación %: -1.1777683495969453
    Fecha: 2017-04-14 23:59:59+00:00 | Precio: -0.0006259679794311523 | Variación %: -13.532219570405728
    Fecha: 2017-04-15 23:59:59+00:00 | Precio: 0.0009530186653137207 | Variación %: -2.5224719101123596
    Fecha: 2017-04-16 23:59:59+00:00 | Precio: -0.00048100948333740234 | Variación %: -1.504721996372506
    Fecha: 2017-04-17 23:59:59+00:00 | Precio: -0.00016999244689941406 | Variación %: -0.6465923172242874
    Fecha: 2017-04-18 23:59:59+00:00 | Precio: 0.0003280043601989746 | Variación %: -2.929523141654979
    Fecha: 2017-04-19 23:59:59+00:00 | Precio: -9.304285049438477e-05 | Variación %: -1.2836634562965654
    Fecha: 2017-04-20 23:59:59+00:00 | Precio: -0.001248002052307129 | Variación %: 12.41319666880205
    Fecha: 2017-04-21 23:59:59+00:00 | Precio: -0.01410597562789917 | Variación %: 10.30284649918808
    Fecha: 2017-04-22 23:59:59+00:00 | Precio: -0.0432400107383728 | Variación %: 2.0653683147482242
    Fecha: 2017-04-23 23:59:59+00:00 | Precio: -0.019595980644226074 | Variación %: -0.5468090708211627
    Fecha: 2017-04-24 23:59:59+00:00 | Precio: -0.003443002700805664 | Variación %: -0.8243005663602684
    Fecha: 2017-04-25 23:59:59+00:00 | Precio: -0.004294991493225098 | Variación %: 0.2474551623848764
    Fecha: 2017-04-26 23:59:59+00:00 | Precio: 0.007454991340637207 | Variación %: -2.735740653362569
    Fecha: 2017-04-27 23:59:59+00:00 | Precio: 0.003300964832305908 | Variación %: -0.5572141292354926
    Fecha: 2017-04-28 23:59:59+00:00 | Precio: 0.010191023349761963 | Variación %: 2.0872862534082084
    Fecha: 2017-04-29 23:59:59+00:00 | Precio: 0.0026509761810302734 | Variación %: -0.73987144469724
    Fecha: 2017-04-30 23:59:59+00:00 | Precio: -0.0003389716148376465 | Variación %: -1.127866714632611
    Fecha: 2017-05-01 23:59:59+00:00 | Precio: -0.0009829998016357422 | Variación %: 1.899947248109724
    Fecha: 2017-05-02 23:59:59+00:00 | Precio: -0.003264009952545166 | Variación %: 2.320458404074703
    Fecha: 2017-05-03 23:59:59+00:00 | Precio: 0.0007439851760864258 | Variación %: -1.2279359398111795
    Fecha: 2017-05-04 23:59:59+00:00 | Precio: 0.012580037117004395 | Variación %: 15.908988944079475
    Fecha: 2017-05-05 23:59:59+00:00 | Precio: 0.009669959545135498 | Variación %: -0.23132503861497788
    Fecha: 2017-05-06 23:59:59+00:00 | Precio: 0.013018012046813965 | Variación %: 0.34623231731747156
    Fecha: 2017-05-07 23:59:59+00:00 | Precio: 0.00037103891372680664 | Variación %: -0.9714980357682481
    Fecha: 2017-05-08 23:59:59+00:00 | Precio: -0.0017300248146057129 | Variación %: -5.662650602409639
    Fecha: 2017-05-09 23:59:59+00:00 | Precio: 0.0032269954681396484 | Variación %: -2.865288544358312
    Fecha: 2017-05-10 23:59:59+00:00 | Precio: 0.011512994766235352 | Variación %: 2.567713335796084
    Fecha: 2017-05-11 23:59:59+00:00 | Precio: 0.001721024513244629 | Variación %: -0.8505146099525772
    Fecha: 2017-05-12 23:59:59+00:00 | Precio: -0.007651031017303467 | Variación %: -5.445625822539308
    Fecha: 2017-05-13 23:59:59+00:00 | Precio: -0.0024219751358032227 | Variación %: -0.6834446063117877
    Fecha: 2017-05-14 23:59:59+00:00 | Precio: 0.0074579715728759766 | Variación %: -4.079293202736625
    Fecha: 2017-05-15 23:59:59+00:00 | Precio: -0.013808012008666992 | Variación %: -2.8514433681787668
    Fecha: 2017-05-16 23:59:59+00:00 | Precio: -0.008706986904144287 | Variación %: -0.36942501942501943
    Fecha: 2017-05-17 23:59:59+00:00 | Precio: 0.011838018894195557 | Variación %: -2.3595999424968683
    Fecha: 2017-05-18 23:59:59+00:00 | Precio: -0.003286004066467285 | Variación %: -1.2775805728844112
    Fecha: 2017-05-19 23:59:59+00:00 | Precio: 0.03405696153640747 | Variación %: -11.364248140758209
    Fecha: 2017-05-20 23:59:59+00:00 | Precio: -0.007768988609313965 | Variación %: -1.2281174907811074
    Fecha: 2017-05-21 23:59:59+00:00 | Precio: 0.006649017333984375 | Variación %: -1.855840788080588
    Fecha: 2017-05-22 23:59:59+00:00 | Precio: 0.007779955863952637 | Variación %: 0.17009107860011474
    Fecha: 2017-05-23 23:59:59+00:00 | Precio: -0.0015599727630615234 | Variación %: -1.2005117754317147
    Fecha: 2017-05-24 23:59:59+00:00 | Precio: 0.010560035705566406 | Variación %: -7.76937184777625
    Fecha: 2017-05-25 23:59:59+00:00 | Precio: 0.019739985466003418 | Variación %: 0.8693104849634246
    Fecha: 2017-05-26 23:59:59+00:00 | Precio: -0.00039005279541015625 | Variación %: -1.019759527993671
    Fecha: 2017-05-27 23:59:59+00:00 | Precio: -0.0125199556350708 | Variación %: 31.098105134474327
    Fecha: 2017-05-28 23:59:59+00:00 | Precio: 0.01875007152557373 | Variación %: -2.4976148536062843
    Fecha: 2017-05-29 23:59:59+00:00 | Precio: -0.020840048789978027 | Variación %: -2.1114650288962213
    Fecha: 2017-05-30 23:59:59+00:00 | Precio: -0.012089967727661133 | Variación %: -0.4198685497571774
    Fecha: 2017-05-31 23:59:59+00:00 | Precio: 0.02676999568939209 | Variación %: -3.214232187580114
    Fecha: 2017-06-01 23:59:59+00:00 | Precio: -0.005710005760192871 | Variación %: -1.213298717954427
    Fecha: 2017-06-02 23:59:59+00:00 | Precio: -0.006690025329589844 | Variación %: 0.1716319756153573
    Fecha: 2017-06-03 23:59:59+00:00 | Precio: -0.0006600618362426758 | Variación %: -0.9013364219529579
    Fecha: 2017-06-04 23:59:59+00:00 | Precio: -0.01157999038696289 | Variación %: 16.543796279573776
    Fecha: 2017-06-05 23:59:59+00:00 | Precio: 0.005160093307495117 | Variación %: -1.4456042824788964
    Fecha: 2017-06-06 23:59:59+00:00 | Precio: -0.011970043182373047 | Variación %: -3.3197338631428175
    Fecha: 2017-06-07 23:59:59+00:00 | Precio: 0.004150032997131348 | Variación %: -1.34670158945146
    Fecha: 2017-06-08 23:59:59+00:00 | Precio: -0.004220008850097656 | Variación %: -2.0168615172493034
    Fecha: 2017-06-09 23:59:59+00:00 | Precio: -0.004090070724487305 | Variación %: -0.030790960451977403
    Fecha: 2017-06-10 23:59:59+00:00 | Precio: 0.02369999885559082 | Variación %: -6.794520547945205
    Fecha: 2017-06-11 23:59:59+00:00 | Precio: -0.016199946403503418 | Variación %: -1.6835420753483226
    Fecha: 2017-06-12 23:59:59+00:00 | Precio: 0.0095900297164917 | Variación %: -1.591979101512197
    Fecha: 2017-06-13 23:59:59+00:00 | Precio: -0.009370088577270508 | Variación %: -1.9770656457046254
    Fecha: 2017-06-14 23:59:59+00:00 | Precio: 0.016770005226135254 | Variación %: -2.789738174601155
    Fecha: 2017-06-15 23:59:59+00:00 | Precio: -0.007730007171630859 | Variación %: -1.4609424426167745
    Fecha: 2017-06-16 23:59:59+00:00 | Precio: -0.0018099546432495117 | Variación %: -0.7658534328542348
    Fecha: 2017-06-17 23:59:59+00:00 | Precio: -0.027036011219024658 | Variación %: 13.937397088849371
    Fecha: 2017-06-18 23:59:59+00:00 | Precio: 0.014236032962799072 | Variación %: -1.5265581837302051
    Fecha: 2017-06-19 23:59:59+00:00 | Precio: -0.016413986682891846 | Variación %: -2.1529888084541597
    Fecha: 2017-06-20 23:59:59+00:00 | Precio: -0.011134028434753418 | Variación %: -0.32167433483065283
    Fecha: 2017-06-21 23:59:59+00:00 | Precio: 0.006088972091674805 | Variación %: -1.5468795169113159
    Fecha: 2017-06-22 23:59:59+00:00 | Precio: -0.008458971977233887 | Variación %: -2.389228239163632
    Fecha: 2017-06-23 23:59:59+00:00 | Precio: 0.033098042011260986 | Variación %: -4.912773573472005
    Fecha: 2017-06-24 23:59:59+00:00 | Precio: 0.014499902725219727 | Variación %: -0.5619105589301504
    Fecha: 2017-06-25 23:59:59+00:00 | Precio: -0.007349967956542969 | Variación %: -1.5068977424075505
    Fecha: 2017-06-26 23:59:59+00:00 | Precio: -0.0030499696731567383 | Variación %: -0.5850363306085377
    Fecha: 2017-06-27 23:59:59+00:00 | Precio: -0.002969980239868164 | Variación %: -0.026226304475278482
    Fecha: 2017-06-28 23:59:59+00:00 | Precio: 0.00466001033782959 | Variación %: -2.5690374889620293
    Fecha: 2017-06-29 23:59:59+00:00 | Precio: 0.006009936332702637 | Variación %: 0.28968304724872734
    Fecha: 2017-06-30 23:59:59+00:00 | Precio: -0.011969923973083496 | Variación %: -2.9916889814539323
    Fecha: 2017-07-01 23:59:59+00:00 | Precio: 0.014140009880065918 | Variación %: -2.1812948780512094
    Fecha: 2017-07-02 23:59:59+00:00 | Precio: 0.0002899169921875 | Variación %: -0.9794966909750031
    Fecha: 2017-07-03 23:59:59+00:00 | Precio: -0.01951003074645996 | Variación %: -68.29523026315789
    Fecha: 2017-07-04 23:59:59+00:00 | Precio: -0.0019219517707824707 | Variación %: -0.9014890444941404
    Fecha: 2017-07-05 23:59:59+00:00 | Precio: -0.0023679733276367188 | Variación %: 0.23206698712978757
    Fecha: 2017-07-06 23:59:59+00:00 | Precio: 0.007139980792999268 | Variación %: -4.015228554168345
    Fecha: 2017-07-07 23:59:59+00:00 | Precio: 0.00439000129699707 | Variación %: -0.38515222599737875
    Fecha: 2017-07-08 23:59:59+00:00 | Precio: -0.008265018463134766 | Variación %: -2.8826915766034866
    Fecha: 2017-07-09 23:59:59+00:00 | Precio: 0.010195016860961914 | Variación %: -2.233514106040501
    Fecha: 2017-07-10 23:59:59+00:00 | Precio: -0.001970052719116211 | Variación %: -1.1932368279507028
    Fecha: 2017-07-11 23:59:59+00:00 | Precio: 0.004340052604675293 | Variación %: -3.203013433377708
    Fecha: 2017-07-12 23:59:59+00:00 | Precio: -0.014833986759185791 | Variación %: -4.417927871013816
    Fecha: 2017-07-13 23:59:59+00:00 | Precio: 0.006373941898345947 | Variación %: -1.4296850200704778
    Fecha: 2017-07-14 23:59:59+00:00 | Precio: -0.0008299350738525391 | Variación %: -1.1302075053536194
    Fecha: 2017-07-15 23:59:59+00:00 | Precio: -0.00102996826171875 | Variación %: 0.24102269462798045
    Fecha: 2017-07-16 23:59:59+00:00 | Precio: -0.0028090476989746094 | Variación %: 1.7273148148148147
    Fecha: 2017-07-17 23:59:59+00:00 | Precio: -0.0022730231285095215 | Variación %: -0.19082074350704464
    Fecha: 2017-07-18 23:59:59+00:00 | Precio: 0.0013279914855957031 | Variación %: -1.584240199291989
    Fecha: 2017-07-19 23:59:59+00:00 | Precio: 0.004874050617218018 | Variación %: 2.67024236983842
    Fecha: 2017-07-20 23:59:59+00:00 | Precio: -0.016224026679992676 | Variación %: -4.328653712105463
    Fecha: 2017-07-21 23:59:59+00:00 | Precio: 0.010335981845855713 | Variación %: -1.637078701220453
    Fecha: 2017-07-22 23:59:59+00:00 | Precio: -0.004001975059509277 | Variación %: -1.3871886695615567
    Fecha: 2017-07-23 23:59:59+00:00 | Precio: 0.004561007022857666 | Variación %: -2.139689017306604
    Fecha: 2017-07-24 23:59:59+00:00 | Precio: -0.003764033317565918 | Variación %: -1.8252636531148312
    Fecha: 2017-07-25 23:59:59+00:00 | Precio: 0.005805015563964844 | Variación %: -2.5422327790973873
    Fecha: 2017-07-26 23:59:59+00:00 | Precio: -0.002847015857696533 | Variación %: -1.4904406932807623
    Fecha: 2017-07-27 23:59:59+00:00 | Precio: 0.00032001733779907227 | Variación %: -1.1124044802679787
    Fecha: 2017-07-28 23:59:59+00:00 | Precio: 0.004665017127990723 | Variación %: 13.577388712981934
    Fecha: 2017-07-29 23:59:59+00:00 | Precio: -0.005321025848388672 | Variación %: -2.140623003603097
    Fecha: 2017-07-30 23:59:59+00:00 | Precio: 0.002249002456665039 | Variación %: -1.4226633210861188
    Fecha: 2017-07-31 23:59:59+00:00 | Precio: 0.0020520687103271484 | Variación %: -0.08756493162302555
    Fecha: 2017-08-01 23:59:59+00:00 | Precio: -0.0041010379791259766 | Variación %: -2.9984896014871616
    Fecha: 2017-08-02 23:59:59+00:00 | Precio: 0.004611015319824219 | Variación %: -2.124353235277019
    Fecha: 2017-08-03 23:59:59+00:00 | Precio: -0.032126009464263916 | Variación %: -7.967231127197518
    Fecha: 2017-08-04 23:59:59+00:00 | Precio: 0.03504592180252075 | Variación %: -2.0908893568466653
    Fecha: 2017-08-05 23:59:59+00:00 | Precio: -0.006035923957824707 | Variación %: -1.1722289969097222
    Fecha: 2017-08-06 23:59:59+00:00 | Precio: 0.002725958824157715 | Variación %: -1.4516224596606957
    Fecha: 2017-08-07 23:59:59+00:00 | Precio: -0.00478595495223999 | Variación %: -2.755695981108147
    Fecha: 2017-08-08 23:59:59+00:00 | Precio: 0.005255997180938721 | Variación %: -2.0982128401519398
    Fecha: 2017-08-09 23:59:59+00:00 | Precio: 0.0013499259948730469 | Variación %: -0.7431646273006657
    Fecha: 2017-08-10 23:59:59+00:00 | Precio: -0.009868979454040527 | Variación %: -8.31075591663723
    Fecha: 2017-08-11 23:59:59+00:00 | Precio: 0.007899045944213867 | Variación %: -1.8003913657941464
    Fecha: 2017-08-12 23:59:59+00:00 | Precio: 0.00023996829986572266 | Variación %: -0.9696205970239353
    Fecha: 2017-08-13 23:59:59+00:00 | Precio: -0.0025140047073364258 | Variación %: -11.476403378042722
    Fecha: 2017-08-14 23:59:59+00:00 | Precio: -0.00045299530029296875 | Variación %: -0.8198112760206743
    Fecha: 2017-08-15 23:59:59+00:00 | Precio: 0.0033670663833618164 | Variación %: -8.432894736842105
    Fecha: 2017-08-16 23:59:59+00:00 | Precio: -0.0003300905227661133 | Variación %: -1.0980350504514074
    Fecha: 2017-08-17 23:59:59+00:00 | Precio: 0.006749987602233887 | Variación %: -21.448898519321055
    Fecha: 2017-08-18 23:59:59+00:00 | Precio: 0.005380034446716309 | Variación %: -0.20295639581088956
    Fecha: 2017-08-19 23:59:59+00:00 | Precio: -0.010589957237243652 | Variación %: -2.968380935498881
    Fecha: 2017-08-20 23:59:59+00:00 | Precio: -0.006111025810241699 | Variación %: -0.42294140822873866
    Fecha: 2017-08-21 23:59:59+00:00 | Precio: 0.002633988857269287 | Variación %: -1.4310223748122428
    Fecha: 2017-08-22 23:59:59+00:00 | Precio: 0.007257044315338135 | Variación %: 1.7551537643411554
    Fecha: 2017-08-23 23:59:59+00:00 | Precio: -0.004510045051574707 | Variación %: -1.621471339515248
    Fecha: 2017-08-24 23:59:59+00:00 | Precio: 0.002910017967224121 | Variación %: -1.6452303544524622
    Fecha: 2017-08-25 23:59:59+00:00 | Precio: -0.0020600557327270508 | Variación %: -1.70791856130433
    Fecha: 2017-08-26 23:59:59+00:00 | Precio: -0.003927946090698242 | Variación %: 0.9067183612059487
    Fecha: 2017-08-27 23:59:59+00:00 | Precio: 0.004008054733276367 | Variación %: -2.0203945371775416
    Fecha: 2017-08-28 23:59:59+00:00 | Precio: -0.001880049705505371 | Variación %: -1.4690678722265182
    Fecha: 2017-08-29 23:59:59+00:00 | Precio: 0.00046002864837646484 | Variación %: -1.2446896201889543
    Fecha: 2017-08-30 23:59:59+00:00 | Precio: -0.0007799863815307617 | Variación %: -2.6955169733091475
    Fecha: 2017-08-31 23:59:59+00:00 | Precio: 0.002379894256591797 | Variación %: -4.051199755463855
    Fecha: 2017-09-01 23:59:59+00:00 | Precio: 0.0012500286102294922 | Variación %: -0.4747545582047686
    Fecha: 2017-09-02 23:59:59+00:00 | Precio: 0.013509988784790039 | Variación %: 9.807743658210947
    Fecha: 2017-09-03 23:59:59+00:00 | Precio: -0.015649914741516113 | Variación %: -2.1583958351716226
    Fecha: 2017-09-04 23:59:59+00:00 | Precio: 0.028319954872131348 | Variación %: -2.8095916393080493
    Fecha: 2017-09-05 23:59:59+00:00 | Precio: -0.02631998062133789 | Variación %: -1.929379327762928
    Fecha: 2017-09-06 23:59:59+00:00 | Precio: 0.0008599758148193359 | Variación %: -1.0326738772034711
    Fecha: 2017-09-07 23:59:59+00:00 | Precio: -0.00373995304107666 | Variación %: -5.348904907125035
    Fecha: 2017-09-08 23:59:59+00:00 | Precio: 0.005540013313293457 | Variación %: -2.4813055812322697
    Fecha: 2017-09-09 23:59:59+00:00 | Precio: -0.0056400299072265625 | Variación %: -2.0180534934262906
    Fecha: 2017-09-10 23:59:59+00:00 | Precio: 0.004199981689453125 | Variación %: -1.744673655732161
    Fecha: 2017-09-11 23:59:59+00:00 | Precio: -0.004379987716674805 | Variación %: -2.0428587647593095
    Fecha: 2017-09-12 23:59:59+00:00 | Precio: 0.004220008850097656 | Variación %: -1.963475042186054
    Fecha: 2017-09-13 23:59:59+00:00 | Precio: -0.0027500391006469727 | Variación %: -1.6516666666666666
    Fecha: 2017-09-14 23:59:59+00:00 | Precio: 0.0005899667739868164 | Variación %: -1.2145303220772465
    Fecha: 2017-09-15 23:59:59+00:00 | Precio: 0.0022400617599487305 | Variación %: 2.7969286724590825
    Fecha: 2017-09-16 23:59:59+00:00 | Precio: -0.0033800601959228516 | Variación %: -2.5089138417327446
    Fecha: 2017-09-17 23:59:59+00:00 | Precio: 0.004580020904541016 | Variación %: -2.355011638569514
    Fecha: 2017-09-18 23:59:59+00:00 | Precio: -0.0041599273681640625 | Variación %: -1.9082769390942218
    Fecha: 2017-09-19 23:59:59+00:00 | Precio: -0.0005600452423095703 | Variación %: -0.8653713892709766
    Fecha: 2017-09-20 23:59:59+00:00 | Precio: 0.002689957618713379 | Variación %: -5.803107705406556
    Fecha: 2017-09-21 23:59:59+00:00 | Precio: 0.0001800060272216797 | Variación %: -0.9330822069576779
    Fecha: 2017-09-22 23:59:59+00:00 | Precio: -0.00012993812561035156 | Variación %: -1.7218543046357615
    Fecha: 2017-09-23 23:59:59+00:00 | Precio: -0.0025000572204589844 | Variación %: 18.240366972477066
    Fecha: 2017-09-24 23:59:59+00:00 | Precio: 0.0008400678634643555 | Variación %: -1.3360194545107762
    Fecha: 2017-09-25 23:59:59+00:00 | Precio: -0.0016300678253173828 | Variación %: -2.9404001702852276
    Fecha: 2017-09-26 23:59:59+00:00 | Precio: 0.001289963722229004 | Variación %: -1.7913558578323827
    Fecha: 2017-09-27 23:59:59+00:00 | Precio: -0.001949906349182129 | Variación %: -2.5115978190555404
    Fecha: 2017-09-28 23:59:59+00:00 | Precio: 0.0011500120162963867 | Variación %: -1.589778076664425
    Fecha: 2017-09-29 23:59:59+00:00 | Precio: -0.001927018165588379 | Variación %: -2.6756504612833005
    Fecha: 2017-09-30 23:59:59+00:00 | Precio: -0.0033750534057617188 | Variación %: 0.7514382926074853
    Fecha: 2017-10-01 23:59:59+00:00 | Precio: 0.0034360289573669434 | Variación %: -2.0180665442215315
    Fecha: 2017-10-02 23:59:59+00:00 | Precio: 0.0017760396003723145 | Variación %: -0.4831127378701407
    Fecha: 2017-10-03 23:59:59+00:00 | Precio: -0.0015799999237060547 | Variación %: -1.8896197603785616
    Fecha: 2017-10-04 23:59:59+00:00 | Precio: 0.0011299848556518555 | Variación %: -1.7151803229213822
    Fecha: 2017-10-05 23:59:59+00:00 | Precio: -0.0009499788284301758 | Variación %: -1.8407004958328939
    Fecha: 2017-10-06 23:59:59+00:00 | Precio: 0.0007899999618530273 | Variación %: -1.8315974400803112
    Fecha: 2017-10-07 23:59:59+00:00 | Precio: -0.0017700791358947754 | Variación %: -3.2406066093254866
    Fecha: 2017-10-08 23:59:59+00:00 | Precio: -0.0008779764175415039 | Variación %: -0.5039903020507122
    Fecha: 2017-10-09 23:59:59+00:00 | Precio: 0.0013380050659179688 | Variación %: -2.5239646978954515
    Fecha: 2017-10-10 23:59:59+00:00 | Precio: -0.0003389716148376465 | Variación %: -1.253341054882395
    Fecha: 2017-10-11 23:59:59+00:00 | Precio: -0.000816047191619873 | Variación %: 1.4074204325655002
    Fecha: 2017-10-12 23:59:59+00:00 | Precio: -0.0012019872665405273 | Variación %: 0.4729384267036739
    Fecha: 2017-10-13 23:59:59+00:00 | Precio: 0.002626955509185791 | Variación %: -3.1855102648021423
    Fecha: 2017-10-14 23:59:59+00:00 | Precio: -0.0003409385681152344 | Variación %: -1.1297846754248633
    Fecha: 2017-10-15 23:59:59+00:00 | Precio: -0.00046700239181518555 | Variación %: 0.36975524475524474
    Fecha: 2017-10-16 23:59:59+00:00 | Precio: -0.0012320280075073242 | Variación %: 1.6381620931716656
    Fecha: 2017-10-17 23:59:59+00:00 | Precio: 0.0013250112533569336 | Variación %: -2.0754716981132075
    Fecha: 2017-10-18 23:59:59+00:00 | Precio: 0.0033449530601501465 | Variación %: 1.5244714349977508
    Fecha: 2017-10-19 23:59:59+00:00 | Precio: -0.0020200014114379883 | Variación %: -1.6038952939289723
    Fecha: 2017-10-20 23:59:59+00:00 | Precio: 0.0003600120544433594 | Variación %: -1.1782236647978754
    Fecha: 2017-10-21 23:59:59+00:00 | Precio: -9.000301361083984e-05 | Variación %: -1.25
    Fecha: 2017-10-22 23:59:59+00:00 | Precio: 0.001000046730041504 | Variación %: -12.111258278145696
    Fecha: 2017-10-23 23:59:59+00:00 | Precio: -0.00539398193359375 | Variación %: -6.393729884372393
    Fecha: 2017-10-24 23:59:59+00:00 | Precio: 0.006214022636413574 | Variación %: -2.152028818953324
    Fecha: 2017-10-25 23:59:59+00:00 | Precio: -0.0004900693893432617 | Variación %: -1.0788650795173327
    Fecha: 2017-10-26 23:59:59+00:00 | Precio: -0.002391993999481201 | Variación %: 3.880929214303089
    Fecha: 2017-10-27 23:59:59+00:00 | Precio: 0.00020200014114379883 | Variación %: -1.084448431387207
    Fecha: 2017-10-28 23:59:59+00:00 | Precio: 0.0038900375366210938 | Variación %: 18.257598111537327
    Fecha: 2017-10-29 23:59:59+00:00 | Precio: -0.002850055694580078 | Variación %: -1.7326550625153223
    Fecha: 2017-10-30 23:59:59+00:00 | Precio: -0.0005300045013427734 | Variación %: -0.81403714237912
    Fecha: 2017-10-31 23:59:59+00:00 | Precio: 0.00013005733489990234 | Variación %: -1.2453891138101665
    Fecha: 2017-11-01 23:59:59+00:00 | Precio: 0.0008399486541748047 | Variación %: 5.458295142071494
    Fecha: 2017-11-02 23:59:59+00:00 | Precio: -0.0005499124526977539 | Variación %: -1.654697700823162
    Fecha: 2017-11-03 23:59:59+00:00 | Precio: 0.005319952964782715 | Variación %: -10.674181660524605
    Fecha: 2017-11-04 23:59:59+00:00 | Precio: -0.004230022430419922 | Variación %: -1.7951240280547651
    Fecha: 2017-11-05 23:59:59+00:00 | Precio: -0.0032899975776672363 | Variación %: -0.22222691917483936
    Fecha: 2017-11-06 23:59:59+00:00 | Precio: 0.00457996129989624 | Variación %: -2.3920865264416546
    Fecha: 2017-11-07 23:59:59+00:00 | Precio: 0.002280116081237793 | Variación %: -0.5021538541625997
    Fecha: 2017-11-08 23:59:59+00:00 | Precio: 0.0062999725341796875 | Variación %: 1.7630051759293146
    Fecha: 2017-11-09 23:59:59+00:00 | Precio: -0.0037800073623657227 | Variación %: -1.6000037844383894
    Fecha: 2017-11-10 23:59:59+00:00 | Precio: -0.002169966697692871 | Variación %: -0.42593585417389385
    Fecha: 2017-11-11 23:59:59+00:00 | Precio: 0.0029799938201904297 | Variación %: -2.373290117013679
    Fecha: 2017-11-12 23:59:59+00:00 | Precio: 0.0034799575805664062 | Variación %: 0.1677734218737499
    Fecha: 2017-11-13 23:59:59+00:00 | Precio: -0.0031200647354125977 | Variación %: -1.896581255138394
    Fecha: 2017-11-14 23:59:59+00:00 | Precio: -0.002519965171813965 | Variación %: -0.19233561303633515
    Fecha: 2017-11-15 23:59:59+00:00 | Precio: -0.0036499500274658203 | Variación %: 0.44841288613463265
    Fecha: 2017-11-16 23:59:59+00:00 | Precio: -0.0010600090026855469 | Variación %: -0.7095825984714874
    Fecha: 2017-11-17 23:59:59+00:00 | Precio: -0.0007300376892089844 | Variación %: -0.3112910481331534
    Fecha: 2017-11-18 23:59:59+00:00 | Precio: 0.0009200572967529297 | Variación %: -2.260287393860222
    Fecha: 2017-11-19 23:59:59+00:00 | Precio: 0.00012993812561035156 | Variación %: -0.8587717025136046
    Fecha: 2017-11-20 23:59:59+00:00 | Precio: -0.0005199909210205078 | Variación %: -5.001834862385321
    Fecha: 2017-11-21 23:59:59+00:00 | Precio: -0.005872964859008789 | Variación %: 10.29436038514443
    Fecha: 2017-11-22 23:59:59+00:00 | Precio: 0.004102945327758789 | Variación %: -1.69861567815532
    Fecha: 2017-11-23 23:59:59+00:00 | Precio: -0.005518972873687744 | Variación %: -2.345124644081585
    Fecha: 2017-11-24 23:59:59+00:00 | Precio: 0.007698953151702881 | Variación %: -2.394997462011167
    Fecha: 2017-11-25 23:59:59+00:00 | Precio: 0.003080010414123535 | Variación %: -0.5999442582083659
    Fecha: 2017-11-26 23:59:59+00:00 | Precio: 0.0032700300216674805 | Variación %: 0.0616944691721175
    Fecha: 2017-11-27 23:59:59+00:00 | Precio: -0.007390022277832031 | Variación %: -3.2599249024825925
    Fecha: 2017-11-28 23:59:59+00:00 | Precio: -0.0011500120162963867 | Variación %: -0.8443831462124145
    Fecha: 2017-11-29 23:59:59+00:00 | Precio: -0.009533941745758057 | Variación %: 7.2902975018140355
    Fecha: 2017-11-30 23:59:59+00:00 | Precio: 0.017494022846221924 | Variación %: -2.834920257825736
    Fecha: 2017-12-01 23:59:59+00:00 | Precio: 0.0016800165176391602 | Variación %: -0.9039662556515992
    Fecha: 2017-12-02 23:59:59+00:00 | Precio: -0.010126054286956787 | Variación %: -7.027354005534662
    Fecha: 2017-12-03 23:59:59+00:00 | Precio: 0.0010059475898742676 | Variación %: -1.0993425041351015
    Fecha: 2017-12-04 23:59:59+00:00 | Precio: 0.0030100345611572266 | Variación %: 1.992237956982876
    Fecha: 2017-12-05 23:59:59+00:00 | Precio: -0.0016999244689941406 | Variación %: -1.5647524752475248
    Fecha: 2017-12-06 23:59:59+00:00 | Precio: 0.007939934730529785 | Variación %: -5.670757363253857
    Fecha: 2017-12-07 23:59:59+00:00 | Precio: 0.02174997329711914 | Variación %: 1.739313865325426
    Fecha: 2017-12-08 23:59:59+00:00 | Precio: -0.014059901237487793 | Variación %: -1.6464330344419353
    Fecha: 2017-12-09 23:59:59+00:00 | Precio: -0.00047004222869873047 | Variación %: -0.9665685966950137
    Fecha: 2017-12-10 23:59:59+00:00 | Precio: 0.0006200075149536133 | Variación %: -2.3190464113619074
    Fecha: 2017-12-11 23:59:59+00:00 | Precio: 0.0008100271224975586 | Variación %: 0.3064795231686214
    Fecha: 2017-12-12 23:59:59+00:00 | Precio: 0.05931997299194336 | Variación %: 72.23208241353937
    Fecha: 2017-12-13 23:59:59+00:00 | Precio: -0.0507199764251709 | Variación %: -1.8550235926786331
    Fecha: 2017-12-14 23:59:59+00:00 | Precio: -0.018970012664794922 | Variación %: -0.625985380872917
    Fecha: 2017-12-15 23:59:59+00:00 | Precio: 0.007910013198852539 | Variación %: -1.4169745871352084
    Fecha: 2017-12-16 23:59:59+00:00 | Precio: -0.008680105209350586 | Variación %: -2.0973566024655637
    Fecha: 2017-12-17 23:59:59+00:00 | Precio: 0.0018200874328613281 | Variación %: -1.2096849506962946
    Fecha: 2017-12-18 23:59:59+00:00 | Precio: 0.0037800073623657227 | Variación %: 1.0768273513230286
    Fecha: 2017-12-19 23:59:59+00:00 | Precio: -0.002340078353881836 | Variación %: -1.6190671418209341
    Fecha: 2017-12-20 23:59:59+00:00 | Precio: -0.010499954223632812 | Variación %: 3.487009679062659
    Fecha: 2017-12-21 23:59:59+00:00 | Precio: 0.009029984474182129 | Variación %: -1.8600022706630337
    Fecha: 2017-12-22 23:59:59+00:00 | Precio: 0.008740067481994629 | Variación %: -0.03210603440309443
    Fecha: 2017-12-23 23:59:59+00:00 | Precio: 0.027309894561767578 | Variación %: 2.12467776913949
    Fecha: 2017-12-24 23:59:59+00:00 | Precio: -0.022229909896850586 | Variación %: -1.8139873937108235
    Fecha: 2017-12-25 23:59:59+00:00 | Precio: -0.011900067329406738 | Variación %: -0.4646821608983365
    Fecha: 2017-12-26 23:59:59+00:00 | Precio: -0.007059931755065918 | Variación %: -0.4067317806160781
    Fecha: 2017-12-27 23:59:59+00:00 | Precio: -0.0004100799560546875 | Variación %: -0.9419144589095453
    Fecha: 2017-12-28 23:59:59+00:00 | Precio: 0.0029300451278686523 | Variación %: -8.145058139534884
    Fecha: 2017-12-29 23:59:59+00:00 | Precio: -0.0009499788284301758 | Variación %: -1.3242198624842345
    Fecha: 2017-12-30 23:59:59+00:00 | Precio: 0.015709996223449707 | Variación %: -17.537206675868994
    Fecha: 2017-12-31 23:59:59+00:00 | Precio: -0.009090065956115723 | Variación %: -1.5786166862693023


### Tarea 3.2: Comparación de precios de cierre (Join)

El objetivo es unir los precios de dos activos en una misma tabla para su comparación.

1.  Crea dos *pipelines* separadas para los precios de cierre (`close`):
    - `btc_data` para **`BTC`**.
    - `eth_data` para **`ETH`**.
    - Ambas deben usar el mismo rango de tiempo (ej. **año 2020**).
2.  Usa la función **`join()`** para combinar ambas tablas por la marca de tiempo (`on: ["_time"]`).
3.  Usa la función **`map()`** para calcular una nueva columna llamada **`ratio`** que sea el resultado de dividir el precio de BTC entre el precio de ETH (`r.btc_data._value / r.eth_data._value`).




```python
query_5 = """
// Pipeline BTC
btc_data = 
    from(bucket: "crypto_raw")
        |> range(start: 2020-01-01T00:00:00Z, stop: 2021-01-01T00:00:00Z)
        |> filter(fn: (r) => r.symbol == "BTC")
        |> filter(fn: (r) => r._field == "close")

// Pipeline ETH
eth_data = 
    from(bucket: "crypto_raw")
        |> range(start: 2020-01-01T00:00:00Z, stop: 2021-01-01T00:00:00Z)
        |> filter(fn: (r) => r.symbol == "ETH")
        |> filter(fn: (r) => r._field == "close")

// Join por timestamp
join(
    tables: {btc_data: btc_data, eth_data: eth_data},
    on: ["_time"]
)
|> map(fn: (r) => ({
        r with
        ratio: r._value_btc_data / r._value_eth_data
    }))
"""

result = query_api.query(query=query_5)

for table in result:
    for record in table.records:
        btc = record["_value_btc_data"]
        eth = record["_value_eth_data"]
        ratio = record["ratio"]

        print(
            f"Fecha: {record.get_time()} | "
            f"BTC: {btc} | "
            f"ETH: {eth} | "
            f"Ratio BTC/ETH: {ratio}"
        )

```

    Fecha: 2020-01-01 23:59:59+00:00 | BTC: 7200.17439274 | ETH: 130.802008077 | Ratio BTC/ETH: 55.04635975084901
    Fecha: 2020-01-02 23:59:59+00:00 | BTC: 6985.47000061 | ETH: 127.410182379 | Ratio BTC/ETH: 54.826622724946034
    Fecha: 2020-01-03 23:59:59+00:00 | BTC: 7344.88418341 | ETH: 134.171712485 | Ratio BTC/ETH: 54.74241960078684
    Fecha: 2020-01-04 23:59:59+00:00 | BTC: 7410.65656642 | ETH: 135.069371268 | Ratio BTC/ETH: 54.865559059396446
    Fecha: 2020-01-05 23:59:59+00:00 | BTC: 7411.31732676 | ETH: 136.276776707 | Ratio BTC/ETH: 54.38430160917732
    Fecha: 2020-01-06 23:59:59+00:00 | BTC: 7769.21903905 | ETH: 144.30415371 | Ratio BTC/ETH: 53.83919200734419
    Fecha: 2020-01-07 23:59:59+00:00 | BTC: 8163.69223944 | ETH: 143.543998337 | Ratio BTC/ETH: 56.87240382056238
    Fecha: 2020-01-08 23:59:59+00:00 | BTC: 8079.86277673 | ETH: 141.258134415 | Ratio BTC/ETH: 57.199274294479224
    Fecha: 2020-01-09 23:59:59+00:00 | BTC: 7879.07152428 | ETH: 138.979196656 | Ratio BTC/ETH: 56.692452639384605
    Fecha: 2020-01-10 23:59:59+00:00 | BTC: 8166.55414039 | ETH: 143.963781218 | Ratio BTC/ETH: 56.72644932841569
    Fecha: 2020-01-11 23:59:59+00:00 | BTC: 8037.53738872 | ETH: 142.927114494 | Ratio BTC/ETH: 56.23521762945415
    Fecha: 2020-01-12 23:59:59+00:00 | BTC: 8192.49400532 | ETH: 145.873931189 | Ratio BTC/ETH: 56.16146722408875
    Fecha: 2020-01-13 23:59:59+00:00 | BTC: 8144.19451744 | ETH: 144.226591141 | Ratio BTC/ETH: 56.4680510924508
    Fecha: 2020-01-14 23:59:59+00:00 | BTC: 8827.76442606 | ETH: 165.955358611 | Ratio BTC/ETH: 53.19360881110391
    Fecha: 2020-01-15 23:59:59+00:00 | BTC: 8807.01027532 | ETH: 166.230685102 | Ratio BTC/ETH: 52.98065318034378
    Fecha: 2020-01-16 23:59:59+00:00 | BTC: 8723.78576573 | ETH: 164.391010988 | Ratio BTC/ETH: 53.06729189935334
    Fecha: 2020-01-17 23:59:59+00:00 | BTC: 8929.0376776 | ETH: 170.77995796 | Ratio BTC/ETH: 52.28387326158819
    Fecha: 2020-01-18 23:59:59+00:00 | BTC: 8942.80890321 | ETH: 175.36567147 | Ratio BTC/ETH: 50.99520806008978
    Fecha: 2020-01-19 23:59:59+00:00 | BTC: 8706.24512993 | ETH: 166.969841975 | Ratio BTC/ETH: 52.142620649024536
    Fecha: 2020-01-20 23:59:59+00:00 | BTC: 8657.64293942 | ETH: 167.120509335 | Ratio BTC/ETH: 51.80479029097138
    Fecha: 2020-01-21 23:59:59+00:00 | BTC: 8745.89478833 | ETH: 169.69716391 | Ratio BTC/ETH: 51.5382495901254
    Fecha: 2020-01-22 23:59:59+00:00 | BTC: 8680.87604222 | ETH: 168.294161709 | Ratio BTC/ETH: 51.581563816992265
    Fecha: 2020-01-23 23:59:59+00:00 | BTC: 8406.5160678 | ETH: 162.928558428 | Ratio BTC/ETH: 51.596332459511295
    Fecha: 2020-01-24 23:59:59+00:00 | BTC: 8445.43428152 | ETH: 163.051182861 | Ratio BTC/ETH: 51.79621596931114
    Fecha: 2020-01-25 23:59:59+00:00 | BTC: 8367.84777344 | ETH: 161.283936353 | Ratio BTC/ETH: 51.882710471087485
    Fecha: 2020-01-26 23:59:59+00:00 | BTC: 8596.82983316 | ETH: 168.077100489 | Ratio BTC/ETH: 51.14813266143075
    Fecha: 2020-01-27 23:59:59+00:00 | BTC: 8909.81917753 | ETH: 170.930890433 | Ratio BTC/ETH: 52.12527211997642
    Fecha: 2020-01-28 23:59:59+00:00 | BTC: 9358.59031703 | ETH: 176.370320541 | Ratio BTC/ETH: 53.06216084612973
    Fecha: 2020-01-29 23:59:59+00:00 | BTC: 9316.62950445 | ETH: 175.050337929 | Ratio BTC/ETH: 53.222573658948335
    Fecha: 2020-01-30 23:59:59+00:00 | BTC: 9508.9935947 | ETH: 184.690476436 | Ratio BTC/ETH: 51.486106799855
    Fecha: 2020-01-31 23:59:59+00:00 | BTC: 9350.52936518 | ETH: 180.160175239 | Ratio BTC/ETH: 51.90120043331226
    Fecha: 2020-02-01 23:59:59+00:00 | BTC: 9392.87536841 | ETH: 183.673947121 | Ratio BTC/ETH: 51.13885510514019
    Fecha: 2020-02-02 23:59:59+00:00 | BTC: 9344.36529292 | ETH: 188.617538168 | Ratio BTC/ETH: 49.54133843374127
    Fecha: 2020-02-03 23:59:59+00:00 | BTC: 9293.52108908 | ETH: 189.865063235 | Ratio BTC/ETH: 48.94803146367804
    Fecha: 2020-02-04 23:59:59+00:00 | BTC: 9180.9629665 | ETH: 189.250602393 | Ratio BTC/ETH: 48.51219943508927
    Fecha: 2020-02-05 23:59:59+00:00 | BTC: 9613.42428895 | ETH: 204.230244698 | Ratio BTC/ETH: 47.07150159451453
    Fecha: 2020-02-06 23:59:59+00:00 | BTC: 9729.80223149 | ETH: 212.339079745 | Ratio BTC/ETH: 45.82200432993593
    Fecha: 2020-02-07 23:59:59+00:00 | BTC: 9795.94377253 | ETH: 222.72606629 | Ratio BTC/ETH: 43.98202660201977
    Fecha: 2020-02-08 23:59:59+00:00 | BTC: 9865.11946905 | ETH: 223.146521744 | Ratio BTC/ETH: 44.209156351392934
    Fecha: 2020-02-09 23:59:59+00:00 | BTC: 10116.673759 | ETH: 228.578569991 | Ratio BTC/ETH: 44.25906487820941
    Fecha: 2020-02-10 23:59:59+00:00 | BTC: 9856.61149362 | ETH: 223.52269963 | Ratio BTC/ETH: 44.096691342471146
    Fecha: 2020-02-11 23:59:59+00:00 | BTC: 10208.2362609 | ETH: 235.851199501 | Ratio BTC/ETH: 43.28252848617256
    Fecha: 2020-02-12 23:59:59+00:00 | BTC: 10326.0545246 | ETH: 265.406126106 | Ratio BTC/ETH: 38.906617100751845
    Fecha: 2020-02-13 23:59:59+00:00 | BTC: 10214.3794638 | ETH: 268.099256044 | Ratio BTC/ETH: 38.09924583350441
    Fecha: 2020-02-14 23:59:59+00:00 | BTC: 10312.1160909 | ETH: 284.217509609 | Ratio BTC/ETH: 36.282479939699876
    Fecha: 2020-02-15 23:59:59+00:00 | BTC: 9889.42462838 | ETH: 264.728585265 | Ratio BTC/ETH: 37.356844628170535
    Fecha: 2020-02-16 23:59:59+00:00 | BTC: 9934.43339025 | ETH: 259.894703492 | Ratio BTC/ETH: 38.22483973997492
    Fecha: 2020-02-17 23:59:59+00:00 | BTC: 9690.14261814 | ETH: 266.363446303 | Ratio BTC/ETH: 36.37940097500106
    Fecha: 2020-02-18 23:59:59+00:00 | BTC: 10141.9963705 | ETH: 281.944579134 | Ratio BTC/ETH: 35.97159555842996
    Fecha: 2020-02-19 23:59:59+00:00 | BTC: 9633.38688518 | ETH: 259.763962739 | Ratio BTC/ETH: 37.085155244799004
    Fecha: 2020-02-20 23:59:59+00:00 | BTC: 9608.47590343 | ETH: 257.949455024 | Ratio BTC/ETH: 37.24945223294236
    Fecha: 2020-02-21 23:59:59+00:00 | BTC: 9686.44119763 | ETH: 265.600612524 | Ratio BTC/ETH: 36.46995052300462
    Fecha: 2020-02-22 23:59:59+00:00 | BTC: 9663.18182933 | ETH: 262.331720974 | Ratio BTC/ETH: 36.83573527994248
    Fecha: 2020-02-23 23:59:59+00:00 | BTC: 9924.51522822 | ETH: 273.754156046 | Ratio BTC/ETH: 36.25338651133517
    Fecha: 2020-02-24 23:59:59+00:00 | BTC: 9650.17480677 | ETH: 265.216417336 | Ratio BTC/ETH: 36.38603863102596
    Fecha: 2020-02-25 23:59:59+00:00 | BTC: 9341.70516876 | ETH: 247.817592279 | Ratio BTC/ETH: 37.695891897145245
    Fecha: 2020-02-26 23:59:59+00:00 | BTC: 8820.52220005 | ETH: 225.680265514 | Ratio BTC/ETH: 39.08415376931937
    Fecha: 2020-02-27 23:59:59+00:00 | BTC: 8784.49384867 | ETH: 226.753395276 | Ratio BTC/ETH: 38.74029686734207
    Fecha: 2020-02-28 23:59:59+00:00 | BTC: 8672.45534996 | ETH: 226.760501479 | Ratio BTC/ETH: 38.24499987165157
    Fecha: 2020-02-29 23:59:59+00:00 | BTC: 8599.50861972 | ETH: 219.84851255 | Ratio BTC/ETH: 39.11560974406965
    Fecha: 2020-03-01 23:59:59+00:00 | BTC: 8562.45405008 | ETH: 218.970599927 | Ratio BTC/ETH: 39.10321318448474
    Fecha: 2020-03-02 23:59:59+00:00 | BTC: 8869.67031078 | ETH: 230.569781825 | Ratio BTC/ETH: 38.46848550827005
    Fecha: 2020-03-03 23:59:59+00:00 | BTC: 8787.78645576 | ETH: 224.479622332 | Ratio BTC/ETH: 39.14736831997639
    Fecha: 2020-03-04 23:59:59+00:00 | BTC: 8755.24589461 | ETH: 224.517976367 | Ratio BTC/ETH: 38.995745624833894
    Fecha: 2020-03-05 23:59:59+00:00 | BTC: 9078.76279174 | ETH: 229.26818886 | Ratio BTC/ETH: 39.59887691738972
    Fecha: 2020-03-06 23:59:59+00:00 | BTC: 9122.54557333 | ETH: 243.525299741 | Ratio BTC/ETH: 37.46036072240639
    Fecha: 2020-03-07 23:59:59+00:00 | BTC: 8909.9536515 | ETH: 237.853095033 | Ratio BTC/ETH: 37.459902088992465
    Fecha: 2020-03-08 23:59:59+00:00 | BTC: 8108.11629101 | ETH: 200.689052256 | Ratio BTC/ETH: 40.40138811691255
    Fecha: 2020-03-09 23:59:59+00:00 | BTC: 7923.6447033 | ETH: 201.986327111 | Ratio BTC/ETH: 39.228619167601494
    Fecha: 2020-03-10 23:59:59+00:00 | BTC: 7909.72939346 | ETH: 200.767247427 | Ratio BTC/ETH: 39.3975087810875
    Fecha: 2020-03-11 23:59:59+00:00 | BTC: 7911.43012933 | ETH: 194.868528471 | Ratio BTC/ETH: 40.598808804097715
    Fecha: 2020-03-12 23:59:59+00:00 | BTC: 4970.78790105 | ETH: 112.347123759 | Ratio BTC/ETH: 44.244905741539256
    Fecha: 2020-03-13 23:59:59+00:00 | BTC: 5563.70689169 | ETH: 133.201807239 | Ratio BTC/ETH: 41.7690045429129
    Fecha: 2020-03-14 23:59:59+00:00 | BTC: 5200.36626392 | ETH: 123.306024593 | Ratio BTC/ETH: 42.174470234402655
    Fecha: 2020-03-15 23:59:59+00:00 | BTC: 5392.31488002 | ETH: 125.214304313 | Ratio BTC/ETH: 43.06468745408474
    Fecha: 2020-03-16 23:59:59+00:00 | BTC: 5014.47997748 | ETH: 110.605876012 | Ratio BTC/ETH: 45.33646998045531
    Fecha: 2020-03-17 23:59:59+00:00 | BTC: 5225.62919259 | ETH: 113.942750228 | Ratio BTC/ETH: 45.861883991157754
    Fecha: 2020-03-18 23:59:59+00:00 | BTC: 5238.43857664 | ETH: 114.842273039 | Ratio BTC/ETH: 45.61420144358381
    Fecha: 2020-03-19 23:59:59+00:00 | BTC: 6191.19295222 | ETH: 136.593857971 | Ratio BTC/ETH: 45.32555888079858
    Fecha: 2020-03-20 23:59:59+00:00 | BTC: 6198.77820508 | ETH: 132.737170068 | Ratio BTC/ETH: 46.69964111713715
    Fecha: 2020-03-21 23:59:59+00:00 | BTC: 6185.06651501 | ETH: 132.818707849 | Ratio BTC/ETH: 46.56773594004339
    Fecha: 2020-03-22 23:59:59+00:00 | BTC: 5830.25479765 | ETH: 123.321147745 | Ratio BTC/ETH: 47.27700726322817
    Fecha: 2020-03-23 23:59:59+00:00 | BTC: 6416.31475839 | ETH: 134.911612009 | Ratio BTC/ETH: 47.55939583586004
    Fecha: 2020-03-24 23:59:59+00:00 | BTC: 6734.80378045 | ETH: 138.761445013 | Ratio BTC/ETH: 48.53512284928312
    Fecha: 2020-03-25 23:59:59+00:00 | BTC: 6681.06312656 | ETH: 136.195892908 | Ratio BTC/ETH: 49.05480616124777
    Fecha: 2020-03-26 23:59:59+00:00 | BTC: 6716.44054866 | ETH: 138.361557339 | Ratio BTC/ETH: 48.54267816749151
    Fecha: 2020-03-27 23:59:59+00:00 | BTC: 6469.79813509 | ETH: 133.937940192 | Ratio BTC/ETH: 48.304447013411924
    Fecha: 2020-03-28 23:59:59+00:00 | BTC: 6242.1938684 | ETH: 130.986494884 | Ratio BTC/ETH: 47.65524777136764
    Fecha: 2020-03-29 23:59:59+00:00 | BTC: 5922.0431227 | ETH: 125.583730441 | Ratio BTC/ETH: 47.15613321808601
    Fecha: 2020-03-30 23:59:59+00:00 | BTC: 6429.84193389 | ETH: 132.904538063 | Ratio BTC/ETH: 48.37940094146445
    Fecha: 2020-03-31 23:59:59+00:00 | BTC: 6438.64476637 | ETH: 133.593565057 | Ratio BTC/ETH: 48.19577023506215
    Fecha: 2020-04-01 23:59:59+00:00 | BTC: 6606.77626829 | ETH: 135.634552336 | Ratio BTC/ETH: 48.71012698831635
    Fecha: 2020-04-02 23:59:59+00:00 | BTC: 6793.62459642 | ETH: 142.029147631 | Ratio BTC/ETH: 47.83260837465724
    Fecha: 2020-04-03 23:59:59+00:00 | BTC: 6733.3873906 | ETH: 142.091309874 | Ratio BTC/ETH: 47.387749444852446
    Fecha: 2020-04-04 23:59:59+00:00 | BTC: 6867.52731596 | ETH: 145.219384622 | Ratio BTC/ETH: 47.2907066355906
    Fecha: 2020-04-05 23:59:59+00:00 | BTC: 6791.12944093 | ETH: 143.54664871 | Ratio BTC/ETH: 47.30956453500892
    Fecha: 2020-04-06 23:59:59+00:00 | BTC: 7271.7811527 | ETH: 169.135884595 | Ratio BTC/ETH: 42.99372170555325
    Fecha: 2020-04-07 23:59:59+00:00 | BTC: 7176.41450049 | ETH: 165.101942525 | Ratio BTC/ETH: 43.46656611507364
    Fecha: 2020-04-08 23:59:59+00:00 | BTC: 7334.09845346 | ETH: 172.641733789 | Ratio BTC/ETH: 42.48160796637747
    Fecha: 2020-04-09 23:59:59+00:00 | BTC: 7302.0895105 | ETH: 170.807147486 | Ratio BTC/ETH: 42.75049152201612
    Fecha: 2020-04-10 23:59:59+00:00 | BTC: 6865.49337195 | ETH: 158.412448608 | Ratio BTC/ETH: 43.33935515976416
    Fecha: 2020-04-11 23:59:59+00:00 | BTC: 6859.08296343 | ETH: 158.216023679 | Ratio BTC/ETH: 43.352644087088166
    Fecha: 2020-04-12 23:59:59+00:00 | BTC: 6971.09159108 | ETH: 161.142420145 | Ratio BTC/ETH: 43.260437473926714
    Fecha: 2020-04-13 23:59:59+00:00 | BTC: 6845.03769683 | ETH: 156.279549094 | Ratio BTC/ETH: 43.79995806561231
    Fecha: 2020-04-14 23:59:59+00:00 | BTC: 6842.42786097 | ETH: 157.596395681 | Ratio BTC/ETH: 43.41741339579971
    Fecha: 2020-04-15 23:59:59+00:00 | BTC: 6642.10989286 | ETH: 153.286892905 | Ratio BTC/ETH: 43.331231829302375
    Fecha: 2020-04-16 23:59:59+00:00 | BTC: 7116.80421777 | ETH: 172.157382821 | Ratio BTC/ETH: 41.33894289720744
    Fecha: 2020-04-17 23:59:59+00:00 | BTC: 7096.18465879 | ETH: 171.638582707 | Ratio BTC/ETH: 41.34376168150795
    Fecha: 2020-04-18 23:59:59+00:00 | BTC: 7257.66485847 | ETH: 186.914005844 | Ratio BTC/ETH: 38.82889795068277
    Fecha: 2020-04-19 23:59:59+00:00 | BTC: 7189.42482356 | ETH: 181.614959142 | Ratio BTC/ETH: 39.586082872935464
    Fecha: 2020-04-20 23:59:59+00:00 | BTC: 6881.95869275 | ETH: 172.297157575 | Ratio BTC/ETH: 39.94238088201961
    Fecha: 2020-04-21 23:59:59+00:00 | BTC: 6880.32347375 | ETH: 172.737700531 | Ratio BTC/ETH: 39.831047030264465
    Fecha: 2020-04-22 23:59:59+00:00 | BTC: 7117.20747869 | ETH: 182.599574801 | Ratio BTC/ETH: 38.97713062282018
    Fecha: 2020-04-23 23:59:59+00:00 | BTC: 7429.72464927 | ETH: 185.028670833 | Ratio BTC/ETH: 40.154450744424324
    Fecha: 2020-04-24 23:59:59+00:00 | BTC: 7550.90102725 | ETH: 189.236941873 | Ratio BTC/ETH: 39.9018339258385
    Fecha: 2020-04-25 23:59:59+00:00 | BTC: 7569.93603405 | ETH: 195.515300681 | Ratio BTC/ETH: 38.71787020086474
    Fecha: 2020-04-26 23:59:59+00:00 | BTC: 7679.86720422 | ETH: 197.317530184 | Ratio BTC/ETH: 38.921362927351005
    Fecha: 2020-04-27 23:59:59+00:00 | BTC: 7795.60083451 | ETH: 197.2247212 | Ratio BTC/ETH: 39.5264893116756
    Fecha: 2020-04-28 23:59:59+00:00 | BTC: 7807.05845106 | ETH: 198.415382994 | Ratio BTC/ETH: 39.34704221646001
    Fecha: 2020-04-29 23:59:59+00:00 | BTC: 8801.03776688 | ETH: 216.968223855 | Ratio BTC/ETH: 40.563717628816185
    Fecha: 2020-04-30 23:59:59+00:00 | BTC: 8658.55417975 | ETH: 207.602055895 | Ratio BTC/ETH: 41.70745873600251
    Fecha: 2020-05-01 23:59:59+00:00 | BTC: 8864.76680793 | ETH: 214.219106382 | Ratio BTC/ETH: 41.38177475225838
    Fecha: 2020-05-02 23:59:59+00:00 | BTC: 8988.5962069 | ETH: 215.32538422 | Ratio BTC/ETH: 41.74424784825307
    Fecha: 2020-05-03 23:59:59+00:00 | BTC: 8897.46850985 | ETH: 210.93315693 | Ratio BTC/ETH: 42.18145994374276
    Fecha: 2020-05-04 23:59:59+00:00 | BTC: 8912.65460539 | ETH: 208.174010942 | Ratio BTC/ETH: 42.81348360950389
    Fecha: 2020-05-05 23:59:59+00:00 | BTC: 9003.07017834 | ETH: 206.774404531 | Ratio BTC/ETH: 43.54054457929895
    Fecha: 2020-05-06 23:59:59+00:00 | BTC: 9268.76208066 | ETH: 204.055782253 | Ratio BTC/ETH: 45.42268774901983
    Fecha: 2020-05-07 23:59:59+00:00 | BTC: 9951.5187451 | ETH: 212.289405787 | Ratio BTC/ETH: 46.877133167374495
    Fecha: 2020-05-08 23:59:59+00:00 | BTC: 9842.66636785 | ETH: 212.991579806 | Ratio BTC/ETH: 46.21152806517064
    Fecha: 2020-05-09 23:59:59+00:00 | BTC: 9593.89673363 | ETH: 211.600123566 | Ratio BTC/ETH: 45.33975014734609
    Fecha: 2020-05-10 23:59:59+00:00 | BTC: 8756.43114193 | ETH: 188.599570436 | Ratio BTC/ETH: 46.42869080606648
    Fecha: 2020-05-11 23:59:59+00:00 | BTC: 8601.79620238 | ETH: 185.91283695 | Ratio BTC/ETH: 46.26789813708987
    Fecha: 2020-05-12 23:59:59+00:00 | BTC: 8804.47781074 | ETH: 189.312502269 | Ratio BTC/ETH: 46.50764056897545
    Fecha: 2020-05-13 23:59:59+00:00 | BTC: 9269.98770576 | ETH: 199.193283428 | Ratio BTC/ETH: 46.53765200426907
    Fecha: 2020-05-14 23:59:59+00:00 | BTC: 9733.72147137 | ETH: 202.949100772 | Ratio BTC/ETH: 47.961392459211716
    Fecha: 2020-05-15 23:59:59+00:00 | BTC: 9328.19722645 | ETH: 195.622658341 | Ratio BTC/ETH: 47.68464607095532
    Fecha: 2020-05-16 23:59:59+00:00 | BTC: 9377.0140257 | ETH: 200.677118596 | Ratio BTC/ETH: 46.72687195881886
    Fecha: 2020-05-17 23:59:59+00:00 | BTC: 9670.73937122 | ETH: 207.158694333 | Ratio BTC/ETH: 46.682758849959924
    Fecha: 2020-05-18 23:59:59+00:00 | BTC: 9726.5748149 | ETH: 214.525055208 | Ratio BTC/ETH: 45.34004107571151
    Fecha: 2020-05-19 23:59:59+00:00 | BTC: 9729.0379192 | ETH: 213.451110911 | Ratio BTC/ETH: 45.57970149547075
    Fecha: 2020-05-20 23:59:59+00:00 | BTC: 9522.98115678 | ETH: 210.096735593 | Ratio BTC/ETH: 45.326649792541026
    Fecha: 2020-05-21 23:59:59+00:00 | BTC: 9081.76202252 | ETH: 199.883605552 | Ratio BTC/ETH: 45.435252168079224
    Fecha: 2020-05-22 23:59:59+00:00 | BTC: 9182.57751787 | ETH: 207.169194624 | Ratio BTC/ETH: 44.32404892308358
    Fecha: 2020-05-23 23:59:59+00:00 | BTC: 9209.28742769 | ETH: 208.694402844 | Ratio BTC/ETH: 44.128099758257456
    Fecha: 2020-05-24 23:59:59+00:00 | BTC: 8790.36800074 | ETH: 202.370350969 | Ratio BTC/ETH: 43.43703491469731
    Fecha: 2020-05-25 23:59:59+00:00 | BTC: 8906.93476142 | ETH: 205.319750096 | Ratio BTC/ETH: 43.38079876512339
    Fecha: 2020-05-26 23:59:59+00:00 | BTC: 8835.05306073 | ETH: 201.902309998 | Ratio BTC/ETH: 43.75904892231059
    Fecha: 2020-05-27 23:59:59+00:00 | BTC: 9181.01794762 | ETH: 208.863429364 | Ratio BTC/ETH: 43.95703917903041
    Fecha: 2020-05-28 23:59:59+00:00 | BTC: 9525.7510947 | ETH: 219.840431324 | Ratio BTC/ETH: 43.33029660345318
    Fecha: 2020-05-29 23:59:59+00:00 | BTC: 9439.12439045 | ETH: 220.675124275 | Ratio BTC/ETH: 42.77384875826417
    Fecha: 2020-05-30 23:59:59+00:00 | BTC: 9700.41407169 | ETH: 242.345590189 | Ratio BTC/ETH: 40.027194487528575
    Fecha: 2020-05-31 23:59:59+00:00 | BTC: 9461.05891806 | ETH: 230.975700856 | Ratio BTC/ETH: 40.96127377467478
    Fecha: 2020-06-01 23:59:59+00:00 | BTC: 10167.2681012 | ETH: 246.991760327 | Ratio BTC/ETH: 41.16440195308232
    Fecha: 2020-06-02 23:59:59+00:00 | BTC: 9529.80414872 | ETH: 237.219061533 | Ratio BTC/ETH: 40.17301176024715
    Fecha: 2020-06-03 23:59:59+00:00 | BTC: 9656.71776526 | ETH: 244.179324047 | Ratio BTC/ETH: 39.54764721767049
    Fecha: 2020-06-04 23:59:59+00:00 | BTC: 9800.63659532 | ETH: 244.426387575 | Ratio BTC/ETH: 40.096475231475424
    Fecha: 2020-06-05 23:59:59+00:00 | BTC: 9665.53278908 | ETH: 241.221991758 | Ratio BTC/ETH: 40.069036486427436
    Fecha: 2020-06-06 23:59:59+00:00 | BTC: 9653.67926335 | ETH: 241.931320121 | Ratio BTC/ETH: 39.90256101823357
    Fecha: 2020-06-07 23:59:59+00:00 | BTC: 9758.8524174 | ETH: 245.167259144 | Ratio BTC/ETH: 39.80487627700768
    Fecha: 2020-06-08 23:59:59+00:00 | BTC: 9771.48948366 | ETH: 246.309898559 | Ratio BTC/ETH: 39.67152575201674
    Fecha: 2020-06-09 23:59:59+00:00 | BTC: 9795.70019463 | ETH: 244.911453825 | Ratio BTC/ETH: 39.99690517385707
    Fecha: 2020-06-10 23:59:59+00:00 | BTC: 9870.09445278 | ETH: 247.444943732 | Ratio BTC/ETH: 39.8880425840101
    Fecha: 2020-06-11 23:59:59+00:00 | BTC: 9321.78129819 | ETH: 231.702669421 | Ratio BTC/ETH: 40.23165258080163
    Fecha: 2020-06-12 23:59:59+00:00 | BTC: 9480.84378943 | ETH: 237.493210284 | Ratio BTC/ETH: 39.92048352916103
    Fecha: 2020-06-13 23:59:59+00:00 | BTC: 9475.27733834 | ETH: 238.908842797 | Ratio BTC/ETH: 39.66063887551918
    Fecha: 2020-06-14 23:59:59+00:00 | BTC: 9386.78789214 | ETH: 234.114695213 | Ratio BTC/ETH: 40.094825673372625
    Fecha: 2020-06-15 23:59:59+00:00 | BTC: 9450.70198692 | ETH: 229.928901759 | Ratio BTC/ETH: 41.10271442441696
    Fecha: 2020-06-16 23:59:59+00:00 | BTC: 9538.0243743 | ETH: 234.416174104 | Ratio BTC/ETH: 40.688422677133204
    Fecha: 2020-06-17 23:59:59+00:00 | BTC: 9480.25536624 | ETH: 233.028279483 | Ratio BTC/ETH: 40.68285354581442
    Fecha: 2020-06-18 23:59:59+00:00 | BTC: 9411.84046197 | ETH: 232.101162633 | Ratio BTC/ETH: 40.55059593498059
    Fecha: 2020-06-19 23:59:59+00:00 | BTC: 9288.01871603 | ETH: 227.138289785 | Ratio BTC/ETH: 40.89147067551519
    Fecha: 2020-06-20 23:59:59+00:00 | BTC: 9332.340762 | ETH: 229.274256792 | Ratio BTC/ETH: 40.703831701726536
    Fecha: 2020-06-21 23:59:59+00:00 | BTC: 9303.62971409 | ETH: 228.989820504 | Ratio BTC/ETH: 40.62901003028423
    Fecha: 2020-06-22 23:59:59+00:00 | BTC: 9648.71760979 | ETH: 242.53319314 | Ratio BTC/ETH: 39.78308076049767
    Fecha: 2020-06-23 23:59:59+00:00 | BTC: 9629.65836578 | ETH: 244.142144306 | Ratio BTC/ETH: 39.44283521041944
    Fecha: 2020-06-24 23:59:59+00:00 | BTC: 9313.61034868 | ETH: 235.772462091 | Ratio BTC/ETH: 39.50253675123972
    Fecha: 2020-06-25 23:59:59+00:00 | BTC: 9264.81304308 | ETH: 232.944486695 | Ratio BTC/ETH: 39.7726221149447
    Fecha: 2020-06-26 23:59:59+00:00 | BTC: 9162.91760386 | ETH: 229.66803925 | Ratio BTC/ETH: 39.89635490328679
    Fecha: 2020-06-27 23:59:59+00:00 | BTC: 9045.39095672 | ETH: 222.959785939 | Ratio BTC/ETH: 40.56960728870966
    Fecha: 2020-06-28 23:59:59+00:00 | BTC: 9143.58219104 | ETH: 225.347168434 | Ratio BTC/ETH: 40.57553620301196
    Fecha: 2020-06-29 23:59:59+00:00 | BTC: 9190.85446467 | ETH: 228.194866701 | Ratio BTC/ETH: 40.276341871934505
    Fecha: 2020-06-30 23:59:59+00:00 | BTC: 9137.99340026 | ETH: 226.314997358 | Ratio BTC/ETH: 40.37732146316808
    Fecha: 2020-07-01 23:59:59+00:00 | BTC: 9228.32559024 | ETH: 231.113421712 | Ratio BTC/ETH: 39.92985574736459
    Fecha: 2020-07-02 23:59:59+00:00 | BTC: 9123.41015432 | ETH: 229.392201582 | Ratio BTC/ETH: 39.77210250130795
    Fecha: 2020-07-03 23:59:59+00:00 | BTC: 9087.30391103 | ETH: 225.387063259 | Ratio BTC/ETH: 40.31865795503741
    Fecha: 2020-07-04 23:59:59+00:00 | BTC: 9132.48795051 | ETH: 229.074112293 | Ratio BTC/ETH: 39.866957724271266
    Fecha: 2020-07-05 23:59:59+00:00 | BTC: 9073.94286936 | ETH: 227.664598709 | Ratio BTC/ETH: 39.85662646197479
    Fecha: 2020-07-06 23:59:59+00:00 | BTC: 9375.47475925 | ETH: 241.510225122 | Ratio BTC/ETH: 38.82019800409667
    Fecha: 2020-07-07 23:59:59+00:00 | BTC: 9252.27750386 | ETH: 239.075528329 | Ratio BTC/ETH: 38.70022820205849
    Fecha: 2020-07-08 23:59:59+00:00 | BTC: 9428.3330848 | ETH: 246.670015358 | Ratio BTC/ETH: 38.22245306595681
    Fecha: 2020-07-09 23:59:59+00:00 | BTC: 9277.96790642 | ETH: 243.015967829 | Ratio BTC/ETH: 38.17842913494685
    Fecha: 2020-07-10 23:59:59+00:00 | BTC: 9278.8078672 | ETH: 240.984985207 | Ratio BTC/ETH: 38.503676315060616
    Fecha: 2020-07-11 23:59:59+00:00 | BTC: 9240.34632654 | ETH: 239.45817693 | Ratio BTC/ETH: 38.5885604117048
    Fecha: 2020-07-12 23:59:59+00:00 | BTC: 9276.49985018 | ETH: 242.131695235 | Ratio BTC/ETH: 38.31179491465059
    Fecha: 2020-07-13 23:59:59+00:00 | BTC: 9243.61385509 | ETH: 239.60458484 | Ratio BTC/ETH: 38.5786184403048
    Fecha: 2020-07-14 23:59:59+00:00 | BTC: 9243.21341642 | ETH: 240.211494177 | Ratio BTC/ETH: 38.47948012682995
    Fecha: 2020-07-15 23:59:59+00:00 | BTC: 9192.83736784 | ETH: 238.423526948 | Ratio BTC/ETH: 38.556754383743986
    Fecha: 2020-07-16 23:59:59+00:00 | BTC: 9132.22786293 | ETH: 233.640883013 | Ratio BTC/ETH: 39.08660053481254
    Fecha: 2020-07-17 23:59:59+00:00 | BTC: 9151.39223963 | ETH: 232.773085613 | Ratio BTC/ETH: 39.314649352738186
    Fecha: 2020-07-18 23:59:59+00:00 | BTC: 9159.03990531 | ETH: 235.483805219 | Ratio BTC/ETH: 38.894563882183284
    Fecha: 2020-07-19 23:59:59+00:00 | BTC: 9185.81691242 | ETH: 238.487523715 | Ratio BTC/ETH: 38.51697048688105
    Fecha: 2020-07-20 23:59:59+00:00 | BTC: 9164.2313647 | ETH: 236.153167708 | Ratio BTC/ETH: 38.806302933151585
    Fecha: 2020-07-21 23:59:59+00:00 | BTC: 9374.88752808 | ETH: 245.01672849 | Ratio BTC/ETH: 38.26223452519334
    Fecha: 2020-07-22 23:59:59+00:00 | BTC: 9525.36344997 | ETH: 262.190656292 | Ratio BTC/ETH: 36.32991192242055
    Fecha: 2020-07-23 23:59:59+00:00 | BTC: 9581.07201141 | ETH: 274.689049046 | Ratio BTC/ETH: 34.879701410322824
    Fecha: 2020-07-24 23:59:59+00:00 | BTC: 9536.89268563 | ETH: 279.215409484 | Ratio BTC/ETH: 34.15603996661401
    Fecha: 2020-07-25 23:59:59+00:00 | BTC: 9677.11349729 | ETH: 304.056761197 | Ratio BTC/ETH: 31.826667689261303
    Fecha: 2020-07-26 23:59:59+00:00 | BTC: 9905.16724705 | ETH: 309.643609292 | Ratio BTC/ETH: 31.98892839964681
    Fecha: 2020-07-27 23:59:59+00:00 | BTC: 10990.8733998 | ETH: 321.514088181 | Ratio BTC/ETH: 34.18473343417712
    Fecha: 2020-07-28 23:59:59+00:00 | BTC: 10912.8230505 | ETH: 316.657252341 | Ratio BTC/ETH: 34.46257102852728
    Fecha: 2020-07-29 23:59:59+00:00 | BTC: 11100.4681253 | ETH: 318.190884419 | Ratio BTC/ETH: 34.88619149341402
    Fecha: 2020-07-30 23:59:59+00:00 | BTC: 11111.2142899 | ETH: 334.586629282 | Ratio BTC/ETH: 33.20878157547391
    Fecha: 2020-07-31 23:59:59+00:00 | BTC: 11323.4664207 | ETH: 345.554649307 | Ratio BTC/ETH: 32.768959825627846
    Fecha: 2020-08-01 23:59:59+00:00 | BTC: 11759.5927707 | ETH: 385.199719325 | Ratio BTC/ETH: 30.528560070881614
    Fecha: 2020-08-02 23:59:59+00:00 | BTC: 11053.613901 | ETH: 370.671711492 | Ratio BTC/ETH: 29.82049495093063
    Fecha: 2020-08-03 23:59:59+00:00 | BTC: 11246.3487749 | ETH: 386.295173437 | Ratio BTC/ETH: 29.113355662296776
    Fecha: 2020-08-04 23:59:59+00:00 | BTC: 11205.8929179 | ETH: 389.875485136 | Ratio BTC/ETH: 28.74223526516692
    Fecha: 2020-08-05 23:59:59+00:00 | BTC: 11747.0228312 | ETH: 401.59058634 | Ratio BTC/ETH: 29.251240519006036
    Fecha: 2020-08-06 23:59:59+00:00 | BTC: 11779.7732574 | ETH: 394.961957147 | Ratio BTC/ETH: 29.825083262425988
    Fecha: 2020-08-07 23:59:59+00:00 | BTC: 11601.4727146 | ETH: 379.512855039 | Ratio BTC/ETH: 30.569380089662037
    Fecha: 2020-08-08 23:59:59+00:00 | BTC: 11754.0458135 | ETH: 393.987376065 | Ratio BTC/ETH: 29.833559468059757
    Fecha: 2020-08-09 23:59:59+00:00 | BTC: 11675.7393433 | ETH: 391.120454943 | Ratio BTC/ETH: 29.852029459828596
    Fecha: 2020-08-10 23:59:59+00:00 | BTC: 11878.1113253 | ETH: 395.887569508 | Ratio BTC/ETH: 30.003749145399652
    Fecha: 2020-08-11 23:59:59+00:00 | BTC: 11410.5256775 | ETH: 380.384068285 | Ratio BTC/ETH: 29.99738061834584
    Fecha: 2020-08-12 23:59:59+00:00 | BTC: 11584.9345762 | ETH: 391.024162058 | Ratio BTC/ETH: 29.627157859573966
    Fecha: 2020-08-13 23:59:59+00:00 | BTC: 11784.1373895 | ETH: 428.741782282 | Ratio BTC/ETH: 27.48539535096936
    Fecha: 2020-08-14 23:59:59+00:00 | BTC: 11768.8706193 | ETH: 437.397839521 | Ratio BTC/ETH: 26.906558642786717
    Fecha: 2020-08-15 23:59:59+00:00 | BTC: 11865.69857 | ETH: 433.354926495 | Ratio BTC/ETH: 27.38101690909681
    Fecha: 2020-08-16 23:59:59+00:00 | BTC: 11892.8040631 | ETH: 433.786609983 | Ratio BTC/ETH: 27.41625441957758
    Fecha: 2020-08-17 23:59:59+00:00 | BTC: 12254.4019083 | ETH: 429.531252334 | Ratio BTC/ETH: 28.52970963512354
    Fecha: 2020-08-18 23:59:59+00:00 | BTC: 11991.2332456 | ETH: 423.669315654 | Ratio BTC/ETH: 28.30328466693334
    Fecha: 2020-08-19 23:59:59+00:00 | BTC: 11758.2835921 | ETH: 406.463786824 | Ratio BTC/ETH: 28.928243974638193
    Fecha: 2020-08-20 23:59:59+00:00 | BTC: 11878.3716211 | ETH: 416.439794883 | Ratio BTC/ETH: 28.52362278306583
    Fecha: 2020-08-21 23:59:59+00:00 | BTC: 11592.4890449 | ETH: 389.126350308 | Ratio BTC/ETH: 29.79106666953896
    Fecha: 2020-08-22 23:59:59+00:00 | BTC: 11681.8255623 | ETH: 395.835141215 | Ratio BTC/ETH: 29.511845579053713
    Fecha: 2020-08-23 23:59:59+00:00 | BTC: 11664.8479948 | ETH: 391.384499842 | Ratio BTC/ETH: 29.804062244440036
    Fecha: 2020-08-24 23:59:59+00:00 | BTC: 11774.5958414 | ETH: 408.144207149 | Ratio BTC/ETH: 28.849106847917316
    Fecha: 2020-08-25 23:59:59+00:00 | BTC: 11366.1350817 | ETH: 384.001043035 | Ratio BTC/ETH: 29.599229710071455
    Fecha: 2020-08-26 23:59:59+00:00 | BTC: 11488.3634896 | ETH: 386.466124211 | Ratio BTC/ETH: 29.726702471152855
    Fecha: 2020-08-27 23:59:59+00:00 | BTC: 11323.3970324 | ETH: 382.632632123 | Ratio BTC/ETH: 29.59339084482479
    Fecha: 2020-08-28 23:59:59+00:00 | BTC: 11542.4997333 | ETH: 395.874666093 | Ratio BTC/ETH: 29.15695476857921
    Fecha: 2020-08-29 23:59:59+00:00 | BTC: 11506.8653177 | ETH: 399.921471038 | Ratio BTC/ETH: 28.77281204190868
    Fecha: 2020-08-30 23:59:59+00:00 | BTC: 11711.506161 | ETH: 428.395717595 | Ratio BTC/ETH: 27.338056100906012
    Fecha: 2020-08-31 23:59:59+00:00 | BTC: 11680.8204905 | ETH: 435.079745266 | Ratio BTC/ETH: 26.847539141033916
    Fecha: 2020-09-01 23:59:59+00:00 | BTC: 11970.4787405 | ETH: 477.051924154 | Ratio BTC/ETH: 25.092611798450136
    Fecha: 2020-09-02 23:59:59+00:00 | BTC: 11414.0337325 | ETH: 440.040506887 | Ratio BTC/ETH: 25.93859781965723
    Fecha: 2020-09-03 23:59:59+00:00 | BTC: 10245.296686 | ETH: 385.671928369 | Ratio BTC/ETH: 26.56479751929881
    Fecha: 2020-09-04 23:59:59+00:00 | BTC: 10511.8138807 | ETH: 388.241140415 | Ratio BTC/ETH: 27.075476518185777
    Fecha: 2020-09-05 23:59:59+00:00 | BTC: 10169.567221 | ETH: 335.260079079 | Ratio BTC/ETH: 30.333367602062946
    Fecha: 2020-09-06 23:59:59+00:00 | BTC: 10280.3517032 | ETH: 353.362265679 | Ratio BTC/ETH: 29.092952761794994
    Fecha: 2020-09-07 23:59:59+00:00 | BTC: 10369.5637386 | ETH: 352.673494754 | Ratio BTC/ETH: 29.402730550627492
    Fecha: 2020-09-08 23:59:59+00:00 | BTC: 10131.5166457 | ETH: 337.602111896 | Ratio BTC/ETH: 30.010228872090302
    Fecha: 2020-09-09 23:59:59+00:00 | BTC: 10242.3477803 | ETH: 351.110016528 | Ratio BTC/ETH: 29.17133461922526
    Fecha: 2020-09-10 23:59:59+00:00 | BTC: 10363.1390401 | ETH: 368.101907072 | Ratio BTC/ETH: 28.15290777092603
    Fecha: 2020-09-11 23:59:59+00:00 | BTC: 10400.9146854 | ETH: 374.695588755 | Ratio BTC/ETH: 27.75830566876725
    Fecha: 2020-09-12 23:59:59+00:00 | BTC: 10442.1706031 | ETH: 387.183109613 | Ratio BTC/ETH: 26.969592277765503
    Fecha: 2020-09-13 23:59:59+00:00 | BTC: 10323.7557975 | ETH: 365.570005047 | Ratio BTC/ETH: 28.2401609950814
    Fecha: 2020-09-14 23:59:59+00:00 | BTC: 10680.8374328 | ETH: 377.268875067 | Ratio BTC/ETH: 28.310942509909324
    Fecha: 2020-09-15 23:59:59+00:00 | BTC: 10796.9509861 | ETH: 364.83921823 | Ratio BTC/ETH: 29.5937236092131
    Fecha: 2020-09-16 23:59:59+00:00 | BTC: 10974.9048915 | ETH: 365.812291316 | Ratio BTC/ETH: 30.0014656479094
    Fecha: 2020-09-17 23:59:59+00:00 | BTC: 10948.9899152 | ETH: 389.019219686 | Ratio BTC/ETH: 28.14511304618205
    Fecha: 2020-09-18 23:59:59+00:00 | BTC: 10944.5858045 | ETH: 384.364541978 | Ratio BTC/ETH: 28.474493896282556
    Fecha: 2020-09-19 23:59:59+00:00 | BTC: 11094.3462761 | ETH: 385.544383604 | Ratio BTC/ETH: 28.7757953374707
    Fecha: 2020-09-20 23:59:59+00:00 | BTC: 10938.2712894 | ETH: 371.052826188 | Ratio BTC/ETH: 29.47901354579077
    Fecha: 2020-09-21 23:59:59+00:00 | BTC: 10462.2596185 | ETH: 341.78607406 | Ratio BTC/ETH: 30.61054973428604
    Fecha: 2020-09-22 23:59:59+00:00 | BTC: 10538.4603213 | ETH: 344.503162317 | Ratio BTC/ETH: 30.59031519601225
    Fecha: 2020-09-23 23:59:59+00:00 | BTC: 10246.18649281 | ETH: 321.11631734 | Ratio BTC/ETH: 31.908021920795985
    Fecha: 2020-09-24 23:59:59+00:00 | BTC: 10760.06625677 | ETH: 349.35558514 | Ratio BTC/ETH: 30.7997545035899
    Fecha: 2020-09-25 23:59:59+00:00 | BTC: 10692.71721234 | ETH: 352.18324474 | Ratio BTC/ETH: 30.36123203485708
    Fecha: 2020-09-26 23:59:59+00:00 | BTC: 10750.72357903 | ETH: 355.48809037 | Ratio BTC/ETH: 30.24214838770099
    Fecha: 2020-09-27 23:59:59+00:00 | BTC: 10775.26937624 | ETH: 357.43849724 | Ratio BTC/ETH: 30.145799793369786
    Fecha: 2020-09-28 23:59:59+00:00 | BTC: 10709.65218175 | ETH: 355.15942359 | Ratio BTC/ETH: 30.154492519149205
    Fecha: 2020-09-29 23:59:59+00:00 | BTC: 10844.64098118 | ETH: 359.75739393 | Ratio BTC/ETH: 30.144317154160014
    Fecha: 2020-09-30 23:59:59+00:00 | BTC: 10784.49157795 | ETH: 359.93787376 | Ratio BTC/ETH: 29.962091694582
    Fecha: 2020-10-01 23:59:59+00:00 | BTC: 10619.45190766 | ETH: 353.20591482 | Ratio BTC/ETH: 30.065894884778086
    Fecha: 2020-10-02 23:59:59+00:00 | BTC: 10575.97504191 | ETH: 346.2389138 | Ratio BTC/ETH: 30.54531024788006
    Fecha: 2020-10-03 23:59:59+00:00 | BTC: 10549.32889962 | ETH: 346.52208572 | Ratio BTC/ETH: 30.44345320068334
    Fecha: 2020-10-04 23:59:59+00:00 | BTC: 10669.58254327 | ETH: 352.5790067 | Ratio BTC/ETH: 30.261536678354936
    Fecha: 2020-10-05 23:59:59+00:00 | BTC: 10793.33942751 | ETH: 353.95677154 | Ratio BTC/ETH: 30.493383077685422
    Fecha: 2020-10-06 23:59:59+00:00 | BTC: 10604.40588882 | ETH: 340.81584538 | Ratio BTC/ETH: 31.11476779196222
    Fecha: 2020-10-07 23:59:59+00:00 | BTC: 10668.96895539 | ETH: 341.80866898 | Ratio BTC/ETH: 31.213277847011735
    Fecha: 2020-10-08 23:59:59+00:00 | BTC: 10915.68573098 | ETH: 350.76615934 | Ratio BTC/ETH: 31.119551987337957
    Fecha: 2020-10-09 23:59:59+00:00 | BTC: 11064.45759247 | ETH: 365.59047723 | Ratio BTC/ETH: 30.264621978950338
    Fecha: 2020-10-10 23:59:59+00:00 | BTC: 11296.3614282 | ETH: 370.96758819 | Ratio BTC/ETH: 30.451073861510228
    Fecha: 2020-10-11 23:59:59+00:00 | BTC: 11384.1819535 | ETH: 375.14204941 | Ratio BTC/ETH: 30.34632340310645
    Fecha: 2020-10-12 23:59:59+00:00 | BTC: 11555.3628878 | ETH: 387.7312655 | Ratio BTC/ETH: 29.80250476550749
    Fecha: 2020-10-13 23:59:59+00:00 | BTC: 11425.8994007 | ETH: 381.19076126 | Ratio BTC/ETH: 29.974229603394562
    Fecha: 2020-10-14 23:59:59+00:00 | BTC: 11429.50688675 | ETH: 379.48403791 | Ratio BTC/ETH: 30.118544510324487
    Fecha: 2020-10-15 23:59:59+00:00 | BTC: 11495.34965037 | ETH: 377.44184574 | Ratio BTC/ETH: 30.455949121996788
    Fecha: 2020-10-16 23:59:59+00:00 | BTC: 11322.12268618 | ETH: 366.22901728 | Ratio BTC/ETH: 30.915416725495795
    Fecha: 2020-10-17 23:59:59+00:00 | BTC: 11358.10156733 | ETH: 368.85594038 | Ratio BTC/ETH: 30.79278472681975
    Fecha: 2020-10-18 23:59:59+00:00 | BTC: 11483.35971184 | ETH: 378.21369795 | Ratio BTC/ETH: 30.362093636698756
    Fecha: 2020-10-19 23:59:59+00:00 | BTC: 11742.03715033 | ETH: 379.93560927 | Ratio BTC/ETH: 30.905334651023878
    Fecha: 2020-10-20 23:59:59+00:00 | BTC: 11916.33514058 | ETH: 369.13691491 | Ratio BTC/ETH: 32.28161329647929
    Fecha: 2020-10-21 23:59:59+00:00 | BTC: 12823.68918938 | ETH: 392.18996695 | Ratio BTC/ETH: 32.69764723740341
    Fecha: 2020-10-22 23:59:59+00:00 | BTC: 12965.89129043 | ETH: 413.77299269 | Ratio BTC/ETH: 31.33576023446287
    Fecha: 2020-10-23 23:59:59+00:00 | BTC: 12931.53902256 | ETH: 409.76669164 | Ratio BTC/ETH: 31.55829716369672
    Fecha: 2020-10-24 23:59:59+00:00 | BTC: 13108.06261161 | ETH: 412.45761883 | Ratio BTC/ETH: 31.780386670497325
    Fecha: 2020-10-25 23:59:59+00:00 | BTC: 13031.17431056 | ETH: 406.2177613 | Ratio BTC/ETH: 32.079282473658786
    Fecha: 2020-10-26 23:59:59+00:00 | BTC: 13075.24769656 | ETH: 393.88831313 | Ratio BTC/ETH: 33.19531770988242
    Fecha: 2020-10-27 23:59:59+00:00 | BTC: 13654.21844012 | ETH: 403.99704505 | Ratio BTC/ETH: 33.79781760143842
    Fecha: 2020-10-28 23:59:59+00:00 | BTC: 13271.28536861 | ETH: 388.65077072 | Ratio BTC/ETH: 34.14707075975717
    Fecha: 2020-10-29 23:59:59+00:00 | BTC: 13437.8832414 | ETH: 386.7301135 | Ratio BTC/ETH: 34.7474447225843
    Fecha: 2020-10-30 23:59:59+00:00 | BTC: 13546.52226938 | ETH: 382.81999199 | Ratio BTC/ETH: 35.386141144200906
    Fecha: 2020-10-31 23:59:59+00:00 | BTC: 13780.99470249 | ETH: 386.59033529 | Ratio BTC/ETH: 35.64754067675337
    Fecha: 2020-11-01 23:59:59+00:00 | BTC: 13737.10982864 | ETH: 396.35818693 | Ratio BTC/ETH: 34.65832240035471
    Fecha: 2020-11-02 23:59:59+00:00 | BTC: 13550.4893841 | ETH: 383.15673256 | Ratio BTC/ETH: 35.365395496418884
    Fecha: 2020-11-03 23:59:59+00:00 | BTC: 13950.30084729 | ETH: 387.60217328 | Ratio BTC/ETH: 35.991286450327614
    Fecha: 2020-11-04 23:59:59+00:00 | BTC: 14133.70715301 | ETH: 402.14199843 | Ratio BTC/ETH: 35.14606086454366
    Fecha: 2020-11-05 23:59:59+00:00 | BTC: 15579.84846029 | ETH: 414.06733818 | Ratio BTC/ETH: 37.62636417730987
    Fecha: 2020-11-06 23:59:59+00:00 | BTC: 15565.88058083 | ETH: 454.71929029 | Ratio BTC/ETH: 34.23184569738127
    Fecha: 2020-11-07 23:59:59+00:00 | BTC: 14833.7541075 | ETH: 435.71313513 | Ratio BTC/ETH: 34.04477145972242
    Fecha: 2020-11-08 23:59:59+00:00 | BTC: 15479.56703842 | ETH: 453.55478553 | Ratio BTC/ETH: 34.129431619449015
    Fecha: 2020-11-09 23:59:59+00:00 | BTC: 15332.31559743 | ETH: 444.16305707 | Ratio BTC/ETH: 34.51956517629433
    Fecha: 2020-11-10 23:59:59+00:00 | BTC: 15290.90268148 | ETH: 449.67962112 | Ratio BTC/ETH: 34.003992983705885
    Fecha: 2020-11-11 23:59:59+00:00 | BTC: 15701.33973237 | ETH: 462.96052774 | Ratio BTC/ETH: 33.91507221796654
    Fecha: 2020-11-12 23:59:59+00:00 | BTC: 16276.34394919 | ETH: 461.00527114 | Ratio BTC/ETH: 35.30619923052275
    Fecha: 2020-11-13 23:59:59+00:00 | BTC: 16317.80819009 | ETH: 474.62642092 | Ratio BTC/ETH: 34.38031991236414
    Fecha: 2020-11-14 23:59:59+00:00 | BTC: 16068.13870685 | ETH: 460.14983674 | Ratio BTC/ETH: 34.919361964109605
    Fecha: 2020-11-15 23:59:59+00:00 | BTC: 15955.58743887 | ETH: 447.55909533 | Ratio BTC/ETH: 35.65023614838041
    Fecha: 2020-11-16 23:59:59+00:00 | BTC: 16716.11132377 | ETH: 459.94031258 | Ratio BTC/ETH: 36.34408827963405
    Fecha: 2020-11-17 23:59:59+00:00 | BTC: 17645.40576746 | ETH: 480.36008258 | Ratio BTC/ETH: 36.73370541675121
    Fecha: 2020-11-18 23:59:59+00:00 | BTC: 17804.00563217 | ETH: 479.48406975 | Ratio BTC/ETH: 37.13158946334317
    Fecha: 2020-11-19 23:59:59+00:00 | BTC: 17817.09024754 | ETH: 471.63041968 | Ratio BTC/ETH: 37.77765280625633
    Fecha: 2020-11-20 23:59:59+00:00 | BTC: 18621.31436938 | ETH: 509.74457334 | Ratio BTC/ETH: 36.53067701607403
    Fecha: 2020-11-21 23:59:59+00:00 | BTC: 18642.23276593 | ETH: 549.48662086 | Ratio BTC/ETH: 33.92663635149677
    Fecha: 2020-11-22 23:59:59+00:00 | BTC: 18370.00252365 | ETH: 558.06809523 | Ratio BTC/ETH: 32.91713445126989
    Fecha: 2020-11-23 23:59:59+00:00 | BTC: 18364.12159134 | ETH: 608.45402857 | Ratio BTC/ETH: 30.18160901079035
    Fecha: 2020-11-24 23:59:59+00:00 | BTC: 19107.46444977 | ETH: 603.89774601 | Ratio BTC/ETH: 31.640231439866305
    Fecha: 2020-11-25 23:59:59+00:00 | BTC: 18732.1207774 | ETH: 570.68661621 | Ratio BTC/ETH: 32.82383053207436
    Fecha: 2020-11-26 23:59:59+00:00 | BTC: 17150.62357809 | ETH: 518.80117389 | Ratio BTC/ETH: 33.058181903278424
    Fecha: 2020-11-27 23:59:59+00:00 | BTC: 17108.40172774 | ETH: 517.49368769 | Ratio BTC/ETH: 33.060116740957504
    Fecha: 2020-11-28 23:59:59+00:00 | BTC: 17717.4150112 | ETH: 538.22980058 | Ratio BTC/ETH: 32.91793763947592
    Fecha: 2020-11-29 23:59:59+00:00 | BTC: 18177.48341979 | ETH: 575.75804789 | Ratio BTC/ETH: 31.571392682057407
    Fecha: 2020-11-30 23:59:59+00:00 | BTC: 19625.83502949 | ETH: 614.84252202 | Ratio BTC/ETH: 31.920100394181254
    Fecha: 2020-12-01 23:59:59+00:00 | BTC: 18802.99829969 | ETH: 587.32418713 | Ratio BTC/ETH: 32.01468407349635
    Fecha: 2020-12-02 23:59:59+00:00 | BTC: 19201.09115697 | ETH: 598.35234223 | Ratio BTC/ETH: 32.08994066173358
    Fecha: 2020-12-03 23:59:59+00:00 | BTC: 19445.39847988 | ETH: 616.70875486 | Ratio BTC/ETH: 31.53092659483054
    Fecha: 2020-12-04 23:59:59+00:00 | BTC: 18699.76561337 | ETH: 569.35419749 | Ratio BTC/ETH: 32.84381795340753
    Fecha: 2020-12-05 23:59:59+00:00 | BTC: 19154.231131 | ETH: 596.59547474 | Ratio BTC/ETH: 32.1058940974159
    Fecha: 2020-12-06 23:59:59+00:00 | BTC: 19345.12095871 | ETH: 601.90899244 | Ratio BTC/ETH: 32.139611140031896
    Fecha: 2020-12-07 23:59:59+00:00 | BTC: 19191.63128698 | ETH: 591.84337934 | Ratio BTC/ETH: 32.42687500936774
    Fecha: 2020-12-08 23:59:59+00:00 | BTC: 18321.14491611 | ETH: 554.82775708 | Ratio BTC/ETH: 33.02132000845137
    Fecha: 2020-12-09 23:59:59+00:00 | BTC: 18553.91537685 | ETH: 573.47911163 | Ratio BTC/ETH: 32.35325402544165
    Fecha: 2020-12-10 23:59:59+00:00 | BTC: 18264.99210672 | ETH: 559.67850106 | Ratio BTC/ETH: 32.63479313950263
    Fecha: 2020-12-11 23:59:59+00:00 | BTC: 18058.90334725 | ETH: 545.79734103 | Ratio BTC/ETH: 33.08719553886098
    Fecha: 2020-12-12 23:59:59+00:00 | BTC: 18803.65687045 | ETH: 568.56731778 | Ratio BTC/ETH: 33.07199742656653
    Fecha: 2020-12-13 23:59:59+00:00 | BTC: 19142.3825335 | ETH: 589.6632225 | Ratio BTC/ETH: 32.463246482190094
    Fecha: 2020-12-14 23:59:59+00:00 | BTC: 19246.64434137 | ETH: 586.01115197 | Ratio BTC/ETH: 32.8434779383777
    Fecha: 2020-12-15 23:59:59+00:00 | BTC: 19417.07603342 | ETH: 589.35560245 | Ratio BTC/ETH: 32.946282266091316
    Fecha: 2020-12-16 23:59:59+00:00 | BTC: 21310.59813054 | ETH: 636.18184867 | Ratio BTC/ETH: 33.49765192938446
    Fecha: 2020-12-17 23:59:59+00:00 | BTC: 22805.16149213 | ETH: 642.86896702 | Ratio BTC/ETH: 35.47404317530312
    Fecha: 2020-12-18 23:59:59+00:00 | BTC: 23137.96056165 | ETH: 654.81192689 | Ratio BTC/ETH: 35.33527660612828
    Fecha: 2020-12-19 23:59:59+00:00 | BTC: 23869.83196434 | ETH: 659.29792646 | Ratio BTC/ETH: 36.20492497603539
    Fecha: 2020-12-20 23:59:59+00:00 | BTC: 23477.29519711 | ETH: 638.29084637 | Ratio BTC/ETH: 36.781500675791996
    Fecha: 2020-12-21 23:59:59+00:00 | BTC: 22803.0814087 | ETH: 609.81787165 | Ratio BTC/ETH: 37.39326521704113
    Fecha: 2020-12-22 23:59:59+00:00 | BTC: 23783.02850288 | ETH: 634.85419947 | Ratio BTC/ETH: 37.462189779535144
    Fecha: 2020-12-23 23:59:59+00:00 | BTC: 23241.34486501 | ETH: 583.71459689 | Ratio BTC/ETH: 39.81628177338486
    Fecha: 2020-12-24 23:59:59+00:00 | BTC: 23735.94972763 | ETH: 611.60718693 | Ratio BTC/ETH: 38.809141283597505
    Fecha: 2020-12-25 23:59:59+00:00 | BTC: 24664.79027412 | ETH: 626.41070163 | Ratio BTC/ETH: 39.37479070829904
    Fecha: 2020-12-26 23:59:59+00:00 | BTC: 26437.0375091 | ETH: 635.83583086 | Ratio BTC/ETH: 41.57840157158582
    Fecha: 2020-12-27 23:59:59+00:00 | BTC: 26272.29456706 | ETH: 682.6423591 | Ratio BTC/ETH: 38.48617686382304
    Fecha: 2020-12-28 23:59:59+00:00 | BTC: 27084.80788628 | ETH: 730.39736483 | Ratio BTC/ETH: 37.08229135326082
    Fecha: 2020-12-29 23:59:59+00:00 | BTC: 27362.4365573 | ETH: 731.52011874 | Ratio BTC/ETH: 37.4048995459348
    Fecha: 2020-12-30 23:59:59+00:00 | BTC: 28840.95341968 | ETH: 751.61897194 | Ratio BTC/ETH: 38.37177412544385
    Fecha: 2020-12-31 23:59:59+00:00 | BTC: 29001.71982218 | ETH: 737.80339769 | Ratio BTC/ETH: 39.308194992028945



```python

```
