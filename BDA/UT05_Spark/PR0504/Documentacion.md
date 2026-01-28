# PR0503. Limpieza de datos sobre dataset de lugares famosos

Seguimos trabajando con dataframes en PySpark. En esta ocasión el objetivo es transformar datos crudos de destinos turísticos para limpieza de texto, cálculos matemáticos avanzados y gestión de fechas.

Supón que en la empresa en la que estás trabajando está preparando un catálogo turístico y el departamento de marketing necesita un dataset enriquecido con códigos cortos para la app móvil, precios ajustados psicológicamente y fechas límite para ofertas promocionales.

Trabajarás sobre el archivo el mismo dataset de la práctica anterior.


```python
from pyspark.sql import SparkSession

spark = ( SparkSession.builder
            .appName("Haciendo pruebas")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
print("SparkSession iniciada correctamente.")
```

    SparkSession iniciada correctamente.



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

    26/01/28 11:05:35 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors


    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |   Place_Name|      Country|         City|Annual_Visitors_Millions|          Type|UNESCO_World_Heritage|Year_Built|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|
    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    | Eiffel Tower|       France|        Paris|                     7.0|Monument/Tower|                   No|      1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|
    | Times Square|United States|New York City|                    50.0|Urban Landmark|                   No|      1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|
    |Louvre Museum|       France|        Paris|                     8.7|        Museum|                  Yes|      1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|
    +-------------+-------------+-------------+------------------------+--------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    only showing top 3 rows
    


## Ejercicio 1: Generación de códigos SKUs

La App móvil no puede mostrar nombres largos. Necesitamos un **SKU (Stock Keeping Unit)** para cada lugar.

Para ello tienes que crear una columna `SKU_Lugar` en un nuevo DataFrame `df_feat`. El formato debe ser `PAIS(3)-CIUDAD(3)-TIPO`. Debes tener en cuenta:

  - **País:** extrae los 3 primeros caracteres del `Country` y conviértelos a mayúsculas (`upper`, `substring`).
  - **Ciudad:** extrae los 3 primeros caracteres de `City`. Si la ciudad tiene menos de 3 letras (raro, pero posible), rellena con 'X' a la derecha (`rpad`).
  - **Tipo:** la columna `Type` a veces tiene barras (ej: "Monument/Tower"). Queremos solo la **primera parte** antes de la barra. Usa `split` para dividir el texto y extrae el primer elemento (índice 0).
  - **Unión:** concatena todo con guiones bajos (`concat_ws`).



```python
from pyspark.sql.functions import col,upper,substring,rpad,split,concat_ws
df_feat = (df_world
              .withColumn("Country",upper(substring(df_world.Country,1,3)))
              .withColumn("City",rpad("City",3,"X"))
              .withColumn("Type",split(col("Type"),"/")[0])
              .withColumn("SKU_Lugar",concat_ws("-",col("Country"),col("City"),col("Type")))
              .select("Country","City","Type","SKU_Lugar")
         )
df_feat.show(3)
```

    +-------+----+--------------+--------------------+
    |Country|City|          Type|           SKU_Lugar|
    +-------+----+--------------+--------------------+
    |    FRA| Par|      Monument|    FRA-Par-Monument|
    |    UNI| New|Urban Landmark|UNI-New-Urban Lan...|
    |    FRA| Par|        Museum|      FRA-Par-Museum|
    +-------+----+--------------+--------------------+
    only showing top 3 rows
    


## Ejercicio 2: Ajuste de precios y tiempos

Necesitamos normalizar las métricas para el algoritmo de recomendación.

Añade las siguientes columnas numéricas:

  - `Duracion_Techo`: la `Average_Visit_Duration_Hours` tiene decimales (2.5 horas). Redondea siempre hacia arriba (`ceil`) para reservar bloques completos en la agenda del turista.
  - `Log_Ingresos`: los ingresos (`Tourism_Revenue_Million_USD`) varían demasiado (de 45 a 180). Aplica una transformación logarítmica (`log10`) para suavizar la escala.
  - `Mejor_Oferta`: compara el `Entry_Fee_USD` actual contra un "Precio de Competencia" simulado (que es siempre 20 USD). Usa la función `least` para quedarte con el precio más bajo de los dos (fila a fila).




