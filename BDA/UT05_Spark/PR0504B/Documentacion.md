# PR0504B. Limpieza de datos sobre dataset de lugares famosos

Vamos a trabajar con el dataset del portal de datos abiertos de Turismo de Castilla y León. El archivo contiene información sobre alojamientos, bares y restaurantes. Sin embargo, la calidad de los datos es deficiente: hay inconsistencias en mayúsculas/minúsculas, valores nulos, formatos de coordenadas mezclados y columnas redundantes.

Debes utilizar **PySpark** para ingestar, limpiar, normalizar y estructurar estos datos para su posterior análisis en un Dashboard.



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
    26/02/12 08:41:13 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable


    SparkSession iniciada correctamente.


    26/02/12 08:41:33 WARN GarbageCollectionMetrics: To enable non-built-in garbage collector(s) List(G1 Concurrent GC), users should configure it(them) to spark.eventLog.gcMetrics.youngGenerationGarbageCollectors or spark.eventLog.gcMetrics.oldGenerationGarbageCollectors


## 2. Ingesta de datos

El fichero original es un **CSV** (o archivo de texto plano). Debes cargarlo en un `DataFrame` teniendo en cuenta:

* **Delimitador:** Punto y coma (`;`).
* **Cabecera:** La primera fila contiene los nombres de las columnas.
* **Codificación:** Asegúrate de que se lean correctamente los acentos (UTF-8 o ISO-8859-1 según corresponda).



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
                .option("encoding",'UTF-8')
                .load("./registro-de-turismo-de-castilla-y-leon.csv")
           )
df_cyl.show(3)
```

    26/02/12 08:41:39 WARN SparkStringUtils: Truncated the string representation of a plan since it was too large. This behavior can be adjusted by setting 'spark.sql.debug.maxToStringFields'.
                                                                                    

    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|  categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|       NULL|          NULL| NULL|BERNARDO MORO MEN...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|POLA DE SOMIEDO|POLA DE SOMIEDO| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|3 Estrellas|          NULL| NULL|        LA SASTRERÍA|Calle VEINTIOCHO ...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|4 Estrellas|          NULL| NULL|         LAS HAZANAS|       Plaza MAYOR 4|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|
    +--------------------+----------+------+--------------------+-----------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 3 rows
    


## 3. Instrucciones de transformación por campo

A continuación se detallan las reglas de negocio que debes aplicar columna por columna. Debes aplicar estas transformaciones usando las funciones de `pyspark.sql.functions`.


### A. Identificación y categorización

| Campo original        | Transformación requerida |
| --------------------- | --- |
| **`establecimiento`** | Convertir a **Title Case** (primera letra mayúscula, resto minúscula). Eliminar espacios en blanco al inicio y final. |
| **`n_registro`**      | Clave primaria. Eliminar espacios. Si es nulo, eliminar la fila completa (integridad referencial). |
| **`tipo`**            | Limpieza de prefijos. Algunos valores vienen como "p - Actividades..." o "n - Oficinas...". Debes **eliminar los prefijos** "x - " para dejar solo la descripción limpia. |
| **`categoria`**       | Normalización. <br>1. Reemplazar "Categoría única" por "Unica".<br>2. Si contiene "Estrellas" o "Llaves", intentar extraer solo el número (ej: "2 Estrellas"  "2"). Mantener como String. |



```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col

