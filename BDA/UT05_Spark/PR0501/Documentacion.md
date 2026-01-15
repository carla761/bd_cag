# PR0501 Ingesta de datos de ficheros CSV
En esta primera práctica practicaremos con la carga de datos en dataframes de Spark. Para cada uno de los ejercicios tienes que cargar el dataset referenciado definiendo tú previamente el esquema. Una vez que lo hayas hecho muestra el esquema del dataframe y muestra los 5 primeros registros.


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

[Kaggle: Smart Crop yield predication dataset](https://www.kaggle.com/datasets/miadul/smart-crop-yield-predication-dataset)



```python
!head -n2 ./crop_yield_dataset.csv
```

    Crop,Region,Soil_Type,Soil_pH,Rainfall_mm,Temperature_C,Humidity_pct,Fertilizer_Used_kg,Irrigation,Pesticides_Used_kg,Planting_Density,Previous_Crop,Yield_ton_per_ha
    Maize,Region_C,Sandy,7.01,1485.4,19.7,40.3,105.1,Drip,10.2,23.2,Rice,101.48



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
df_crop.printSchema()
df_crop.show(5)
```

    root
     |-- Crop: string (nullable = true)
     |-- Region: string (nullable = true)
     |-- Soil_Type: string (nullable = true)
     |-- Soil_pH: double (nullable = true)
     |-- Rainfall_mm: double (nullable = true)
     |-- Temperature_C: double (nullable = true)
     |-- Humidity_pct: double (nullable = true)
     |-- Fertilizer_Used_kg: double (nullable = true)
     |-- Irrigation: string (nullable = true)
     |-- Pesticides_Used_kg: double (nullable = true)
     |-- Planting_Density: double (nullable = true)
     |-- Previous_Crop: string (nullable = true)
     |-- Yield_ton_per_ha: double (nullable = true)
    


                                                                                    

    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    |  Crop|  Region|Soil_Type|Soil_pH|Rainfall_mm|Temperature_C|Humidity_pct|Fertilizer_Used_kg|Irrigation|Pesticides_Used_kg|Planting_Density|Previous_Crop|Yield_ton_per_ha|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    | Maize|Region_C|    Sandy|   7.01|     1485.4|         19.7|        40.3|             105.1|      Drip|              10.2|            23.2|         Rice|          101.48|
    |Barley|Region_D|     Loam|   5.79|      399.4|         29.1|        55.4|             221.8| Sprinkler|              35.5|             7.4|       Barley|          127.39|
    |  Rice|Region_C|     Clay|   7.24|      980.9|         30.5|        74.4|              61.2| Sprinkler|              40.0|             5.1|        Wheat|           68.99|
    | Maize|Region_D|     Loam|   6.79|     1054.3|         26.4|        62.0|             257.8|      Drip|              42.7|            23.7|         None|          169.06|
    | Maize|Region_D|    Sandy|   5.96|      744.6|         20.4|        70.9|             195.8|      Drip|              25.5|            15.6|        Maize|          118.71|
    +------+--------+---------+-------+-----------+-------------+------------+------------------+----------+------------------+----------------+-------------+----------------+
    only showing top 5 rows
    


## Dataset 2: Lugares famosos del mundo

[Kaggle: World Famous Places](https://www.kaggle.com/datasets/shaistashahid/world-famous-places)



```python
!head -n2 ./world_famous_places_2024.csv
```

    Place_Name,Country,City,Annual_Visitors_Millions,Type,UNESCO_World_Heritage,Year_Built,Entry_Fee_USD,Best_Visit_Month,Region,Tourism_Revenue_Million_USD,Average_Visit_Duration_Hours,Famous_For
    Eiffel Tower,France,Paris,7,Monument/Tower,No,1889,35,May-June/Sept-Oct,Western Europe,95,2.5,"Iconic iron lattice tower, symbol of Paris"



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
df_world.printSchema()
df_world.show(5)
```

    root
     |-- Place_Name: string (nullable = true)
     |-- Country: string (nullable = true)
     |-- City: string (nullable = true)
     |-- Annual_Visitors_Millions: double (nullable = true)
     |-- Type: string (nullable = true)
     |-- UNESCO_World_Heritage: string (nullable = true)
     |-- Year_Built: integer (nullable = true)
     |-- Entry_Fee_USD: decimal(10,0) (nullable = true)
     |-- Best_Visit_Month: string (nullable = true)
     |-- Region: string (nullable = true)
     |-- Tourism_Revenue_Million_USD: decimal(10,0) (nullable = true)
     |-- Average_Visit_Duration_Hours: double (nullable = true)
     |-- Famous_For: string (nullable = true)
    
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |         Place_Name|      Country|            City|Annual_Visitors_Millions|              Type|UNESCO_World_Heritage|Year_Built|Entry_Fee_USD| Best_Visit_Month|        Region|Tourism_Revenue_Million_USD|Average_Visit_Duration_Hours|          Famous_For|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    |       Eiffel Tower|       France|           Paris|                     7.0|    Monument/Tower|                   No|      1889|           35|May-June/Sept-Oct|Western Europe|                         95|                         2.5|Iconic iron latti...|
    |       Times Square|United States|   New York City|                    50.0|    Urban Landmark|                   No|      1904|            0|Apr-June/Sept-Nov| North America|                         70|                         1.5|Bright lights, Br...|
    |      Louvre Museum|       France|           Paris|                     8.7|            Museum|                  Yes|      1793|           22|        Oct-March|Western Europe|                        120|                         4.0|World's most visi...|
    |Great Wall of China|        China|Beijing/Multiple|                    10.0| Historic Monument|                  Yes|      NULL|           10| Apr-May/Sept-Oct|     East Asia|                        180|                         4.0|Ancient defensive...|
    |          Taj Mahal|        India|            Agra|                     7.5|Monument/Mausoleum|                  Yes|      1653|           15|        Oct-March|    South Asia|                         65|                         2.0|White marble maus...|
    +-------------------+-------------+----------------+------------------------+------------------+---------------------+----------+-------------+-----------------+--------------+---------------------------+----------------------------+--------------------+
    only showing top 5 rows
    


## Dataset 3: Registro turístico de Castilla y León

[Datos Abierto Junta de Castilla y León: Registro turístico completo (CSV)](https://datosabiertos.jcyl.es/web/jcyl/set/es/turismo/retu/1285002755102)


```python
!head -n2 ./registro-de-turismo-de-castilla-y-leon.csv
```

    establecimiento;n_registro;codigo;tipo;categoria;especialidades;clase;nombre;direccion;c_postal;provincia;municipio;localidad;nucleo;telefono_1;telefono_2;telefono_3;email;web;q_calidad;posada_real;plazas;gps_longitud;gps_latitud;accesible_a_personas_con_discapacidad;column_27;posicion
    Turismo Activo;47/000047;;Profesional de Turismo Activo;;;;BERNARDO MORO MENENDEZ;Calle Rio Somiedo 1  2º C;33840;Asturias;Somiedo;POLA DE SOMIEDO;POLA DE SOMIEDO;616367277;;;bernardomoro@hotmail.com;;;;;;;;;



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
df_cyl.printSchema()
df_cyl.show(5)
```

    root
     |-- establecimiento: string (nullable = true)
     |-- n_registro: string (nullable = true)
     |-- codigo: string (nullable = true)
     |-- tipo: string (nullable = true)
     |-- categoria: string (nullable = true)
     |-- especialidades: string (nullable = true)
     |-- clase: string (nullable = true)
     |-- nombre: string (nullable = true)
     |-- direccion: string (nullable = true)
     |-- c_postal: string (nullable = true)
     |-- provincia: string (nullable = true)
     |-- municipio: string (nullable = true)
     |-- localidad: string (nullable = true)
     |-- nucleo: string (nullable = true)
     |-- telefono_1: long (nullable = true)
     |-- telefono_2: long (nullable = true)
     |-- telefono_3: long (nullable = true)
     |-- email: string (nullable = true)
     |-- web: string (nullable = true)
     |-- q_calidad: string (nullable = true)
     |-- posada_real: string (nullable = true)
     |-- plazas: integer (nullable = true)
     |-- gps_longitud: double (nullable = true)
     |-- gps_latitud: double (nullable = true)
     |-- accesible_a_personas_con_discapacidad: string (nullable = true)
     |-- column_27: string (nullable = true)
     |-- posicion: string (nullable = true)
    
    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|      categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|           NULL|          NULL| NULL|BERNARDO MORO MEN...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|POLA DE SOMIEDO|POLA DE SOMIEDO| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|    3 Estrellas|          NULL| NULL|        LA SASTRERÍA|Calle VEINTIOCHO ...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|    4 Estrellas|          NULL| NULL|         LAS HAZANAS|       Plaza MAYOR 4|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|
    |Alojam. Turismo R...| 05/001050|  NULL|Casa Rural de Alq...|    4 Estrellas|          NULL| NULL| LA CASITA DEL PAJAR|   Plaza MAYOR 4   B|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     2|  -4.6033333| 40.9438889|                                 NULL|     NULL|40.9438889, -4.60...|
    |               Bares| 05/002525|  NULL|                 Bar|Categoría única|          NULL| NULL|            MARACANA|Calle 28 DE JUNIO...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 666389333|      NULL|      NULL|emo123anatoliev@g...|                NULL|     NULL|       NULL|    42|        NULL|       NULL|                                   Si|     NULL|                NULL|
    +--------------------+----------+------+--------------------+---------------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 5 rows
    