```python
from pyspark.sql.functions import col,ceil,log10,least,lit
df_feat = (df_world
              .withColumn("Duracion_Techo",ceil(col("Average_Visit_Duration_Hours")))
              .withColumn("Log_Ingresos",log10(col("Tourism_Revenue_Million_USD")))
              .withColumn("Precio_Competencia",lit(20))
              .withColumn("Mejor_Oferta",least(col("Entry_Fee_USD"),col("Precio_Competencia")))
              .select("Duracion_Techo", "Average_Visit_Duration_Hours","Log_ingresos", "Tourism_Revenue_Million_USD", "Mejor_Oferta", "Entry_Fee_USD")
         )
df_feat.show(3)
```

    +--------------+----------------------------+------------------+---------------------------+------------+-------------+
    |Duracion_Techo|Average_Visit_Duration_Hours|      Log_ingresos|Tourism_Revenue_Million_USD|Mejor_Oferta|Entry_Fee_USD|
    +--------------+----------------------------+------------------+---------------------------+------------+-------------+
    |             3|                         2.5|1.9777236052888478|                         95|          20|           35|
    |             2|                         1.5| 1.845098040014257|                         70|           0|            0|
    |             4|                         4.0|2.0791812460476247|                        120|          20|           22|
    +--------------+----------------------------+------------------+---------------------------+------------+-------------+
    only showing top 3 rows
    


## Ejercicio 3: Limpieza de texto

La columna `Famous_For` es demasiado larga para las notificaciones push.

Haz lo siguiente:

- Crea `Desc_Corta`: extrae solo los primeros 15 caracteres de `Famous_For` (`substring`).
- Crea `Ciudad_Limpia`: reemplaza la cadena "New York City" por "NYC" usando `regexp_replace` en la columna `City`.




```python
from pyspark.sql.functions import col,substring,regexp_replace
df_feat1 = (df_world
              .withColumn("Desc_Corta",substring(col("Famous_for"),1,15))
              .withColumn("Ciudad_Limpia",regexp_replace("City","New York City","NYC"))
              .select("Desc_Corta","Famous_For","Ciudad_Limpia","City")
         )
df_feat1.show(3)
```

    +---------------+--------------------+-------------+-------------+
    |     Desc_Corta|          Famous_For|Ciudad_Limpia|         City|
    +---------------+--------------------+-------------+-------------+
    |Iconic iron lat|Iconic iron latti...|        Paris|        Paris|
    |Bright lights, |Bright lights, Br...|          NYC|New York City|
    |World's most vi|World's most visi...|        Paris|        Paris|
    +---------------+--------------------+-------------+-------------+
    only showing top 3 rows
    


## Ejercicio 4: Gestión de fechas de campaña

Vamos a simular que lanzamos una campaña hoy.

- Crea una columna `Inicio_Campana` usando `to_date` con la fecha "2024-06-01".
- Crea `Fin_Campana`: Suma 90 días a la fecha de inicio (`date_add`).
- Crea `Dias_Hasta_Fin`: Calcula la diferencia en días entre el fin de la campaña y la fecha de construcción del monumento.

**Nota:**

- Como `Year_Built` es un número (ej. 1889), primero deberás crear una fecha ficticia de construcción. Usa `concat` para unir el año con "-01-01" (ej: "1889-01-01") y conviértelo a fecha con `to_date`.
- Si el año tiene texto (como "220 BC"), `to_date` devolverá null, lo cual es correcto para este ejercicio.


```python
from pyspark.sql.functions import col,to_date,date_add,lit,concat,datediff
df_feat1 = (df_world
              .withColumn("Inicio_Campana",to_date(lit("2024-06-01")))
              .withColumn("Fin_Campana",date_add(col("Inicio_Campana"),90))
              .withColumn("Fecha_Construccion",to_date(concat(col("Year_Built"),lit("-01-01"))))
              .withColumn("Dias_Hasta_Fin",datediff(col("Fin_Campana"),col("Fecha_Construccion")))
              .select("Inicio_Campana", "Fin_Campana","Fecha_Construccion","Dias_Hasta_Fin")
         )
df_feat1.show(3)
```

    +--------------+-----------+------------------+--------------+
    |Inicio_Campana|Fin_Campana|Fecha_Construccion|Dias_Hasta_Fin|
    +--------------+-----------+------------------+--------------+
    |    2024-06-01| 2024-08-30|        1889-01-01|         49549|
    |    2024-06-01| 2024-08-30|        1904-01-01|         44072|
    |    2024-06-01| 2024-08-30|        1793-01-01|         84612|
    +--------------+-----------+------------------+--------------+
    only showing top 3 rows
    