df_A = (
    df_cyl

        # Limpia el nombre del establecimiento:
        # - trim() elimina espacios al inicio y final
        # - initcap() pone la primera letra de cada palabra en mayúscula
        .withColumn('establecimiento', F.initcap(F.trim(F.col('establecimiento'))))

        # Limpia la clave primaria eliminando espacios
        .withColumn('n_registro', F.trim(F.col('n_registro')))

        # Elimina filas donde n_registro sea nulo o vacío (integridad referencial)
        .filter(col('n_registro').isNotNull() & (col('n_registro') != ""))

        # Limpia el campo tipo:
        # elimina prefijos como "p - ", "n - ", "x - "
            #   r""        -> cadena cruda
            #   ^          -> inicio de la cadena
            #   [a-zA-Z]   -> una letra
            #   \s*        -> cero o más espacios
            #   -          -> un guion literal
            #   \s*        -> cero o más espacios
        .withColumn(
            'tipo',
            F.trim(F.regexp_replace(F.col("tipo"), r"^[a-zA-Z]\s*-\s*", ""))
        )

        # Normaliza la categoría única:
        # Reemplaza exactamente "Categoría única" por "Unica"
        .withColumn(
            'categoria',
            F.regexp_replace(F.col('categoria'), "Categoría única", "Unica")
        )

        # Extrae solo el número si la categoría contiene "Estrellas" o "Llaves":
        # - rlike() detecta si aparece alguna de esas palabras (ignorando mayúsculas)
        # - regexp_extract() extrae el número (\d+)
        # - otherwise() deja el valor original si no coincide
        .withColumn(
            'categoria',
            F.when(
                F.col('categoria').rlike(r"(?i)(estrellas|llaves)"),
                F.regexp_extract(F.col('categoria'), r"(\d+)", 1)
            ).otherwise(F.col('categoria'))
        )

        # Selecciona las columnas
        #.select('establecimiento', 'n_registro', 'tipo', 'categoria')
)

df_A.show(3)

```

    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|     NULL|          NULL| NULL|BERNARDO MORO MEN...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|POLA DE SOMIEDO|POLA DE SOMIEDO| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|        3|          NULL| NULL|        LA SASTRERÍA|Calle VEINTIOCHO ...|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|        4|          NULL| NULL|         LAS HAZANAS|       Plaza MAYOR 4|   05296|    Ávila|  Adanero|        ADANERO|        ADANERO| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 3 rows
    


### B. Datos del negocio

| Campo original                            | Transformación requerida |
| ----------------------------------------- | --- |
| **`nombre`**                              | Convertir a **Title Case**. Eliminar espacios dobles dentro del texto (ej: "Rio  Somiedo"  "Rio Somiedo"). |
| **`direccion`**                           | Convertir a **Title Case**. Intenta reemplazar abreviaturas comunes (ej: "C/" por "Calle", "Avda." por "Avenida"), si no, solo normalizar espacios y capitalización. |
| **`c_postal`**                            | Asegurar que sea un **String** de 5 caracteres. Si tiene menos de 5, rellenar con ceros a la izquierda . |
| **`provincia`, `municipio`, `localidad`** | Convertir a **Title Case**. Eliminar espacios. |
| **`nucleo`**                              | Si `nucleo` es nulo o vacío, rellenarlo con el valor de la columna `localidad`. |



```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col

df_B = (
    df_A

        # Normaliza el nombre:
        # - trim() elimina espacios al inicio y final
        # - regexp_replace() elimina espacios dobles internos
        # - initcap() pone cada palabra en Title Case
        .withColumn(
            'nombre',
            F.initcap(
                F.regexp_replace(
                    F.trim(F.col('nombre')),
                    r"\s+",
                    " "
                )
            )
        )

        # Normaliza la dirección:
        # - Primero reemplaza abreviaturas comunes
        # - Luego elimina espacios dobles y aplica Title Case
        .withColumn(
            'direccion',
            F.initcap(
                F.regexp_replace(
                    F.regexp_replace(
                        F.regexp_replace(
                            F.trim(F.col('direccion')),
                            r"(?i)^c\/", "Calle "
                        ),
                        r"(?i)^avda\.?", "Avenida "
                    ),
                    r"\s+",
                    " "
                )
            )
        )

        # Código postal:
        # - Asegura string
        # - Rellena con ceros a la izquierda hasta 5 caracteres
        .withColumn(
            'c_postal',
            F.lpad(F.col('c_postal').cast("string"), 5, "0")
        )

        # Normaliza provincia, municipio y localidad:
        # - trim() elimina espacios
        # - initcap() pone Title Case
        .withColumn('provincia', F.initcap(F.trim(F.col('provincia'))))
        .withColumn('municipio', F.initcap(F.trim(F.col('municipio'))))
        .withColumn('localidad', F.initcap(F.trim(F.col('localidad'))))

        # Nucleo:
        # - Si está vacío o nulo, usar localidad
        .withColumn(
            'nucleo',
            F.when(
                (F.col('nucleo').isNull()) | (F.trim(F.col('nucleo')) == ""),
                F.col('localidad')
            ).otherwise(
                F.initcap(F.trim(F.col('nucleo')))
            )
        )

        # Selección final
        #.select(
         #   'nombre', 'direccion', 'c_postal',
          #  'provincia', 'municipio', 'localidad', 'nucleo'
        #)
)

