# PR0507. Creación de un motor de recomendación gastronómico

## Contexto

En esta práctica trabajarás con el *dataset* [**Restaurant Recommendations**](https://www.kaggle.com/datasets/teesoong/ml-challenge/*) que contiene una relación de usuarios y restaurantes con sus valoraciones.

Tu objetivo será **construir un motor de recomendación inteligente** que sugiera a cada usuario restaurantes que probablemente le encantarán, basándose en el historial de valoraciones de toda la comunidad.


## El dataset

Para esta primera versión del motor, trabajaremos exclusivamente con el archivo **`ratings.csv`**. Este fichero contiene el historial de valoraciones que los usuarios han dejado en diferentes locales.

Su estructura es muy sencilla:

- `user_id`: identificador único del usuario.
- `venue_id`: identificador único del restaurante/local.
- `rating`: la nota que el usuario le dio a ese local (del 1 al 5).



## Tareas a realizar

Deberás crear un script o Notebook en PySpark que ejecute el flujo completo de Machine Learning. Sigue estos pasos:

### Fase 1: Preparación de datos

1. **Inicializa PySpark:** crea la sesión de Spark con un nombre descriptivo para la aplicación.
2. **Carga de datos:** lee el archivo `ratings.csv` y guárdalo en un DataFrame. Asegúrate de que las columnas tengan el tipo de dato correcto (enteros para los IDs y numérico/double para el rating).
3. **División de la muestra:** separa el DataFrame en dos bloques usando una semilla (seed) para que tus resultados sean reproducibles:
    - **80%** para entrenamiento (train).
    - **20%** para evaluación (test).




```python
!pip install numpy
```

    Requirement already satisfied: numpy in /usr/local/lib/python3.10/site-packages (2.2.6)
    [33mWARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv[0m[33m
    [0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m A new release of pip is available: [0m[31;49m23.0.1[0m[39;49m -> [0m[32;49m26.0.1[0m
    [1m[[0m[34;49mnotice[0m[1;39;49m][0m[39;49m To update, run: [0m[32;49mpip install --upgrade pip[0m



```python
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

spark = ( SparkSession.builder
            .appName("Motor de recomendacion")
            .master("spark://spark-master:7077")
            .getOrCreate()
        )
print("SparkSession iniciada correctamente.")
```

    Setting default log level to "WARN".
    To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
    26/03/05 10:15:03 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.



```python
from pyspark.sql.types import StructType, StructField, DecimalType, DoubleType

schema_rt = StructType([
    StructField("user_id", DecimalType(), True),
    StructField("venue_id", DecimalType(), True),
    StructField("rating", DoubleType(), True)
])
```


```python
df_rating = ( spark.read
                .format("csv")
                .schema(schema_rt)
                .option("header", "true")
                .load("./ratings.csv")
          )
df_rating.show(3)
```

                                                                                    

    +-------+--------+------+
    |user_id|venue_id|rating|
    +-------+--------+------+
    |      1|       1|   5.0|
    |      1|      51|   4.0|
    |      1|      51|   2.0|
    +-------+--------+------+
    only showing top 3 rows
    



```python
# Separar 80-20
train, test = (df_rating
                  .randomSplit([0.8,0.2], seed=42)
              )
print(f"Datos para entrenar: {train.count()}")
print(f"Datos para evaluar:{test.count()}")
```

    26/03/05 10:15:15 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors
                                                                                    

    Datos para entrenar: 2248543


    [Stage 4:====================================>                      (5 + 3) / 8]

    Datos para evaluar:561037


                                                                                    

### Fase 2: Construcción y búsqueda del modelo óptimo

No sabemos qué configuración matemática es la mejor para nuestros usuarios, así que vamos a automatizar la búsqueda.

1. **Instancia el modelo ALS:** configura las columnas de entrada (`userCol`, `itemCol`, `ratingCol`). No olvides configurar la estrategia adecuada para el arranque en frío (`coldStartStrategy`) para evitar errores en la evaluación
2. **Crea la cuadrícula de hiperparámetros (ParamGrid):** configura al menos las siguientes combinaciones para que el sistema las pruebe:
    - `rank` (Factores latentes): Prueba con 5, 10 y 15.
    - `regParam` (Regularización): Prueba con 0.01 y 0.1.
    - `maxIter` (Iteraciones): Fíjalo en 10 para no sobrecargar el sistema.

3. **Configura el evaluador:** utiliza un `RegressionEvaluator` que mida el error usando la métrica **RMSE**.
4. **Validación cruzada (CrossValidator):** ensambla el modelo, la cuadrícula y el evaluador usando `numFolds=3` para asegurar un entrenamiento robusto. Ejecuta el entrenamiento sobre tu **80% de datos**. *(Ten en cuenta que este paso puede tardar unos minutos).*



```python
als = ALS(
    userCol="user_id",
    itemCol="venue_id",
    ratingCol="rating",
    coldStartStrategy="drop"
)
```


```python
from pyspark.ml.tuning import ParamGridBuilder

grid_params = (
    ParamGridBuilder()
    .addGrid(als.rank, [5, 10, 15])        # Factores latentes
    .addGrid(als.regParam, [0.01, 0.1])    # Penalización valores extremos
    .addGrid(als.maxIter, [10])            # Iteraciones
    .build()
)


```


```python
modelo = als.fit(train)
print("El modelo ha sido entrenado")
```

                                                                                    

    El modelo ha sido entrenado



```python
# Evaluacion
predicciones = modelo.transform(test)

evaluador = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)

error_rmse = evaluador.evaluate(predicciones)
print(f"Margen de error(RMSE): {error_rmse}")
```

    [Stage 118:>                                                        (0 + 8) / 9]

    Margen de error(RMSE): 1.6846869062514216


                                                                                    


```python
# Validacion cruzada
from pyspark.ml.tuning import CrossValidator
validador_cruzado = CrossValidator(
                        estimator=als,
                        estimatorParamMaps=grid_params,
                        evaluator=evaluador,
                        numFolds=3
                        )
```


```python
# Reducir dataset al 1%
df_small, _ = df_rating.randomSplit([0.01, 0.9], seed=42)
# df_small = df_rating.sample(False, 0.10, seed=42)

print("Tamaño reducido:", df_small.count())

# Split 80-20
train_small, test_small = df_small.randomSplit([0.8, 0.2], seed=42)

print("Train:", train_small.count())
print("Test:", test_small.count())

```

                                                                                    

    Tamaño reducido: 31021


    [Stage 123:==============>                                          (2 + 6) / 8]

    Train: 24947


    [Stage 126:==============>                                          (2 + 6) / 8]

    Test: 6074


                                                                                    


```python
modelo_optimizado = validador_cruzado.fit(train_small)
print("Modelo entrenado")
```

                                                                                    

    Modelo entrenado


### Fase 3: evaluación y resultados


A partir del objeto de validación cruzada, extrae el mejor modelo y muestra por pantalla mediante código cuáles han sido los hiperparámetros ganadores (`rank` y `regParam`).




```python
combinaciones = modelo_optimizado.getEstimatorParamMaps()

notas_rmse = modelo_optimizado.avgMetrics

ranking = sorted(zip(notas_rmse, combinaciones), key=lambda x: x[0])

print("--- RANKING DE TODAS LAS PRUEBAS ---")
for nota, parametros in ranking:
    print(f"\n RMSE Obtenido: {nota}")

    for param, valor in parametros.items():
        print(f"{param.name}: {valor}")
```

    --- RANKING DE TODAS LAS PRUEBAS ---
    
     RMSE Obtenido: 2.5838521740903833
    rank: 10
    regParam: 0.1
    maxIter: 10
    
     RMSE Obtenido: 2.6018799936412957
    rank: 15
    regParam: 0.1
    maxIter: 10
    
     RMSE Obtenido: 2.6126838759217397
    rank: 15
    regParam: 0.01
    maxIter: 10
    
     RMSE Obtenido: 2.6353273812526172
    rank: 5
    regParam: 0.1
    maxIter: 10
    
     RMSE Obtenido: 2.6403292150764144
    rank: 10
    regParam: 0.01
    maxIter: 10
    
     RMSE Obtenido: 2.692186447215239
    rank: 5
    regParam: 0.01
    maxIter: 10


### Fase 4: Puesta en Producción


1. Selecciona a un usuario cualquiera de tu dataset (por ejemplo, el `user_id = 1`).
2. Utiliza la función específica de Spark para subconjuntos de usuarios y obtén sus **15 mejores restaurantes recomendados**.
3. Limpia la salida para que se muestre en un formato de tabla legible (Usuario, Restaurante, Nota Predicha).


```python
train_small.show(3)
```

    [Stage 1893:>                                                       (0 + 1) / 1]

    +-------+--------+------+
    |user_id|venue_id|rating|
    +-------+--------+------+
    |     15|     233|   3.0|
    |     15|     259|   4.0|
    |     38|     573|   4.0|
    +-------+--------+------+
    only showing top 3 rows
    


                                                                                    


```python
from pyspark.sql.functions import col

# Seleccionar usuario concreto
usuario_objetivo = 15

df_usuario = df_rating.select("user_id").where(col("user_id") == usuario_objetivo).distinct()

# Extraer el ALSModel real
modelo_final = modelo_optimizado.bestModel

# Generar recomendaciones (15 ítems)
recomendaciones_usuario = modelo_final.recommendForUserSubset(df_usuario, 15)

recomendaciones_usuario.show(truncate=False)


```

                                                                                    

    +-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |user_id|recommendations                                                                                                                                                                                                                                                                                                  |
    +-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |15     |[{698462, 4.049541}, {454684, 3.930776}, {259, 3.9216568}, {726763, 3.8252342}, {408909, 3.7741683}, {958970, 3.6833003}, {890899, 3.6799126}, {184789, 3.6571631}, {290261, 3.6259801}, {689715, 3.5888708}, {689656, 3.5888708}, {21514, 3.573833}, {21486, 3.573833}, {583831, 3.5701141}, {969286, 3.567484}]|
    +-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    



```python
from pyspark.sql.functions import explode, col
# Arreglar la tabla de recomendaciones
tabla_recs = recomendaciones_usuario.select(
    col("user_id"),
    explode("recommendations").alias("rec")
).select(
    col("user_id").alias("Usuario"),
    col("rec.venue_id").alias("Restaurante_Id"),
    col("rec.rating").alias("Nota_Predicha")
)

tabla_recs.show(truncate=False)

```

                                                                                    

    +-------+--------------+-------------+
    |Usuario|Restaurante_Id|Nota_Predicha|
    +-------+--------------+-------------+
    |15     |698462        |4.049541     |
    |15     |454684        |3.930776     |
    |15     |259           |3.9216568    |
    |15     |726763        |3.8252342    |
    |15     |408909        |3.7741683    |
    |15     |958970        |3.6833003    |
    |15     |890899        |3.6799126    |
    |15     |184789        |3.6571631    |
    |15     |290261        |3.6259801    |
    |15     |689715        |3.5888708    |
    |15     |689656        |3.5888708    |
    |15     |21514         |3.573833     |
    |15     |21486         |3.573833     |
    |15     |583831        |3.5701141    |
    |15     |969286        |3.567484     |
    +-------+--------------+-------------+
    



```python

```
