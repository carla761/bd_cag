# PR0505. Análisis de estadísticas en dataset

En esta práctica trabajarás sobre [este dataset](https://www.kaggle.com/datasets/juhibhojani/house-price) que contiene precios de casas en la India. 

Dado que es un dataset local con formatos regionales (Rupias, Lakhs, Crores, pies cuadrados), deberás transformarlo a un estándar internacional (dólares USD y metros cuadrados) para poder realizar un análisis estadístico comparativo y preparar los *features* para el entrenamiento del modelo.




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


## 1. Objetivos de ingeniería de datos (ETL)

Antes de cualquier análisis, debe ejecutar un pipeline de transformación sobre los datos crudos.


```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
schema_hs = StructType([
        StructField("Index", IntegerType(), False),
        StructField("Title", StringType(), False),
        StructField("Description", StringType(), False),
        StructField("Amount(in rupees)", StringType(), True),
        StructField("Price(in rupees)", StringType(), True),
        StructField("Location", StringType(), False),
        StructField("Carpet_Area", StringType(), True),
        StructField("Status", StringType(), False),
        StructField("Floor", StringType(), False),
        StructField("Transaction", StringType(), False),
        StructField("Furnishing", IntegerType(), False),
        StructField("Facing", StringType(), True),
        StructField("Overlooking", StringType(), True),
        StructField("Society", StringType(), True),
        StructField("Bathroom", IntegerType(), False),
        StructField("Balcony", IntegerType(), True),
        StructField("Car_Parking", StringType(), True),
        StructField("Ownership", StringType(), True),
        StructField("Super_Area", StringType(), True),
    ])
```


```python
df_house = ( spark.read
                .format("csv")
                .schema(schema_hs)
                .option("header", "true")
                .load("./house_prices.csv")
           )
df_house.show(3)
```

    [Stage 87:>                                                         (0 + 1) / 1]

    +-----+--------------------+--------------------+-----------------+----------------+--------+-----------+-------------+------------+-----------+----------+------+-----------+--------------------+--------+-------+-----------+---------+----------+
    |Index|               Title|         Description|Amount(in rupees)|Price(in rupees)|Location|Carpet_Area|       Status|       Floor|Transaction|Furnishing|Facing|Overlooking|             Society|Bathroom|Balcony|Car_Parking|Ownership|Super_Area|
    +-----+--------------------+--------------------+-----------------+----------------+--------+-----------+-------------+------------+-----------+----------+------+-----------+--------------------+--------+-------+-----------+---------+----------+
    |    0|1 BHK Ready to Oc...|Bhiwandi, Thane h...|          42 Lac |            6000|   thane|   500 sqft|Ready to Move|10 out of 11|     Resale|      NULL|  NULL|       NULL|Srushti Siddhi Ma...|       1|      2|       NULL|     NULL|      NULL|
    |    1|2 BHK Ready to Oc...|One can find this...|          98 Lac |           13799|   thane|   473 sqft|Ready to Move| 3 out of 22|     Resale|      NULL|  East|Garden/Park|         Dosti Vihar|       2|   NULL|     1 Open| Freehold|      NULL|
    |    2|2 BHK Ready to Oc...|Up for immediate ...|         1.40 Cr |           17500|   thane|   779 sqft|Ready to Move|10 out of 29|     Resale|      NULL|  East|Garden/Park|Sunrise by Kalpataru|       2|   NULL|  1 Covered| Freehold|      NULL|
    +-----+--------------------+--------------------+-----------------+----------------+--------+-----------+-------------+------------+-----------+----------+------+-----------+--------------------+--------+-------+-----------+---------+----------+
    only showing top 3 rows
    


                                                                                    

### 1.1. Estandarización monetaria (de INR a USD)

Las columnas `Amount(in rupees)` y `Price (in rupees)` vienen en formato de texto con unidades indias (*Lac* y *Cr*).

1. **Limpieza:** convierte los textos a valores numéricos puros en rupias (INR). Ten en cuenta que 1 Lac = 100,000 INR y 1 Cr = 10,000,000 INR.


2. **Conversión:** crea una nueva columna `Amount_USD` convirtiendo las rupias a dólares. Asume que el valor de conversión es 1 INR = 0.012 USD.



```python
df_house.select("Amount(in rupees)","Price(in rupees)").show(3)
```

    +-----------------+----------------+
    |Amount(in rupees)|Price(in rupees)|
    +-----------------+----------------+
    |          42 Lac |            6000|
    |          98 Lac |           13799|
    |         1.40 Cr |           17500|
    +-----------------+----------------+
    only showing top 3 rows
    



```python
from pyspark.sql import functions as F

df_monetario = (
    df_house
    # Convertir Amount(in rupees)
    .withColumn(
        "Amount_INR",
        F.when(
            F.col("Amount(in rupees)").contains("Lac"), 
            # F.col("Amount(in rupees)").rlike("(?i)Lac"),
            F.regexp_replace(F.col("Amount(in rupees)"), " Lac", "").cast("double") * 100000 
            # F.regexp_extract(F.col("Amount(in rupees)"), r"([\d\.]+)", 1).cast("double") * 100000
        )
        .when(
            F.col("Amount(in rupees)").contains("Cr"),
            F.regexp_replace(F.col("Amount(in rupees)"), " Cr", "").cast("double") * 10000000
        )
        .otherwise(F.col("Amount(in rupees)").cast("double"))
    )
    
    # Conversión a USD
    .withColumn("Amount_USD", F.round(F.col("Amount_INR") * F.lit(0.012),2))
    .withColumn("Price_USD", F.round(F.col("Price(in rupees)") * F.lit(0.012),2))
)


```


```python
df_monetario.select(
     "Amount(in rupees)", "Amount_INR", "Amount_USD",
     "Price(in rupees)", "Price_USD"
).show(3)
```

    +-----------------+----------+----------+----------------+---------+
    |Amount(in rupees)|Amount_INR|Amount_USD|Price(in rupees)|Price_USD|
    +-----------------+----------+----------+----------------+---------+
    |          42 Lac | 4200000.0|   50400.0|            6000|     72.0|
    |          98 Lac | 9800000.0|  117600.0|           13799|   165.59|
    |         1.40 Cr |     1.4E7|  168000.0|           17500|    210.0|
    +-----------------+----------+----------+----------------+---------+
    only showing top 3 rows
    


### 1.2. Estandarización de superficie

La columna `Carpet Area` está en pies cuadrados (*sqft*).

1. **Limpieza:** elimina las unidades textuales y extrae el valor numérico.
2. **Conversión:** crea una nueva columna `Area_m2` convirtiendo los pies cuadrados a metros cuadrados. El factor de conversión es 1 sqft = 0.0929.




```python
df_prueba=(df_house
                .select("Carpet_Area")
          )
df_prueba.show(3)
```

    +-----------+
    |Carpet_Area|
    +-----------+
    |   500 sqft|
    |   473 sqft|
    |   779 sqft|
    +-----------+
    only showing top 3 rows
    



```python
df_superficie = (
    df_monetario
    # Convertir Carpet Area
    .withColumn(
        "Carpet_Area",
        F.split(F.col("Carpet_Area"), " ")[0].cast("integer")
    )
    .withColumn("Area_m2", F.col("Carpet_Area") * 0.0929)
)

```


```python
df_superficie.select("Carpet_Area", "Area_m2").show(3)
```

    +-----------+------------------+
    |Carpet_Area|           Area_m2|
    +-----------+------------------+
    |        500|46.449999999999996|
    |        473|           43.9417|
    |        779|           72.3691|
    +-----------+------------------+
    only showing top 3 rows
    


## 2. Objetivos de análisis estadístico

Utilizando las **nuevas columnas transformadas** (`Amount_USD` y `Area_m2`), calcula e interpreta las siguientes métricas de distribución usando PySpark:



```python
df_superficie.select("Amount_USD", "Area_m2").show(3)
```

    +----------+------------------+
    |Amount_USD|           Area_m2|
    +----------+------------------+
    |   50400.0|46.449999999999996|
    |  117600.0|           43.9417|
    |  168000.0|           72.3691|
    +----------+------------------+
    only showing top 3 rows
    


### 2.1. Medidas de dispersión (varianza y desviación estándar)

- Calcula la varianza y la desviación estándar de la columna `Amount_USD`.
- **Pregunta:** Si la desviación estándar es muy alta en comparación con el precio medio (por ejemplo, si la media es $100k y la desviación es $80k), ¿podemos decir que el "precio promedio" es un buen representante del mercado? ¿O los precios son demasiado dispares para confiar en el promedio?

- **Respuesta**:
    - No. Cuando la desviación estándar es muy alta respecto a la media, el promedio deja de representar bien al mercado.
    - Sí. Una desviación tan grande indica que los precios son muy dispares y no se puede confiar en la media como medida central.


```python
stats = df_superficie.select(
                F.variance("Amount_USD").alias("varianza"),
                F.stddev("Amount_USD").alias("desviacion"),
                F.mean("Amount_USD").alias("Media"),
                F.kurtosis("Amount_USD").alias("curtosis")
            )

stats.show(truncate=False)
```

    [Stage 93:=======>                                                  (1 + 7) / 8]

    +---------------------+-----------------+-----------------+-----------------+
    |varianza             |desviacion       |Media            |curtosis         |
    +---------------------+-----------------+-----------------+-----------------+
    |2.2368142798731815E11|472949.7097866941|143727.1412747055|91491.17725573125|
    +---------------------+-----------------+-----------------+-----------------+
    


                                                                                    


```python
var, desv, med , cur = stats.collect()[0]
var
```

                                                                                    




    223681427987.31815



### 2.2. Medidas de Forma (Skewness y Kurtosis)

- Calcule el `skewness` (asimetría) y la `kurtosis` (curtosis) de `Amount_USD`.
- **Pregunta:** Suponiendo que has obtenido un valor positivo, ¿qué significa esto para el negocio? ¿Hay más oferta de casas "baratas" con algunas pocas mansiones ultra-caras, o hay muchas casas caras y pocas baratas?

    - **Respuesta**: Un skewness positivo indica que hay muchas casas baratas y unas pocas propiedades extremadamente caras que estiran la distribución hacia la derecha.

- **Pregunta:** Supón que obtienes una kurtosis superior a 3. ¿Deberíamos preocuparnos por la presencia de datos erróneos o propiedades de lujo extremo que podrían distorsionar nuestros análisis futuros?

    - **Respuesta**: Sí. Una kurtosis mayor a 3 sugiere colas pesadas, lo que puede indicar outliers, datos erróneos o propiedades de lujo extremo que podrían distorsionar futuros análisis y modelos.



```python
forma = df_superficie.select(
                F.skewness("Amount_USD").alias("asimetria"),
                F.kurtosis("Amount_USD").alias("curtosis")
        ).show(truncate=False)

```

    [Stage 99:=======>                                                  (1 + 7) / 8]

    +-----------------+-----------------+
    |asimetria        |curtosis         |
    +-----------------+-----------------+
    |270.7690536208719|91491.17725573125|
    +-----------------+-----------------+
    


                                                                                    

## 3. Interpretación para IA

Redacta un breve informe técnico respondiendo a estas situaciones de modelado:

### 3.1.- **Pre-procesamiento para redes neuronales:** 
 
Observando la *desviación estándar* de `Amount_USD` (precio) frente a la de `Area_m2` (superficie), notará que tienen escalas muy diferentes (miles de dólares vs. decenas de metros). Realiza los pasos necesarios para homogeneizar las escalas de ambas columnas.



```python
df_superficie.select(
    F.stddev("Amount_USD").alias("Desviavion_Amount_USD"),
    F.stddev("Area_m2").alias("Desviacion_Area_m2")
).show(truncate=False)

```

    [Stage 102:===================================>                     (5 + 3) / 8]

    +---------------------+------------------+
    |Desviavion_Amount_USD|Desviacion_Area_m2|
    +---------------------+------------------+
    |472949.7097866941    |283.10876647919014|
    +---------------------+------------------+
    


                                                                                    


```python
stats_2 = df_superficie.select(
                F.variance("Area_m2").alias("varianza_2"),
                F.stddev("Area_m2").alias("desviacion_2"),
                F.mean("Area_m2").alias("media_2")
            )

stats_2.show(truncate=False)
```

    [Stage 105:=======>                                                 (1 + 7) / 8]

    +----------------+------------------+------------------+
    |varianza_2      |desviacion_2      |media_2           |
    +----------------+------------------+------------------+
    |80150.5736573686|283.10876647919014|111.48601082360713|
    +----------------+------------------+------------------+
    


                                                                                    


```python
var_2, desv_2, med_2 = stats_2.collect()[0]
var_2
```

                                                                                    




    80150.5736573686




```python
df_scaled = (df_superficie
                .withColumn(
                    "z-score(Amount_USD)",
                    (F.col("Amount_USD") - med ) / desv
                )
                .withColumn(
                    "z-score(Area_m2)",
                    (F.col("Area_m2") - med_2 ) / desv_2
                )
            )
df_scaled.select("Amount_USD", "z-score(Amount_USD)","Area_m2","z-score(Area_m2)").show(5)
```

    +----------+--------------------+------------------+--------------------+
    |Amount_USD| z-score(Amount_USD)|           Area_m2|    z-score(Area_m2)|
    +----------+--------------------+------------------+--------------------+
    |   50400.0| -0.1973299472301128|46.449999999999996|-0.22972093599364965|
    |  117600.0|-0.05524295867839553|           43.9417|-0.23858078173842762|
    |  168000.0| 0.05132228273539241|           72.3691|-0.13816919663094365|
    |   30000.0| -0.2404634973261698|49.236999999999995| -0.2198766629438963|
    |  192000.0| 0.10206763578957714|58.991499999999995|-0.18542170726975965|
    +----------+--------------------+------------------+--------------------+
    only showing top 5 rows
    


### 3.2.- **Gestión de outliers (Kurtosis):**

Al calcular la kurtosis de la columna de precios (Amount_USD), puede que obtengas un valor muy alto (mayor a 3, e incluso superior a 10). Si no fuera así supondremos que lo es.

Esto indica una distribución "leptocúrtica" con "colas pesadas". En el contexto de Big Data, esto significa que unos pocos registros extremos (mansiones de lujo o errores de entrada) están distorsionando la media y la varianza, lo que podría arruinar el entrenamiento de futuros modelos de Machine Learning.

Debes **normalizar** la distribución aplicando una técnica de clipping eliminando los extremos superiores, para ello sigue estos pasos:

**Identifica el límite**

En entornos distribuidos, calcular un percentil exacto es computacionalmente muy costoso (requiere ordenar todos los datos). PySpark utiliza algoritmos de aproximación (como [Greenwald-Khanna](https://aakinshin.net/posts/greenwald-khanna-quantile-estimator/)). 

Vas a calcular el percentil 99 para eliminar todos los valores que lo superen. En PySpark se hace con el método [`.approxQuantile("Amount_USD", [0.99], 0.01)`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.approxQuantile.html). Este método devuelve una lista, por lo que deberás extraer el primer valor. El tercer parámetro (0.01) es la tolerancia de error permitida.

**Aplica el filtro**

Genera un nuevo DataFrame llamado `df_limpio` que excluya las propiedades que superen ese precio límite calculado (quédate con el 99% de los datos más "normales").

**Verificación**

Vuelve a calcular la kurtosis, la media y la stddev sobre este nuevo DataFrame `df_limpio`.

**Pregunta**: comparando los resultados antes y después del filtro: ¿Cuánto ha bajado la curtosis? ¿Ha cambiado drásticamente el precio medio al eliminar solo el 1% de los datos? Reflexiona sobre la sensibilidad de la media aritmética frente a los outliers en grandes volúmenes de datos.

**Respuesta**:
 - La curtosis bajo mucho, pasó de 91,491 a 2.43, lo que indica que concentraba outliers muy extremos.
 - La bajada de la media no es tan extrema como la curtosis, pero sí es un cambio claramente significativo para solo un 2% de datos.
 - La media aritmética sigue siendo muy sensible a pocos valores extremos, incluso con muchos datos, un pequeño grupo de outliers puede desplazarla de forma apreciable.


```python
limite = df_scaled.approxQuantile("Amount_USD", [0.98], 0.01)[0]
limite

```

                                                                                    




    522000.0




```python
df_limpio = (df_scaled
                 .filter(F.col("Amount_USD") < limite)
            )
```


```python
stats_3 = df_limpio.select(
                F.kurtosis("Amount_USD").alias("curtosis"),
                F.stddev("Amount_USD").alias("desviacion"),
                F.mean("Amount_USD").alias("Media")
            )

stats_3.show(truncate=False)
```

    [Stage 114:=======>                                                 (1 + 7) / 8]

    +-----------------+-----------------+------------------+
    |curtosis         |desviacion       |Media             |
    +-----------------+-----------------+------------------+
    |2.433184871430435|98492.60499549586|123933.06611560707|
    +-----------------+-----------------+------------------+
    


                                                                                    


```python
stats.show(truncate=False)
```

    [Stage 117:=======>                                                 (1 + 7) / 8]

    +---------------------+-----------------+-----------------+-----------------+
    |varianza             |desviacion       |Media            |curtosis         |
    +---------------------+-----------------+-----------------+-----------------+
    |2.2368142798731815E11|472949.7097866941|143727.1412747055|91491.17725573125|
    +---------------------+-----------------+-----------------+-----------------+
    


                                                                                    

## 4. Análisis de Segmentos (Grouping & Aggregation)

Algo que nos puede ocurrir al realizar el análisis estadístico sobre el dataset completo es que las métricas globales calculadas están "sucias" porque mezclan tipos de propiedades muy diferentes (no es justo comparar un estudio de 1 habitación con un ático de 4 habitaciones).

Vamos a refinar el análisis estadístico agrupando los datos por categorías clave.

### 4.1.- **Ingeniería de variable (Extracción de `BHK` - Bedroom-Hall-Kitchen):**

- La columna `Title` contiene información como *"1 BHK Ready to Occupy..."* o *"2 BHK..."*.
- Crea una nueva columna llamada `Num_Bedrooms` extrayendo el número antes de "BHK"




```python
df_bhk = (
    df_limpio
    .withColumn(
        "Num_Bedrooms",
        F.split(F.col("Title"), " ")[0].cast("int")
    )
)

```


```python
df_bhk.select("Num_Bedrooms", "Title").show(3)
```

    +------------+--------------------+
    |Num_Bedrooms|               Title|
    +------------+--------------------+
    |           1|1 BHK Ready to Oc...|
    |           2|2 BHK Ready to Oc...|
    |           2|2 BHK Ready to Oc...|
    +------------+--------------------+
    only showing top 3 rows
    


### 4.2.- **Cálculo de estadísticas por grupo:**

- Agrupa los datos por `Num_Bedrooms` (ej. 1 BHK, 2 BHK, 3 BHK).
- Para cada grupo, calcula simultáneamente: `Mean`, `StdDev` y `Skewness` del precio (`Amount_USD`).



```python
df_stats_4 = (
    df_bhk
    .groupBy("Num_Bedrooms")
    .agg(
        F.mean("Amount_USD").alias("Media"),
        F.stddev("Amount_USD").alias("Desviacion"),
        F.skewness("Amount_USD").alias("Asimetria")
    )
    .orderBy("Num_Bedrooms")
)

```


```python
df_stats_4.show()
```

    [Stage 136:=======>                                                 (1 + 7) / 8]

    +------------+------------------+------------------+--------------------+
    |Num_Bedrooms|             Media|        Desviacion|           Asimetria|
    +------------+------------------+------------------+--------------------+
    |        NULL| 57512.72727272727| 73510.61074590133|   2.980624321638696|
    |           1|42328.167832167834|31923.193624799565|  3.8502558006230014|
    |           2| 73035.88543515613| 44918.51541522151|  2.2474264102046555|
    |           3|154841.02406844302| 93764.80555647868|   1.327562573380713|
    |           4|266713.99790763715|119459.60735656598|0.056874832557085704|
    |           5| 356968.7031700288|119067.56120280345| -0.9636234924385035|
    |           6|253077.55102040817|128390.71108876045| 0.47465368067230734|
    |           7|269538.46153846156|158009.01629580898| 0.43332821947377914|
    |           8|          196560.0|246412.57110788807|                 0.0|
    |           9|          303000.0|125331.56027114639| 0.15506836162301418|
    |          10|          265350.0|128209.10375521032|-0.31530187120905473|
    +------------+------------------+------------------+--------------------+
    


                                                                                    

### 4.3. **Preguntas de análisis para el modelo:**

Una vez calculadas las métricas por grupo (1 BHK, 2 BHK, etc.), responde a las siguientes preguntas sobre la estructura del mercado:


#### A. Análisis de variabilidad (Desviación Estándar):

Observa cómo cambia la desviación estándar de los precios a medida que aumentan las habitaciones. ¿La variabilidad se mantiene constante o se dispara en las propiedades más grandes?

**Pregunta**: Si la desviación es mucho mayor en los pisos de 3 BHK que en los de 1 BHK, ¿qué nos indica esto sobre la homogeneidad del producto? 

Pista: Un mercado con baja desviación sugiere que los inmuebles son muy parecidos entre sí (*commodities*). Una alta desviación sugiere que dentro de esa categoría conviven pisos "estándar" con propiedades de "ultra-lujo", haciendo que el mercado sea mucho más heterogéneo.


**Respuesta**: Una desviación mucho mayor en 3 BHK indica que ese segmento es menos homogéneo: mezcla pisos estándar con otros de lujo, por eso los precios se dispersan más.

#### B. Confiabilidad del precio promedio:

**Pregunta**: Basándote en lo anterior, ¿en qué segmento (1 BHK o 3 BHK) dirías que el "Precio Promedio" es un indicador más fiable del valor real de una propiedad? Es decir, si tuvieras que tasar una propiedad "a ciegas" usando solo el promedio del mercado, ¿en qué tipo de apartamento tendrías más riesgo de equivocarte drásticamente por exceso o por defecto?

**Respuesta**: El promedio es más fiable en 1 BHK, porque el mercado es más uniforme.
En 3 BHK hay más riesgo de equivocarte mucho usando solo la media.

#### C. Detección de anomalías de mercado (Curtosis):

Compara la curtosis entre los apartamentos pequeños y los grandes.

**Pregunta**: ¿Qué segmento tiene una curtosis más alta (colas más pesadas)?

**Pregunta**: Si el segmento de 3 BHK tiene una curtosis muy elevada, significa que existen propiedades con precios desorbitados que rompen la norma. ¿Consideras que estas "mansiones" representan la realidad del barrio, o son excepciones que deberían analizarse en un estudio de mercado aparte para no distorsionar la visión general?

**Respuesta**: El segmento con mayor curtosis tiene colas más pesadas, es decir, precios extremos.
Si 3 BHK muestra curtosis muy alta, esas “mansiones” son excepciones, no representan al mercado típico y conviene analizarlas por separado.


```python

```