df_B.show(3)

```

    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|telefono_1|telefono_2|telefono_3|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|     NULL|          NULL| NULL|Bernardo Moro Men...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|Pola De Somiedo|Pola De Somiedo| 616367277|      NULL|      NULL|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|        3|          NULL| NULL|        La Sastrería|Calle Veintiocho ...|   05296|    Ávila|  Adanero|        Adanero|        Adanero| 920307158| 606945069| 609289521|                NULL|www.lasastreriade...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|        4|          NULL| NULL|         Las Hazanas|       Plaza Mayor 4|   05296|    Ávila|  Adanero|        Adanero|        Adanero| 655099974|      NULL|      NULL|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+----------+----------+----------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+
    only showing top 3 rows
    


### C. Contacto 

| Campo original               | Transformación requerida |
| ---------------------------- | --- |
| **`telefono_1`, `_2`, `_3`** | 1. Eliminar espacios internos (ej: "920 206"  "920206").<br>2. Crear una nueva columna llamada `telefonos_contacto` de tipo **Array** que contenga los teléfonos no nulos. <br>3. Eliminar las columnas originales `telefono_1`, `2` y `3`. |
| **`email`** | Convertir a **minúsculas**. Validar con una expresión regular simple si contiene un "@". Si no es válido, convertir a `null`. |
| **`web`** | Convertir a **minúsculas**. Comprobar si empieza por "http://" o "https://". Si no tiene protocolo y el campo no está vacío, añadir "https://" al principio. |




```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col

df_C = (
    df_B

        # Limpieza de teléfonos:
        # - trim() elimina espacios al inicio y final
        # - regexp_replace() elimina espacios internos
        .withColumn('telefono_1', F.regexp_replace(F.trim(col('telefono_1')), r"\s+", ""))
        .withColumn('telefono_2', F.regexp_replace(F.trim(col('telefono_2')), r"\s+", ""))
        .withColumn('telefono_3', F.regexp_replace(F.trim(col('telefono_3')), r"\s+", ""))

        # Construcción del array telefonos_contacto:
        # - array() crea un array con los 3 teléfonos
        # - filter() elimina valores nulos o vacíos
        .withColumn(
            'telefonos_contacto',
            F.expr("""
                filter(
                    array(telefono_1, telefono_2, telefono_3),
                    x -> x is not null AND x != ''
                )
            """)
        )

        # Normalización del email:
        # - lower() convierte a minúsculas
        # - trim() elimina espacios
        # - rlike() valida que contenga '@'
        .withColumn(
            'email',
            F.when(
                F.lower(F.trim(col('email'))).rlike(r".+@.+"),
                F.lower(F.trim(col('email')))
            ).otherwise(F.lit(None))
        )

        # Normalización del campo web:
        # - lower() convierte a minúsculas
        # - trim() elimina espacios
        # - when() añade https:// si no tiene protocolo
        .withColumn(
            'web',
            F.when(
                (F.trim(col('web')) != "") &
                (~F.lower(F.trim(col('web'))).rlike(r"^https?://")),
                F.concat(F.lit("https://"), F.lower(F.trim(col('web'))))
            ).otherwise(
                F.lower(F.trim(col('web')))
            )
        )

        # Eliminación de columnas originales de teléfono
        .drop('telefono_1', 'telefono_2', 'telefono_3')

        # Selección final
        #.select('telefonos_contacto', 'email', 'web')
)

df_C.show(3)

