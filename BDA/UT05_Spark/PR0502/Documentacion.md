# PR0502. Manipulación básica de dataframes

Vamos a empezar a realizar operaciones básicas sobre los datasets que cargamos en la anterior práctica.


```python
from pyspark.sql import SparkSession

spark = ( SparkSession.builder
            .appName("Haciendo pruebas")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
print("SparkSession iniciada correctamente.")
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/01/21 11:39:22 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.


## Dataset 1: Datos para la predicción del rendimiento en cultivos


```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema_crop = StructType([
    StructField("Crop", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Soil_Type", StringType(), True),
    StructField("Soil_pH", DoubleType(), True),
    StructField("Rainfall_mm", DoubleType(), True),
    StructField("Temperature_C", DoubleType(), True),
    StructField("Humidity_pct", DoubleType(), True),
    StructField("Fertilizer_Used_kg", DoubleType(), True),
    StructField("Irrigation", StringType(), True),
    StructField("Pesticides_Used_kg", DoubleType(), True),
    StructField("Planting_Density", DoubleType(), True),
    StructField("Previous_Crop", StringType(), True),
    StructField("Yield_ton_per_ha", DoubleType(), True)
])
```


```python
df_crop = ( spark.read
                .format("csv")
                .schema(schema_crop)
                .option("header", "true")
                .load("./crop_yield_dataset.csv")
          )
df_crop.show(3)
```

                                                                                    

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    only showing top 3 rows
    


    26/01/21 11:39:43 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors


### 1.- Selección de características

Crea un nuevo DataFrame llamado `df_sel` que contenga únicamente las columnas: `Crop`, `Region`, `Temperature_C`, `Rainfall_mm`, `Irrigation` y `Yield_ton_per_ha`.



```python
df_sel = (df_crop
              .select("Crop","Region","Temperature_C","Rainfall_mm","Irrigation","Yield_ton_per_ha") 
         )
```


```python
df_sel.show(3)
```

    +------+--------+-------------+-----------+----------+----------------+
    |  Crop|  Region|Temperature_C|Rainfall_mm|Irrigation|Yield_ton_per_ha|
    +------+--------+-------------+-----------+----------+----------------+
    | Maize|Region_C|         19.7|     1485.4|      Drip|          101.48|
    |Barley|Region_D|         29.1|      399.4| Sprinkler|          127.39|
    |  Rice|Region_C|         30.5|      980.9| Sprinkler|           68.99|
    +------+--------+-------------+-----------+----------+----------------+
    only showing top 3 rows
    


### 2.- Normalización de nombres

Los nombres actuales son muy largos y técnicos (tienen unidades). Necesitamos estandarizarlos al español o simplificarlos. Usando el DataFrame `df_sel` del ejercicio anterior, cambia los siguientes nombres:

- `Temperature_C` -> `Temperatura`
- `Rainfall_mm` -> `Lluvia`
- `Yield_ton_per_ha` -> `Rendimiento`

Guarda el resultado en `df_renamed`.


```python
df_renamed = (df_sel
                  .withColumnRenamed("Temperature_C", "Temperatura")
                  .withColumnRenamed("Rainfall_mm", "Lluvia")
                  .withColumnRenamed("Yield_ton_per_ha", "Rendimiento")
             )
df_renamed.show(3)
```

    +------+--------+-----------+------+----------+-----------+
    |  Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
    +------+--------+-----------+------+----------+-----------+
    | Maize|Region_C|       19.7|1485.4|      Drip|     101.48|
    |Barley|Region_D|       29.1| 399.4| Sprinkler|     127.39|
    |  Rice|Region_C|       30.5| 980.9| Sprinkler|      68.99|
    +------+--------+-----------+------+----------+-----------+
    only showing top 3 rows
    


### 3.- Filtrado de datos (`filter`)

Supón que queremos centrarnos en cultivos de **maíz** que han crecido en regiones calurosas (más de 25 grados). Filtra `df_renamed` para mantener solo las filas donde:

- El cultivo (`Crop`) sea igual a "Maize".
- La temperatura (`Temperatura`) sea mayor a 25.


```python
from pyspark.sql.functions import col

(df_renamed
    .filter( (col("Crop") == "Maize") & ( col("Temperatura") > 25 ) )
).show(3)
```

    +-----+--------+-----------+------+----------+-----------+
    | Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
    +-----+--------+-----------+------+----------+-----------+
    |Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
    |Maize|Region_C|       32.4| 846.1|      None|      162.2|
    |Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
    +-----+--------+-----------+------+----------+-----------+
    only showing top 3 rows
    


### 4.- Encadenamiento

En Spark podemos **encadenar** varias funciones. Repite las órdenes anteriores encadenadas en una única sentencia



```python
df_sel = (df_crop
              .select("Crop","Region","Temperature_C","Rainfall_mm","Irrigation","Yield_ton_per_ha")
              .withColumnRenamed("Temperature_C", "Temperatura")
              .withColumnRenamed("Rainfall_mm", "Lluvia")
              .withColumnRenamed("Yield_ton_per_ha", "Rendimiento")
              .filter( (col("Crop") == "Maize") & ( col("Temperatura") > 25 ) )
         ).show(3)
```

    +-----+--------+-----------+------+----------+-----------+
    | Crop|  Region|Temperatura|Lluvia|Irrigation|Rendimiento|
    +-----+--------+-----------+------+----------+-----------+
    |Maize|Region_D|       26.4|1054.3|      Drip|     169.06|
    |Maize|Region_C|       32.4| 846.1|      None|      162.2|
    |Maize|Region_A|       26.6| 362.5| Sprinkler|      95.23|
    +-----+--------+-----------+------+----------+-----------+
    only showing top 3 rows
    


## Dataset 2: Lugares famosos del mundo


```python
from pyspark.sql.types import StructType, StructField, StringType, DecimalType, DoubleType, IntegerType

schema_world = StructType([
    StructField("Place_Name", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("Annual_Visitors_Millions", DoubleType(), True),
    StructField("Type", StringType(), True),
    StructField("UNESCO_World_Heritage", StringType(), True),
    StructField("Year_Built", IntegerType(), True),
    StructField("Entry_Fee_USD", DecimalType(), True),
    StructField("Best_Visit_Month", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Tourism_Revenue_Million_USD", DecimalType(), True),
    StructField("Average_Visit_Duration_Hours", DoubleType(), True),
    StructField("Famous_For", StringType(), True)
])

```


```python
df_world = ( spark.read
                .format("csv")
                .schema(schema_world)
                .option("header", "true")
                .load("./world_famous_places_2024.csv")
           )
df_world.show(3)
```

    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |   Place_Name|      Country|         City|Annual_Visitors_Millions|          Type|UNESCO_World_Heritage|Year_Built|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|
    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    | Eiffel Tower|       France|        Paris|                     7.0|Monument/Tower|                   No|      1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|
    | Times Square|United States|New York City|                    50.0|Urban Landmark|                   No|      1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|
    |Louvre Museum|       France|        Paris|                     8.7|        Museum|                  Yes|      1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|
    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    only showing top 3 rows
    


### 1.- Selección de datos críticos

El dataset tiene mucha información descriptiva que no necesitamos para el análisis cuantitativo (como `Famous_For` o `Best_Visit_Month`).

Crea un nuevo DataFrame llamado `df_base` seleccionando únicamente: `Place_Name`, `Country`, `UNESCO_World_Heritage`, `Entry_Fee_USD` y `Annual_Visitors_Millions`.



```python
df_base = (df_world
               .select( "Place_Name", "Country", "UNESCO_World_Heritage", "Entry_fee_USD", "Annual_Visitors_Millions")
          )
df_base.show(3)
```

    +-------------+-------------+---------------------+-------------+------------------------+
    |   Place_Name|      Country|UNESCO_World_Heritage|Entry_fee_USD|Annual_Visitors_Millions|
    +-------------+-------------+---------------------+-------------+------------------------+
    | Eiffel Tower|       France|                   No|           35|                     7.0|
    | Times Square|United States|                   No|            0|                    50.0|
    |Louvre Museum|       France|                  Yes|           22|                     8.7|
    +-------------+-------------+---------------------+-------------+------------------------+
    only showing top 3 rows
    


### 2.- Traducción y simplificación

Las columnas tienen nombres en inglés y son demasiado largos para los reportes en español. Sobre el DataFrame `df_base`, renombra las columnas de la siguiente manera y guarda el resultado en `df_es`:

- `Place_Name` -> `Lugar`
- `UNESCO_World_Heritage` -> `Es_UNESCO`
- `Entry_Fee_USD` -> `Precio_Entrada`
- `Annual_Visitors_Millions` -> `Visitantes_Millones`



```python
df_es = (df_base
             .withColumnRenamed("Place_Name", "Lugar")
             .withColumnRenamed("UNESCO_World_Heritage", "Es_UNESCO")
             .withColumnRenamed("Entry_Fee_USD", "Precio_Entrada")
             .withColumnRenamed("Annual_Visitors_Millions", "Visitantes_Millones")
        )
df_es.show(3)
```

    +-------------+-------------+---------+--------------+-------------------+
    |        Lugar|      Country|Es_UNESCO|Precio_Entrada|Visitantes_Millones|
    +-------------+-------------+---------+--------------+-------------------+
    | Eiffel Tower|       France|       No|            35|                7.0|
    | Times Square|United States|       No|             0|               50.0|
    |Louvre Museum|       France|      Yes|            22|                8.7|
    +-------------+-------------+---------+--------------+-------------------+
    only showing top 3 rows
    


### 3: Filtrado

Supón que vamos a realizar una campaña y necesitamos filtrar los destinos que cumplan dos condiciones estrictas. Filtra `df_es` para obtener solo los registros que cumplan:

1. Sean Patrimonio de la Humanidad (`Es_UNESCO` es igual a "Yes").
2. El precio de entrada (`Precio_Entrada`) sea menor o igual a **20 dólares**.




```python
(df_es
     .filter( (col("Es_UNESCO") == "Yes") & ( col("Precio_Entrada") <=20))

).show(3)
```

    +-------------------+-------+---------+--------------+-------------------+
    |              Lugar|Country|Es_UNESCO|Precio_Entrada|Visitantes_Millones|
    +-------------------+-------+---------+--------------+-------------------+
    |Great Wall of China|  China|      Yes|            10|               10.0|
    |          Taj Mahal|  India|      Yes|            15|                7.5|
    |          Colosseum|  Italy|      Yes|            18|               7.65|
    +-------------------+-------+---------+--------------+-------------------+
    only showing top 3 rows
    


## Dataset 3: Registro turístico de Castilla y León


```python
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, LongType

schema_cyl = StructType([
    StructField("establecimiento", StringType(), True),
    StructField("n_registro", StringType(), True),
    StructField("codigo", StringType(), True),
    StructField("tipo", StringType(), True),
    StructField("categoria", StringType(), True),
    StructField("especialidades", StringType(), True),
    StructField("clase", StringType(), True),
    StructField("nombre", StringType(), True),
    StructField("direccion", StringType(), True),
    StructField("c_postal", StringType(), True),
    StructField("provincia", StringType(), True),
    StructField("municipio", StringType(), True),
    StructField("localidad", StringType(), True),
    StructField("nucleo", StringType(), True),
    StructField("telefono_1", LongType(), True),
    StructField("telefono_2", LongType(), True),
    StructField("telefono_3", LongType(), True),
    StructField("email", StringType(), True),
    StructField("web", StringType(), True),
    StructField("q_calidad", StringType(), True),
    StructField("posada_real", StringType(), True),
    StructField("plazas", IntegerType(), True),
    StructField("gps_longitud", DoubleType(), True),
    StructField("gps_latitud", DoubleType(), True),
    StructField("accesible_a_personas_con_discapacidad", StringType(), True),
    StructField("column_27", StringType(), True),
    StructField("posicion", StringType(), True)
])

```


```python
df_cyl = ( spark.read
                .format("csv")
                .schema(schema_cyl)
                .option("header", "true")
                .option("sep", ";")
                .load("./registro-de-turismo-de-castilla-y-leon.csv")
           )
df_cyl.show(3)
```

    26/01/21 11:50:52 WARN SparkStringUtils: Truncated the string representation of a plan since it was too large. This behavior can be adjusted by setting 'spark.sql.debug.maxToStringFields'.


    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|  categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|       NULL|          NULL| NULL|BERNARDO MORO MEN...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|POLA DE SOMIEDO|POLA DE SOMIEDO| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|3 Estrellas|          NULL| NULL|        LA SASTRERÍA|Calle VEINTIOCHO ...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|4 Estrellas|          NULL| NULL|         LAS HAZANAS|       Plaza MAYOR 4|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|
    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 3 rows
    


### 1.- Selección y saneamiento

Las columnas originales como `N.Registro` o `GPS.Latitud` tienen puntos, lo cual suele dar problemas en motores SQL o al guardar en Parquet. Además, solo necesitamos datos de contacto.

Crea un `df_contactos` seleccionando únicamente: `Nombre`, `Tipo`, `Provincia`, `web` y `Email`.



```python
df_contactos = (df_cyl
                    .select( "Nombre", "Tipo", "Provincia", "web", "Email")
               )
df_contactos.show(3)
```

    +--------------------+--------------------+---------+--------------------+--------------------+
    |              Nombre|                Tipo|Provincia|                 web|               Email|
    +--------------------+--------------------+---------+--------------------+--------------------+
    |BERNARDO MORO MEN...|Profesional de Tu...| Asturias|                NULL|bernardomoro@hotm...|
    |        LA SASTRERÍA|Casa Rural de Alq...|    Ávila|www.lasastreriade...|                NULL|
    |         LAS HAZANAS|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
    +--------------------+--------------------+---------+--------------------+--------------------+
    only showing top 3 rows
    


### 2.- Renombrado estándar

Vamos a renombrar las columnas para que estén en minúsculas y no tengan ambigüedades

- `Nombre`  `nombre_establecimiento`
- `Tipo`  `categoria_actividad`
- `web`  `sitio_web`
- `Email`  `correo_electronico`

Guarda el resultado en `df_limpio`.


```python
df_limpio = (df_contactos
                 .withColumnRenamed("Nombre", "nombre_establecimiento")
                 .withColumnRenamed("Tipo", "categoria_actividad")
                 .withColumnRenamed("web", "sitio_web")
                 .withColumnRenamed("Email", "correo_electronico")
            )
df_limpio.show(3)
```

    +----------------------+--------------------+---------+--------------------+--------------------+
    |nombre_establecimiento| categoria_actividad|Provincia|           sitio_web|  correo_electronico|
    +----------------------+--------------------+---------+--------------------+--------------------+
    |  BERNARDO MORO MEN...|Profesional de Tu...| Asturias|                NULL|bernardomoro@hotm...|
    |          LA SASTRERÍA|Casa Rural de Alq...|    Ávila|www.lasastreriade...|                NULL|
    |           LAS HAZANAS|Casa Rural de Alq...|    Ávila|                NULL|lashazanas@hotmai...|
    +----------------------+--------------------+---------+--------------------+--------------------+
    only showing top 3 rows
    


### 3: Filtrado de texto

La columna `categoria_actividad` contiene valores sucios como *"g - Bodegas y los complejos de enoturismo"*. No podemos filtrar por igualdad exacta (`==`).

Filtra `df_limpio` para obtener una lista `df_final` que cumpla **todas** estas condiciones simultáneamente:

1. **Ubicación:** la `Provincia` debe ser "Burgos".
2. **Actividad:** la `categoria_actividad` debe contener la palabra "Bodegas" (investiga [`contains`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.contains.html)] o [`like`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.like.html)).
3. **Digitalización:** el `sitio_web` **no** puede estar vacío ni ser nulo (investiga la función [`isNotNull`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.isNotNull.html)).


```python
df_final = (df_limpio
                .filter( col("Provincia") == "Burgos" )
                .filter( col("categoria_actividad").contains("Bodegas") )
              # .filter( col("categoria_actividad").like("%Bodegas%") )
                .filter( col("sitio_web").isNotNull() & (col("sitio_web") != "") )
           )
df_final.show(3)
```

    +----------------------+--------------------+---------+--------------------+--------------------+
    |nombre_establecimiento| categoria_actividad|Provincia|           sitio_web|  correo_electronico|
    +----------------------+--------------------+---------+--------------------+--------------------+
    |        BODEGAS TARSUS|g - Bodegas y los...|   Burgos|  www.tarsusvino.com|                NULL|
    |  BODEGAS DOMINIO D...|g - Bodegas y los...|   Burgos|www.dominiodecair...|bodegas@dominiode...|
    |    TERRITORIO LUTHIER|g - Bodegas y los...|   Burgos|territorioluthier...|luthier@territori...|
    +----------------------+--------------------+---------+--------------------+--------------------+
    only showing top 3 rows
    

