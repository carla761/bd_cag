# PR0506. Análisis de comportamiento de usuarios en Netflix

## Contexto

En esta práctica vamos a trabajar con el *dataset* [**Netflix audience behaviour - IK Movies**](https://www.kaggle.com/datasets/vodclickstream/netflix-audience-behaviour-uk-movies) que abarca el comportamiento en la versión web de los usuarios en Netflix UK entre enero de 2017 y junio de 2019 de forma anonimizada. Este *dataset* documenta cada vez que alguien hizo un click en una URL del tipo netflix.com/watch para ver una película.

Los campos que tiene el *dataset* son:

- `row_id`: identificador de fila
- `click_datetime`: fecha y hora del clic
- `time_to_next_click`: segundos hasta el siguiente clic del usuario
- `movie_title`: título de la película
- `movie_genres`: género/s
- `release_date`: fecha de estreno original
- `title_id`: ID de la película
- `user_id`: ID del usuario


Tu objetivo será utilizar funciones de ventana en PySpark para extraer *insights* sobre cómo los usuarios británicos navegan y consumen películas en la interfaz web de *Netflix.com*.




```python
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

spark = ( SparkSession.builder
            .appName("Ventanas")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
print("SparkSession iniciada correctamente.")
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/03/05 10:10:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.



```python
from pyspark.sql.types import StructType, StructField, DoubleType, LongType,TimestampType,StringType

schema_vnt = StructType([
    StructField("c0_", LongType(), True),
    StructField("datetime", TimestampType(), True),
    StructField("duration", DoubleType(), True),
    StructField("title", StringType(), True),
    StructField("genres", StringType(), True),
    StructField("release_date", TimestampType(), True),
    StructField("movie_id", StringType(), True),
    StructField("user_id", StringType(), True)
])
```


```python
df_ventana = ( spark.read
                .format("csv")
                .schema(schema_vnt)
                .option("header", "true")
                .load("./vodclickstream_uk_movies_03.csv")
          )
df_ventana.show(3)
```

                                                                                    

    +-----+-------------------+--------+--------------------+--------------------+-------------------+----------+----------+
    |  c0_|           datetime|duration|               title|              genres|       release_date|  movie_id|   user_id|
    +-----+-------------------+--------+--------------------+--------------------+-------------------+----------+----------+
    |58773|2017-01-01 01:15:09|     0.0|Angus, Thongs and...|Comedy, Drama, Ro...|2008-07-25 00:00:00|26bd5987e8|1dea19f6fe|
    |58774|2017-01-01 13:56:02|     0.0|The Curse of Slee...|Fantasy, Horror, ...|2016-06-02 00:00:00|f26ed2675e|544dcbc510|
    |58775|2017-01-01 15:17:47| 10530.0|   London Has Fallen|    Action, Thriller|2016-03-04 00:00:00|f77e500e7a|7cbcc791bf|
    +-----+-------------------+--------+--------------------+--------------------+-------------------+----------+----------+
    only showing top 3 rows
    


## Ejercicios

### 1.- Auditoría de telemetría Web (validación de datos)

Supón que el equipo de ingeniería web necesita verificar si el rastreador del navegador calculó correctamente el tiempo entre clics.

Ignora la columna `time_to_next_click` original. Crea una nueva columna `calculated_time_to_next` calculando tú mismo la diferencia en segundos entre el `click_datetime` de la fila actual y el del siguiente registro cronológico del mismo usuario (recuerda que puedes usar la función `lead()` para extraer información de una columna anterior). 

Compara ambas columnas para ver si hay discrepancias.


```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Ventana por usuario y orden temporal
w = Window.partitionBy("user_id").orderBy("datetime")

df2 = (
    df_ventana
    .withColumn("next_click_datetime", F.lead("datetime").over(w))
    .withColumn(
        "calculated_time_to_next",
        (F.col("next_click_datetime").cast("long") - F.col("datetime").cast("long"))
        # F.unix_timestamp('next_click_datetime')-F.unix_timestamp('datetime')
    )
)

df2.select("user_id", "datetime", "next_click_datetime", "duration", "calculated_time_to_next").show(3)

```

    [Stage 14:=====================>                                    (3 + 5) / 8]

    +----------+-------------------+-------------------+--------+-----------------------+
    |   user_id|           datetime|next_click_datetime|duration|calculated_time_to_next|
    +----------+-------------------+-------------------+--------+-----------------------+
    |0006ea6b5c|2017-05-19 20:21:43|2017-05-20 21:54:34|     0.0|                  91971|
    |0006ea6b5c|2017-05-20 21:54:34|2017-05-26 18:38:01|     0.0|                 506607|
    |0006ea6b5c|2017-05-26 18:38:01|2017-05-26 23:31:46|     0.0|                  17625|
    +----------+-------------------+-------------------+--------+-----------------------+
    only showing top 3 rows
    


                                                                                    

### 2.- Detección de "zapping"

En la versión web, es muy común que los usuarios hagan clic en una película, vean los primeros segundos y vuelvan atrás si no les convence.

Identifica estos rechazos rápidos. Utiliza la función `lead()` (o `lag()`) para calcular el tiempo de visualización. Si el tiempo hasta el siguiente clic del usuario en otra película es **inferior a 5 minutos (300 segundos)**, crea una columna llamada `es_zapping` y márcala con un `1` (de lo contrario, `0`).




```python
from pyspark.sql import functions as F

df_zap = (
    df_ventana
    .withColumn(
        "es_zapping",
        F.when(
            (F.col("duration") < 300) &
            (F.col("duration").isNotNull()),
            1
        ).otherwise(0)
    )
)

df_zap.select("title","user_id","es_zapping").show(3)
```

    +--------------------+----------+----------+
    |               title|   user_id|es_zapping|
    +--------------------+----------+----------+
    |Angus, Thongs and...|1dea19f6fe|         1|
    |The Curse of Slee...|544dcbc510|         1|
    |   London Has Fallen|7cbcc791bf|         0|
    +--------------------+----------+----------+
    only showing top 3 rows
    


### 3.- El ranking de "maratones"

Queremos saber cuántas películas llega a iniciar un usuario web en un solo día.

1. Extrae solo la fecha (sin la hora) de la columna `click_datetime`.
2. Utiliza `row_number()` particionando por `user_id` y por la **fecha**, ordenando por `click_datetime`.
3. Esto creará un contador diario (`pelicula_nro_1`, `pelicula_nro_2`...). Filtra el DataFrame final para encontrar a los usuarios extremos que hayan iniciado más de 5 películas en un mismo día.




```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Añadir la fecha sin hora
df_maraton = df_ventana.withColumn("date", F.to_date("datetime"))

# Ventana por usuario y día
w_day = Window.partitionBy("user_id", "date").orderBy("datetime")

# Numerar películas por día
df_maraton = df_maraton.withColumn(
    "pelicula_num",
    F.row_number().over(w_day)
)

# Contar cuántas películas inicia cada usuario por día
(df_maraton
    .groupBy("user_id", "date")
    .agg(F.max("pelicula_num").alias("total_peliculas"))
    .orderBy(F.col("total_peliculas").desc()) #.orderBy("total_peliculas",ascending=False)
    .show(3)
)

```

                                                                                    

    +----------+----------+---------------+
    |   user_id|      date|total_peliculas|
    +----------+----------+---------------+
    |23c52f9b50|2019-01-21|             64|
    |59416738c3|2017-02-21|             54|
    |3675d9ba4a|2018-11-26|             44|
    +----------+----------+---------------+
    only showing top 3 rows
    


### 4.- Análisis de re-visualización

Queremos identificar las películas que los usuarios del Reino Unido ven repetidas veces en sus ordenadores.

Crea una columna llamada `veces_vista_por_usuario` que cuente cuántas veces un mismo `user_id` ha hecho clic en el mismo `title_id` a lo largo de todo el periodo (2017-2019). Usa la función `count()` sobre una ventana particionada por usuario y película. Luego, filtra para mostrar solo aquellos registros donde el usuario haya visto la misma película 3 veces o más.


```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

w_rewatch = Window.partitionBy("user_id", "title")

df_rewatch = df_ventana.withColumn(
    "view_by_user",
    F.count("title").over(w_rewatch)
)

df_reviews = ( df_rewatch.filter(F.col("view_by_user")  >= 3)
                   .orderBy("view_by_user",ascending=False)
               .select("user_id","title","view_by_user")
               .distinct()

    
)
df_reviews.show(3)

```

    [Stage 10:>                                                         (0 + 1) / 1]

    +----------+----------+------------+
    |   user_id|     title|view_by_user|
    +----------+----------+------------+
    |000052a0a0|    Looper|           9|
    |0012a95d5f| Footloose|           3|
    |0016c962c8|Iron Man 3|           4|
    +----------+----------+------------+
    only showing top 3 rows
    


                                                                                    