```

    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|  telefonos_contacto|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|     NULL|          NULL| NULL|Bernardo Moro Men...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|Pola De Somiedo|Pola De Somiedo|bernardomoro@hotm...|                NULL|     NULL|       NULL|  NULL|        NULL|       NULL|                                 NULL|     NULL|                NULL|         [616367277]|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|        3|          NULL| NULL|        La Sastrería|Calle Veintiocho ...|   05296|    Ávila|  Adanero|        Adanero|        Adanero|                NULL|https://www.lasas...|     NULL|       NULL|     6|        NULL|       NULL|                                 NULL|     NULL|                NULL|[920307158, 60694...|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|        4|          NULL| NULL|         Las Hazanas|       Plaza Mayor 4|   05296|    Ávila|  Adanero|        Adanero|        Adanero|lashazanas@hotmai...|                NULL|     NULL|       NULL|     8|  -4.6033331| 40.9438881|                                 NULL|     NULL|40.9438881, -4.60...|         [655099974]|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    only showing top 3 rows
    


### D. Datos cuantitativos y Lógicos

| Campo original | Transformación requerida |
| --- | --- |
| **`plazas`** | Castear a tipo **Integer**. Los valores nulos deben ser convertidos a `0`. |
| **`accesible...`** | (Columna `accesible_a_personas_con_discapacidad`). Convertir a tipo **Boolean**. <br>Si el valor es "Si" (o variantes como "si"), asignar `True`.<br>Cualquier otro caso (incluido nulo), asignar `False`. |
| **`q_calidad`, `posada_real`, `especialidades`** | Rellenar valores nulos con el string "No aplica" o "Sin información". |



```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col

df_D = (
    df_C

        # Plazas:
        # - cast() convierte a Integer
        # - coalesce() reemplaza nulos por 0
        .withColumn(
            'plazas',
            F.coalesce(col('plazas').cast('int'), F.lit(0))
        )

        # Accesibilidad:
        # - lower() para comparar en minúsculas
        # - when() asigna True si el valor es "si"
        # - otherwise() asigna False
        .withColumn(
            'accesible_a_personas_con_discapacidad',
            F.when(
                F.lower(F.trim(col('accesible_a_personas_con_discapacidad'))) == "si",
                F.lit(True)
            ).otherwise(F.lit(False))
        )

        # Campos cualitativos con nulos:
        # - fillna() aplica a varias columnas
        .fillna(
            {
                'q_calidad': 'No aplica',
                'posada_real': 'No aplica',
                'especialidades': 'No aplica'
            }
        )

        # Selección final
        #.select(
         #   'plazas',
          #  'accesible_a_personas_con_discapacidad',
          #  'q_calidad',
           # 'posada_real',
            #'especialidades'
        #)
)

df_D.show(3)

```

    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|column_27|            posicion|  telefonos_contacto|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|     NULL|     No aplica| NULL|Bernardo Moro Men...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|Pola De Somiedo|Pola De Somiedo|bernardomoro@hotm...|                NULL|No aplica|  No aplica|     0|        NULL|       NULL|                                false|     NULL|                NULL|         [616367277]|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|        3|     No aplica| NULL|        La Sastrería|Calle Veintiocho ...|   05296|    Ávila|  Adanero|        Adanero|        Adanero|                NULL|https://www.lasas...|No aplica|  No aplica|     6|        NULL|       NULL|                                false|     NULL|                NULL|[920307158, 60694...|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|        4|     No aplica| NULL|         Las Hazanas|       Plaza Mayor 4|   05296|    Ávila|  Adanero|        Adanero|        Adanero|lashazanas@hotmai...|                NULL|No aplica|  No aplica|     8|  -4.6033331| 40.9438881|                                false|     NULL|40.9438881, -4.60...|         [655099974]|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+---------+--------------------+--------------------+
    only showing top 3 rows
    


### E. Geolocalización

Hay tres columnas relacionadas: `gps_longitud`, `gps_latitud` y `posicion`.

A veces `gps_longitud` y `gps_latitud` están vacías, pero la información está en `posicion` (formato "lat, long"). A veces `posicion` está vacía pero las columnas individuales tienen datos.

1. **Limpieza:** asegurar que el separador decimal sea un punto (`.`) y no una coma.
2. **Relleno:**
   - Si `gps_latitud` es nula, intentar extraerla de la primera parte de la columna `posicion` (separando por la coma).
   - Si `gps_longitud` es nula, intentar extraerla de la segunda parte de la columna `posicion`.
3. **Casting:** convertir las columnas finales `latitud` y `longitud` a tipo **Double**.
4. **Eliminación:** eliminar la columna `posicion` y `column_27`  al finalizar.



```python
from pyspark.sql import functions as F
from pyspark.sql.functions import col

