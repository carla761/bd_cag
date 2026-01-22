# PR0503. Limpieza de datos sobre dataset de cultivos

Seguimos avanzando en el conocimiento de PySpark realizando tareas más avanzadas.


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


## Dataset 1: Datos para la predicción del rendimiento en cultivos

Supón que queremos preparar los datos de nuestro dataset de cultivos para un modelo de redes neuronales y nos han pedido cuatro transformaciones específicas:

- Generar identificadores únicos estandarizados
- Normalizar las distribuciones numéricas
- Comparar insumos
- Proyectar fechas de cosecha


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

    26/01/22 09:40:00 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors



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
    


### 1.- Creación de un ID único

Necesitamos un código único para cada registro que sirva como clave primaria. Crea una nueva columna llamada `Crop_ID` en un nuevo DataFrame `df_eng`. Este ID debe seguir este formato estricto: `CODIGO_REGION-CULTIVO`.

- **Limpieza:** de la columna `Region` (ej. "Region_C"), elimina la palabra "Region_" y quédate solo con la letra (puedes usar [`substring`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.substring.html) o [`split`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.split.html)).
- **Formato:** convierte el nombre del cultivo (`Crop`) a mayúsculas ([`upper`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.upper.html)).
- **Concatenación:** une la letra de la región y el cultivo con un guion medio ([`concat_ws`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.concat_ws.html)).
- **Relleno:** si por algún motivo la letra de la región fuera muy corta (improbable aquí, pero por seguridad), asegúrate de que esa parte tenga al menos 3 caracteres rellenando con 'X' a la izquierda ([`lpad`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.lpad.html)). *Nota: Como en este dataset es solo una letra, el lpad rellenará con dos X, ej: "XXC".*



```python
from pyspark.sql.functions import col,upper,concat_ws,lit,lpad
df_eng = (df_crop
              .withColumn("Region",substring(df_crop.Region,8,3))
              .withColumn("Region", lpad("Region",3,"X"))
              .withColumn("Crop",upper(col("Crop")))
              .withColumn("Crop_ID", concat_ws("-",lit("CODIGO"),col("Region"),col("Crop")))
              .select("Region","Crop","Crop_ID")
         )
df_eng.show(3)
```

    +------+------+-----------------+
    |Region|  Crop|          Crop_ID|
    +------+------+-----------------+
    |   XXC| MAIZE| CODIGO-XXC-MAIZE|
    |   XXD|BARLEY|CODIGO-XXD-BARLEY|
    |   XXC|  RICE|  CODIGO-XXC-RICE|
    +------+------+-----------------+
    only showing top 3 rows
    


### 2: Transformación matemática

Los valores de lluvia tienen mucha varianza y el rendimiento tiene demasiados decimales irrelevantes. Añade/Modifica las siguientes columnas en `df_eng`:

- `Log_Rainfall`: calcula el logaritmo natural ([`log`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.log.html)) de la columna `Rainfall_mm` + 1 (para evitar errores si hubiera un 0).
- `Yield_Redondeado`: redondea el rendimiento (`Yield_ton_per_ha`) a 1 solo decimal usando la función [`round`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.round.html).
- `Rendimiento_Bancario`: crea otra columna usando [`bround`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.bround.html) sobre el rendimiento (sin decimales) para comparar cómo redondea Spark.




```python
from pyspark.sql.functions import col,lpad,log,bround
df_eng = (df_crop
              .withColumn("Log_Rainfall", log(col("Rainfall_mm")+1))
              .withColumn("Yield_Redondeado", round(col("Yield_ton_per_ha"),1) )
              .withColumn("Rendimiento_Bancario", bround(col("Yield_ton_per_ha")))
              .select("Crop","Log_Rainfall","Yield_Redondeado","Rendimiento_Bancario")
             
         )
df_eng.show(3)
```

    +------+-----------------+----------------+--------------------+
    |  Crop|     Log_Rainfall|Yield_Redondeado|Rendimiento_Bancario|
    +------+-----------------+----------------+--------------------+
    | Maize|7.304112368059574|           101.5|               101.0|
    |Barley|5.992464047441065|           127.4|               127.0|
    |  Rice|6.889489470175245|            69.0|                69.0|
    +------+-----------------+----------------+--------------------+
    only showing top 3 rows
    


### 3.- Comparación de insumos

Queremos saber cuál fue el insumo químico más pesado aplicado en cada parcela. Crea una columna llamada `Max_Quimico_kg`.

- Usa la función [`greatest`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.greatest.html) para comparar, fila por fila, el valor de `Fertilizer_Used_kg` contra `Pesticides_Used_kg`. El resultado debe ser el valor más alto de los dos.



```python
from pyspark.sql.functions import col,greatest
df_eng = (df_crop
              .withColumn("Max_Quimico_kg", greatest(col("Fertilizer_Used_kg"), col("Pesticides_Used_kg")) )
              .select("Crop","Max_Quimico_kg","Fertilizer_Used_kg","Pesticides_Used_kg")
         )
df_eng.show(3)
```

    +------+--------------+------------------+------------------+
    |  Crop|Max_Quimico_kg|Fertilizer_Used_kg|Pesticides_Used_kg|
    +------+--------------+------------------+------------------+
    | Maize|         105.1|             105.1|              10.2|
    |Barley|         221.8|             221.8|              35.5|
    |  Rice|          61.2|              61.2|              40.0|
    +------+--------------+------------------+------------------+
    only showing top 3 rows
    


### 4.- Simulación de fechas

El dataset original no tiene fecha, pero sabemos que todos estos datos corresponden a la siembra del **1 de Abril de 2023**.

- Crea una columna `Fecha_Siembra` usando [`to_date`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.to_date.html) sobre el literal "2023-04-01".
- Calcula la `Fecha_Estimada_Cosecha` sumando 150 días a la fecha de siembra ([`date_add`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.date_add.html)).
- Extrae el mes de la cosecha en una columna nueva llamada `Mes_Cosecha` ([`month`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.month.html)).


```python
from pyspark.sql.functions import col,to_date,date_add,month,lit
df_eng = (df_crop
              .withColumn("Fecha_Siembra", to_date(lit("2023-04-01")) )
              .withColumn("Fecha_Estimada_Cosecha", date_add(col("Fecha_Siembra"),150) )
              .withColumn("Mes_Cosecha", month(col("Fecha_Estimada_Cosecha")) )
              .select("Crop", "Fecha_Siembra", "Fecha_Estimada_Cosecha","Mes_Cosecha")
         )
df_eng.show(3)

```

    +------+-------------+----------------------+-----------+
    |  Crop|Fecha_Siembra|Fecha_Estimada_Cosecha|Mes_Cosecha|
    +------+-------------+----------------------+-----------+
    | Maize|   2023-04-01|            2023-08-29|          8|
    |Barley|   2023-04-01|            2023-08-29|          8|
    |  Rice|   2023-04-01|            2023-08-29|          8|
    +------+-------------+----------------------+-----------+
    only showing top 3 rows
    