df_E = (
    df_D

        # Reemplaza comas decimales por puntos
        .withColumn('gps_latitud',  F.regexp_replace('gps_latitud',  ",", "."))
        .withColumn('gps_longitud', F.regexp_replace('gps_longitud', ",", "."))
        .withColumn('posicion',     F.regexp_replace('posicion',     ",", "."))

        # Extrae latitud desde posicion si gps_latitud está vacía
        .withColumn(
            'gps_latitud',
            F.when(
                (F.col('gps_latitud').isNull()) | (F.trim(F.col('gps_latitud')) == ""),
                F.trim(F.split(F.col('posicion'), "\\s+").getItem(0))
            ).otherwise(F.col('gps_latitud'))
        )

        # Extrae longitud desde posicion si gps_longitud está vacía
        .withColumn(
            'gps_longitud',
            F.when(
                (F.col('gps_longitud').isNull()) | (F.trim(F.col('gps_longitud')) == ""),
                F.trim(F.split(F.col('posicion'), "\\s+").getItem(1))
            ).otherwise(F.col('gps_longitud'))
        )

        # Casting final
        .withColumn('gps_latitud',  F.col('gps_latitud').cast('double'))
        .withColumn('gps_longitud', F.col('gps_longitud').cast('double'))

        # Elimina columnas auxiliares
        .drop('posicion', 'column_27')
)
df_E.show(3)
```

    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+--------------------+
    |     establecimiento|n_registro|codigo|                tipo|categoria|especialidades|clase|              nombre|           direccion|c_postal|provincia|municipio|      localidad|         nucleo|               email|                 web|q_calidad|posada_real|plazas|gps_longitud|gps_latitud|accesible_a_personas_con_discapacidad|  telefonos_contacto|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+--------------------+
    |      Turismo Activo| 47/000047|  NULL|Profesional de Tu...|     NULL|     No aplica| NULL|Bernardo Moro Men...|Calle Rio Somiedo...|   33840| Asturias|  Somiedo|Pola De Somiedo|Pola De Somiedo|bernardomoro@hotm...|                NULL|No aplica|  No aplica|     0|        NULL|       NULL|                                false|         [616367277]|
    |Alojam. Turismo R...| 05/000788|  NULL|Casa Rural de Alq...|        3|     No aplica| NULL|        La Sastrería|Calle Veintiocho ...|   05296|    Ávila|  Adanero|        Adanero|        Adanero|                NULL|https://www.lasas...|No aplica|  No aplica|     6|        NULL|       NULL|                                false|[920307158, 60694...|
    |Alojam. Turismo R...| 05/000696|  NULL|Casa Rural de Alq...|        4|     No aplica| NULL|         Las Hazanas|       Plaza Mayor 4|   05296|    Ávila|  Adanero|        Adanero|        Adanero|lashazanas@hotmai...|                NULL|No aplica|  No aplica|     8|  -4.6033331| 40.9438881|                                false|         [655099974]|
    +--------------------+----------+------+--------------------+---------+--------------+-----+--------------------+--------------------+--------+---------+---------+---------------+---------------+--------------------+--------------------+---------+-----------+------+------------+-----------+-------------------------------------+--------------------+
    only showing top 3 rows
    


## 4. Resultado esperado

El dataframe resultante debe cumplir con este esquema (aproximado):

```text
root
 |-- id_registro: string (nullable = true)
 |-- establecimiento: string (nullable = true)
 |-- categoria_normalizada: string (nullable = true)
 |-- nombre: string (nullable = true)
 |-- direccion_completa: struct (direccion, cp, municipio, provincia)
 |-- contacto: struct (telefonos (Array), email, web)
 |-- capacidad: integer (nullable = false)
 |-- es_accesible: boolean (nullable = false)
 |-- coordenadas: struct (latitud, longitud)

```


```python
df_E.printSchema()

```

    root
     |-- establecimiento: string (nullable = true)
     |-- n_registro: string (nullable = true)
     |-- codigo: string (nullable = true)
     |-- tipo: string (nullable = true)
     |-- categoria: string (nullable = true)
     |-- especialidades: string (nullable = false)
     |-- clase: string (nullable = true)
     |-- nombre: string (nullable = true)
     |-- direccion: string (nullable = true)
     |-- c_postal: string (nullable = true)
     |-- provincia: string (nullable = true)
     |-- municipio: string (nullable = true)
     |-- localidad: string (nullable = true)
     |-- nucleo: string (nullable = true)
     |-- email: string (nullable = true)
     |-- web: string (nullable = true)
     |-- q_calidad: string (nullable = false)
     |-- posada_real: string (nullable = false)
     |-- plazas: integer (nullable = false)
     |-- gps_longitud: double (nullable = true)
     |-- gps_latitud: double (nullable = true)
     |-- accesible_a_personas_con_discapacidad: boolean (nullable = false)
     |-- telefonos_contacto: array (nullable = false)
     |    |-- element: string (containsNull = true)
    



```python
df_final = df_E.select(
    col("n_registro").alias("id_registro"),
    "establecimiento",
    col("categoria").alias("categoria_normalizada"),
    "nombre",
    F.struct("direccion", col("c_postal").alias("cp"), "municipio", "provincia").alias("direccion_completa"),
    F.struct("telefonos_contacto", "email", "web").alias("contacto"),
    col("plazas").alias("capacidad"),
    col("accesible_a_personas_con_discapacidad").alias("es_accesible"),
    F.struct(col("gps_latitud").alias("latitud"), col("gps_longitud").alias("longitud")).alias("coordenadas")
)
```


```python
df_final.printSchema()
```

    root
     |-- id_registro: string (nullable = true)
     |-- establecimiento: string (nullable = true)
     |-- categoria_normalizada: string (nullable = true)
     |-- nombre: string (nullable = true)
     |-- direccion_completa: struct (nullable = false)
     |    |-- direccion: string (nullable = true)
     |    |-- cp: string (nullable = true)
     |    |-- municipio: string (nullable = true)
     |    |-- provincia: string (nullable = true)
     |-- contacto: struct (nullable = false)
     |    |-- telefonos_contacto: array (nullable = false)
     |    |    |-- element: string (containsNull = true)
     |    |-- email: string (nullable = true)
     |    |-- web: string (nullable = true)
     |-- capacidad: integer (nullable = false)
     |-- es_accesible: boolean (nullable = false)
     |-- coordenadas: struct (nullable = false)
     |    |-- latitud: double (nullable = true)
     |    |-- longitud: double (nullable = true)
    



```python
df_final.show(3)
```

    +-----------+--------------------+---------------------+--------------------+--------------------+--------------------+---------+------------+--------------------+
    |id_registro|     establecimiento|categoria_normalizada|              nombre|  direccion_completa|            contacto|capacidad|es_accesible|         coordenadas|
    +-----------+--------------------+---------------------+--------------------+--------------------+--------------------+---------+------------+--------------------+
    |  47/000047|      Turismo Activo|                 NULL|Bernardo Moro Men...|{Calle Rio Somied...|{[616367277], ber...|        0|       false|        {NULL, NULL}|
    |  05/000788|Alojam. Turismo R...|                    3|        La Sastrería|{Calle Veintiocho...|{[920307158, 6069...|        6|       false|        {NULL, NULL}|
    |  05/000696|Alojam. Turismo R...|                    4|         Las Hazanas|{Plaza Mayor 4, 0...|{[655099974], las...|        8|       false|{40.9438881, -4.6...|
    +-----------+--------------------+---------------------+--------------------+--------------------+--------------------+---------+------------+--------------------+
    only showing top 3 rows
    



```python

```
