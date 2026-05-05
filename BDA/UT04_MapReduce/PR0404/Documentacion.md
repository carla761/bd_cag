# PR0404: Aplicación de patrones MapReduce


```python
!hdfs dfs -mkdir /PR0404
```


```python
!hdfs dfs -put countries_gdp_hist.csv /PR0404
```


```python
!head -n 50 countries_gdp_hist.csv > countries_reduced.csv
```

## Ejercicio 1: Limpieza y Transformación
### Patrón

Filtrado y transformación.

### Objetivo

El *dataset* tiene años muy antiguos y valores nulos. Queremos un *dataset* limpio para años del siglo XXI.

### Implementación

1.  **Mapper**:
      - Lee línea por línea desde `sys.stdin`.
      - **Valida:** ignora cabeceras o líneas con errores de formato.
      - **Filtra:** conserva solo registros donde `year >= 2000` y `total_gdp > 0`.
      - **Transforma:** emite solo `Country Name`, `Year` y `Total GDP`.
      - **Salida:** imprime en STDOUT separado por tabuladores (`\t`).
2.  **Reducer:**
      - En este caso el reducer no tiene que hacer nada




```python
%%writefile mapper_ej1.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    # Ignorar cabecera
    if line.startswith("country_code"):
        continue

    campos = line.split(";")

    # Validación básica: esperamos al menos 9 campos
    if len(campos) < 9:
        continue

    try:
        country_name = campos[4]
        year = int(campos[6])
        total_gdp = float(campos[7])
    except ValueError:
        continue

    # Filtro
    if year >= 2000 and total_gdp > 0:
        print(f"{country_name}\t{year}\t{total_gdp}")

```

    Overwriting mapper_ej1.py



```python
!cat countries_reduced.csv | python3 mapper_ej1.py
```

    ARUBA	2000	1873452513.96648
    ARUBA	2001	1896456983.24022
    ARUBA	2002	1961843575.41899
    ARUBA	2003	2044111731.84358
    ARUBA	2004	2254830726.25698
    ARUBA	2005	2360017318.43575
    ARUBA	2006	2469782681.56425
    ARUBA	2007	2677641340.78212
    ARUBA	2008	2843024581.00559


## Ejercicio 2: Agregación por clave

### Patrón

Resumen numérico (promedio).

### Objetivo

Calcular el PIB promedio histórico por cada Región (Asia, Americas, Europe...).


### Implementación

1.  **Mapper**:
      - Extrae `region_name` y `total_gdp`.
      - Emite: `REGION \t GDP`
2.  **Reducer**:
      - Hadoop envía los datos ordenados por clave, hay que ir sumando los valores y el número de ocurrencias de la clave que llevamos. Cuando cambie la clave se emite el promedio de la región y se resetean contadores.
3.  **Salida esperada:** `AMERICAS  650000.50`, `EUROPE  540000.20`, etc.



```python
%%writefile mapper_ej2.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    # Ignorar cabecera
    if line.startswith("country_code"):
        continue

    campo = line.split(";")

    # Validación básica: esperamos al menos 9 campos
    if len(campo) < 9:
        continue

    try:
        region = campo[1]
        gdp_str = float(campo[7])
    except ValueError:
        continue
    
    print(f"{region}\t{gdp_str}")
```

    Overwriting mapper_ej2.py



```python
!cat countries_reduced.csv | python3 mapper_ej2.py 
```

    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	0.0
    AMERICAS	405586592.178771
    AMERICAS	487709497.206704
    AMERICAS	596648044.692737
    AMERICAS	695530726.256983
    AMERICAS	764804469.273743
    AMERICAS	872067039.106145
    AMERICAS	958659217.877095
    AMERICAS	1083240223.46369
    AMERICAS	1245810055.86592
    AMERICAS	1320670391.06145
    AMERICAS	1379888268.15642
    AMERICAS	1531843575.41899
    AMERICAS	1665363128.49162
    AMERICAS	1722905027.93296
    AMERICAS	1873452513.96648
    AMERICAS	1896456983.24022
    AMERICAS	1961843575.41899
    AMERICAS	2044111731.84358
    AMERICAS	2254830726.25698
    AMERICAS	2360017318.43575
    AMERICAS	2469782681.56425
    AMERICAS	2677641340.78212
    AMERICAS	2843024581.00559



```python
%%writefile reducer_ej2.py
#!/usr/bin/env python3
import sys

current_region = None
sum_gdp = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    region, gdp = line.split("\t")

    try:
        gdp = float(gdp)
    except ValueError:
        continue

    if current_region is None:
        current_region = region

    if region == current_region:
        sum_gdp += gdp
        count += 1
    else:
        # Emitir promedio de la región anterior
        avg = sum_gdp / count if count > 0 else 0
        print(f"{current_region}\t{avg:.2f}")

        # Resetear contadores
        current_region = region
        sum_gdp = gdp
        count = 1

# Emitir última región
if current_region is not None:
    avg = sum_gdp / count if count > 0 else 0
    print(f"{current_region}\t{avg:.2f}")

```

    Overwriting reducer_ej2.py



```python
!cat countries_gdp_hist.csv | python3 mapper_ej2.py | sort | python3 reducer_ej2.py 
```

    AFRICA	17415301365.06
    AMERICAS	250120768754.78
    ASIA	205913293760.72
    EUROPE	213179096872.72
    OCEANIA	32533011434.88


## Ejercicio 3: Máximos por grupo (Filtering/Top-K)
### Patrón

Top-K per Group.

### Objetivo

Encontrar el año de mayor variación de PIB (`gdp_variation`) para cada país.

### Implementación

1.  **Mapper**:
      - Emite: `Country_Name \t Year,Variation` (Concatena año y variación en el valor para no perder el dato del año).
2.  **Reducer**:
      - Para cada país, recorre todas las variaciones.
      - Mantén en memoria solo la variación más alta encontrada hasta el momento y su año asociado.
      - Al cambiar de país, emite: `PAIS \t AÑO_RECORD (VARIACION)`



```python
%%writefile mapper_ej3.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    # Ignorar cabecera
    if line.startswith("country_code"):
        continue

    campo = line.split(";")

    # Validación mínima
    if len(campo) < 9:
        continue

    try:
        country = campo[4]
        year = campo[6]
        variation = float(campo[9])
    except ValueError:
        continue

    print(f"{country}\t{year},{variation}")
```

    Overwriting mapper_ej3.py



```python
!cat countries_reduced.csv | python3 mapper_ej3.py 
```

    ARUBA	1960,0.0
    ARUBA	1961,0.0
    ARUBA	1962,0.0
    ARUBA	1963,0.0
    ARUBA	1964,0.0
    ARUBA	1965,0.0
    ARUBA	1966,0.0
    ARUBA	1967,0.0
    ARUBA	1968,0.0
    ARUBA	1969,0.0
    ARUBA	1970,0.0
    ARUBA	1971,0.0
    ARUBA	1972,0.0
    ARUBA	1973,0.0
    ARUBA	1974,0.0
    ARUBA	1975,0.0
    ARUBA	1976,0.0
    ARUBA	1977,0.0
    ARUBA	1978,0.0
    ARUBA	1979,0.0
    ARUBA	1980,0.0
    ARUBA	1981,0.0
    ARUBA	1982,0.0
    ARUBA	1983,0.0
    ARUBA	1984,0.0
    ARUBA	1985,0.0
    ARUBA	1986,0.0
    ARUBA	1987,16.0784313755902
    ARUBA	1988,18.6486486682331
    ARUBA	1989,12.1298405451924
    ARUBA	1990,3.96140172360629
    ARUBA	1991,7.96287173232642
    ARUBA	1992,5.88235395341866
    ARUBA	1993,7.30769324531406
    ARUBA	1994,8.20390129312089
    ARUBA	1995,2.54714368704694
    ARUBA	1996,1.18578851134656
    ARUBA	1997,7.04687499241221
    ARUBA	1998,1.99198444906199
    ARUBA	1999,1.2380418420716
    ARUBA	2000,7.62292064930222
    ARUBA	2001,4.1820016304779
    ARUBA	2002,-0.944953481157384
    ARUBA	2003,1.11050459944282
    ARUBA	2004,7.29372807096192
    ARUBA	2005,-0.383137672063768
    ARUBA	2006,1.12741146411624
    ARUBA	2007,3.0895443848509
    ARUBA	2008,1.83575517191368



```python
%%writefile reducer_ej3.py
#!/usr/bin/env python3
import sys

current_country = None
max_variation = None
max_year = None

for line in sys.stdin:
    line = line.strip()
    country, value = line.split("\t")
    year, variation = value.split(",")

    try:
        variation = float(variation)
    except ValueError:
        continue

    if current_country is None:
        current_country = country
        max_variation = variation
        max_year = year

    if country == current_country:
        if variation > max_variation:
            max_variation = variation
            max_year = year
    else:
        print(f"{current_country}\t{max_year} ({max_variation})")
        current_country = country
        max_variation = variation
        max_year = year

if current_country is not None:
    print(f"{current_country}\t{max_year} ({max_variation})")

```

    Overwriting reducer_ej3.py



```python
!cat countries_gdp_reduced.csv | python3 mapper_ej3.py | sort | python3 reducer_ej3.py 
```

    AFGHANISTAN	2002 (28.6000011706788)
    ANGOLA	1960 (0.0)
    ARUBA	2021 (24.1326273569798)


## Ejercicio 4: Join (Reduce-Side Join)

### Patrón

Reduce-Side Join.

### Objetivo

Unir el dataset de PIB con un dataset auxiliar de códigos de país para obtener el nombre completo en español (simulado).

### Implementación

1.  **Datos Auxiliares:** necesitas un fichero que relacione los códigos de los países con su respectivo nombre. Puedes utilizar [este *dataset*](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv) disponible en Github.
2.  **Estrategia:**
      - Subir ambos archivos (`gdp.csv` y `codes.csv`) a HDFS.
      - **Mapper**
          - Debe detectar qué archivo está leyendo. Una forma de hacerlo sería contando la cantidad de columnas del fichero. Ten cuidado, porque en un fichero el separador es el punto y coma, mientras que en el otro es la coma, así que lo que puedes hacer es:
            - Separo por comas, si obtengo `X` campos es el fichero `codes.csv`
            - Si no, separo por punto y coma, y compruebo que el número de campos concuerda con el fichero `gdp.csv`
          - Si es `codes.csv`: Emite `CODIGO \t A_NombreEsp` (Tag 'A', que usaré en el *reducer* para distinguir entre uno y otro).
          - Si es `gdp.csv`: Emite `CODIGO \t B_PIB` (Tag 'B').
      - **Reducer**
          - Recibirá todas las líneas de un mismo código juntas (ej. `ESP`).
          - Guarda el nombre en español (Tag A) en una variable.
          - Cuando lleguen los datos del PIB (Tag B), imprime: `Nombre_Español \t PIB`.
3. **Ejecución**: ten en cuenta que, en este caso, el *mapper* recibirá dos ficheros, por lo que habría que invocarlo de la siguiente forma (observa que hay dos `-input`):

    ```bash
    # Ejemplo de ejecución
    mapred streaming \
        -files mapper_join.py,reducer_join.py \
        -input /hdfs/ruta/gdp.csv \
        -input /hdfs/ruta/codes.csv \
        -output /hdfs/ruta/salida_join \
        -mapper mapper_join.py \
        -reducer reducer_join.py
    ```


```python
!hdfs dfs -put codes.csv /PR0404
```


```python
!head -n 50 codes.csv > codes_reduced.csv
```


```python
!cat codes.csv | head -n 5
```

    name,alpha-2,alpha-3,country-code,iso_3166-2,region,sub-region,intermediate-region,region-code,sub-region-code,intermediate-region-code
    Afghanistan,AF,AFG,004,ISO 3166-2:AF,Asia,Southern Asia,"",142,034,""
    Åland Islands,AX,ALA,248,ISO 3166-2:AX,Europe,Northern Europe,"",150,154,""
    Albania,AL,ALB,008,ISO 3166-2:AL,Europe,Southern Europe,"",150,039,""
    Algeria,DZ,DZA,012,ISO 3166-2:DZ,Africa,Northern Africa,"",002,015,""



```python
!cat countries_gdp_hist.csv | head -n 5
```

    country_code;region_name;sub_region_name;intermediate_region;country_name;income_group;year;total_gdp;total_gdp_million;gdp_variation
    ABW;AMERICAS;LATIN AMERICA AND THE CARIBBEAN;CARIBBEAN;ARUBA;INGRESO ALTO;1960;0.0;0.0;0.0
    ABW;AMERICAS;LATIN AMERICA AND THE CARIBBEAN;CARIBBEAN;ARUBA;INGRESO ALTO;1961;0.0;0.0;0.0
    ABW;AMERICAS;LATIN AMERICA AND THE CARIBBEAN;CARIBBEAN;ARUBA;INGRESO ALTO;1962;0.0;0.0;0.0
    ABW;AMERICAS;LATIN AMERICA AND THE CARIBBEAN;CARIBBEAN;ARUBA;INGRESO ALTO;1963;0.0;0.0;0.0
    cat: write error: Broken pipe



```python
%%writefile mapper_ej4.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    campos_coma = line.split(",") # Fichero codes.csv
    # Afghanistan,AF,AFG,004,ISO 3166-2:AF,Asia,Southern Asia,"",142,034,""
    campos_puntocoma = line.split(";") # Fichero countries
    # ABW;AMERICAS;LATIN AMERICA AND THE CARIBBEAN;CARIBBEAN;ARUBA;INGRESO ALTO;1960;0.0;0.0;0.0
    

    if len(campos_coma) == 11 and campos_coma[0] != "codigo":
        codigo = campos_coma[2]  
        nombre_esp = campos_coma[0]
        print(f"{codigo}\tA_{nombre_esp}")

    if len(campos_puntocoma) == 10 and campos_puntocoma[0] != "country_code":
        codigo = campos_puntocoma[0]  
        pib = campos_puntocoma[7]
        print(f"{codigo}\tB_{pib}")


```

    Overwriting mapper_ej4.py



```python
!cat codes.csv countries_gdp_hist.csv | python3 mapper_ej4.py | grep ESP | head -n 20
```

    ESP	A_Spain
    ESP	B_12424514013.7604
    ESP	B_14238126759.7335
    ESP	B_16609632790.5843
    ESP	B_19631714759.6491
    ESP	B_21966876027.2517
    ESP	B_25479619606.5284
    ESP	B_29559436182.9186
    ESP	B_32570905397.2885
    ESP	B_32394326463.759
    ESP	B_37090689287.8552
    ESP	B_40963715236.5106
    ESP	B_46586119760.479
    ESP	B_59090176028.993
    ESP	B_78583355225.5854
    ESP	B_97204522642.0536
    ESP	B_114695060869.565
    ESP	B_118422534195.474
    ESP	B_132354665936.473
    ESP	B_160484969618.056



```python
%%writefile reducer_ej4.py
#!/usr/bin/env python3
import sys

current_code = None
nombre_esp = None
pibs = []

for line in sys.stdin:
    line = line.strip()
    codigo, valor = line.split("\t")

    # Cambio de clave
    if current_code is None:
        current_code = codigo

    if codigo != current_code:
        # Emitir resultados del código anterior
        if nombre_esp is not None:
            for pib in pibs:
                print(f"{nombre_esp}\t{pib}")

        # Reset
        current_code = codigo
        nombre_esp = None
        pibs = []

    # Procesar valores
    if valor.startswith("A_"):
        nombre_esp = valor[2:]
    elif valor.startswith("B_"):
        pibs.append(valor[2:])

# Último código
if nombre_esp is not None:
    for pib in pibs:
        print(f"{nombre_esp}\t{pib}")

```

    Writing reducer_ej4.py



```python
!cat codes.csv countries_gdp_hist.csv \
    | python3 mapper_ej4.py \
    | sort \
    | python3 reducer_ej4.py \
    | grep Spain \
    | head

```

    Spain	1069829382514.67
    Spain	114695060869.565
    Spain	1154667551775.88
    Spain	118422534195.474
    Spain	1206164777553.12
    Spain	12424514013.7604
    Spain	1243015667917.12
    Spain	1261846683275.29
    Spain	1289783836971.21
    Spain	1321754088818.83


## Ejercicio 5: Distribución de Riqueza (Binning Pattern)

### Patrón

Binning (Categorización en cubos).

### Objetivo

Clasificar los registros en rangos de riqueza definidos manualmente para generar un histograma. En lugar de agrupar por una columna existente (como Región), debes crear tu propia clave de agrupación basada en lógica de negocio.

Queremos saber cuántos registros de la historia corresponden a economías "Pequeñas", "Medianas" y "Grandes" basándonos en el `total_gdp_million`.

Las **reglas de negocio (bins)** son:

  - **Economía Pequeña:** GDP \< 10,000 Millones.
  - **Economía Mediana:** 10,000 \<= GDP \< 1,000,000 Millones.
  - **Economía Grande:** GDP \>= 1,000,000 Millones.

### Implementación

1.  **Mapper**

      - Leer `total_gdp_million`.
      - Determinar la categoría según las reglas de negocio.
      - **Salida:** `CATEGORIA \t 1` (Emitimos un 1 para contar).

2.  **Reducer**

      - Suma simple de los "1" recibidos por cada categoría.
      - **Salida esperada:**
        ```text
        Economía Grande    250
        Economía Mediana   1500
        Economía Pequeña   3000
        ```



```python
%%writefile mapper_ej5.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith("country_code"):
        continue

    campo = line.split(";")

    if len(campo) < 9:
        continue

    try:
        gdp_million = float(campo[8])
    except:
        continue

    if gdp_million < 10000:
        categoria = "Economía Pequeña"
    elif gdp_million < 1000000:
        categoria = "Economía Mediana"
    else:
        categoria = "Economía Grande"

    categoria = categoria.strip()

    print(f"{categoria}\t1")


```

    Overwriting mapper_ej5.py



```python
!cat countries_reduced.csv | python3 mapper_ej5.py 
```

    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1
    Economía Pequeña	1



```python
%%writefile reducer_ej5.py
#!/usr/bin/env python3
import sys

current_cat = None
count = 0

for line in sys.stdin:
    line = line.strip()
    categoria, valor = line.split("\t")

    try:
        valor = int(valor)
    except ValueError:
        continue

    if current_cat is None:
        current_cat = categoria

    if categoria == current_cat:
        count += valor
    else:
        print(f"{current_cat}\t{count}")
        current_cat = categoria
        count = valor

# Última categoría
if current_cat is not None:
    print(f"{current_cat}\t{count}")

```

    Overwriting reducer_ej5.py



```python
!cat countries_gdp_hist.csv | python3 mapper_ej5.py | sort | python3 reducer_ej5.py
```

    Economía Grande	423
    Economía Mediana	4777
    Economía Pequeña	8560


## Ejercicio 6: Índice invertido de países (Inverted Index Pattern)

### Patrón

Inverted Index (con deduplicación).

### Objetivo

Generar una lista de búsqueda rápida. Dado un nivel de ingresos (`income_group`), queremos obtener la lista de todos los países únicos que pertenecen a ese grupo.

El *dataset* es una serie temporal. El par `(INGRESO ALTO, ESPAÑA)` aparece unas 60 veces (una vez por cada año desde 1960). El *reducer* debe ser capaz de eliminar duplicados para no listar "España" 60 veces.

### Implementación

1.  **Mapper**

      - Leer `income_group` y `country_name`.
      - **Salida:** `INCOME_GROUP \t COUNTRY_NAME`

2.  **Reducer**

      - Recibir la lista de países para un grupo.
      - Almacenar los países en una estructura que no admita duplicados (como un `set` de Python) mientras se itera sobre la misma clave.
      - Al cambiar de clave, unir el set en un string separado por comas.
      - **Salida esperada:**
        ```text
        INGRESO ALTO    ARUBA, ESPAÑA, FRANCIA, ...
        INGRESO BAJO    AFGANISTÁN, ...
        ```


```python
%%writefile mapper_ej6.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    # Ignorar cabecera
    if line.startswith("country_code"):
        continue

    campos = line.split(";")

    if len(campos) < 9:
        continue

    income_group = campos[5].strip()
    country_name = campos[4].strip()

    print(f"{income_group}\t{country_name}")

```

    Overwriting mapper_ej6.py



```python
!cat countries_reduced.csv | python3 mapper_ej6.py 
```

    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA
    INGRESO ALTO	ARUBA



```python
%%writefile reducer_ej6.py
#!/usr/bin/env python3
import sys

current_group = None
countries = set()

for line in sys.stdin:
    line = line.strip()
    group, country = line.split("\t")

    if current_group is None:
        current_group = group

    if group != current_group:
        # Emitir grupo anterior
        lista = ", ".join(sorted(countries))
        print(f"{current_group}\t{lista}")

        # Reset
        current_group = group
        countries = set()

    countries.add(country)

# Último grupo
if current_group is not None:
    lista = ", ".join(sorted(countries))
    print(f"{current_group}\t{lista}")

```

    Overwriting reducer_ej6.py



```python
!cat countries_gdp_hist.csv | python3 mapper_ej6.py | sort | python3 reducer_ej6.py
```

    INGRESO ALTO	AMERICAN SAMOA, ANDORRA, ANTIGUA AND BARBUDA, ARUBA, AUSTRALIA, AUSTRIA, BAHAMAS, BAHRAIN, BARBADOS, BELGIUM, BERMUDA, BRUNEI DARUSSALAM, BULGARIA, CANADA, CAYMAN ISLANDS, CHILE, CROATIA, CURAÇAO, CYPRUS, CZECHIA, DENMARK, ESTONIA, FAROE ISLANDS, FINLAND, FRANCE, FRENCH POLYNESIA, GERMANY, GIBRALTAR, GREECE, GREENLAND, GUAM, GUYANA, HONG KONG, HUNGARY, ICELAND, IRELAND, ISLE OF MAN, ISRAEL, ITALY, JAPAN, KOREA, REPUBLIC OF, KUWAIT, LATVIA, LIECHTENSTEIN, LITHUANIA, LUXEMBOURG, MACAO, MALTA, MONACO, NAURU, NETHERLANDS, NEW CALEDONIA, NEW ZEALAND, NORTHERN MARIANA ISLANDS, NORWAY, OMAN, PALAU, PANAMA, POLAND, PORTUGAL, PUERTO RICO, QATAR, ROMANIA, RUSSIAN FEDERATION, SAINT KITTS AND NEVIS, SAINT MARTIN (FRENCH PART), SAN MARINO, SAUDI ARABIA, SEYCHELLES, SINGAPORE, SINT MAARTEN (DUTCH PART), SLOVAKIA, SLOVENIA, SPAIN, SWEDEN, SWITZERLAND, TRINIDAD AND TOBAGO, TURKS AND CAICOS ISLANDS, UNITED ARAB EMIRATES, UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND, UNITED STATES OF AMERICA, URUGUAY, VIRGIN ISLANDS (BRITISH), VIRGIN ISLANDS (U.S.)
    INGRESO MEDIANO ALTO	ALBANIA, ALGERIA, ARGENTINA, ARMENIA, AZERBAIJAN, BELARUS, BELIZE, BOSNIA AND HERZEGOVINA, BOTSWANA, BRAZIL, CHINA, COLOMBIA, COSTA RICA, CUBA, DOMINICA, DOMINICAN REPUBLIC, ECUADOR, EL SALVADOR, EQUATORIAL GUINEA, FIJI, GABON, GEORGIA, GRENADA, GUATEMALA, INDONESIA, IRAN (ISLAMIC REPUBLIC OF), IRAQ, JAMAICA, KAZAKHSTAN, LIBYA, MALAYSIA, MALDIVES, MARSHALL ISLANDS, MAURITIUS, MEXICO, MOLDOVA, REPUBLIC OF, MONGOLIA, MONTENEGRO, NAMIBIA, NORTH MACEDONIA, PARAGUAY, PERU, SAINT LUCIA, SAINT VINCENT AND THE GRENADINES, SERBIA, SOUTH AFRICA, SURINAME, THAILAND, TONGA, TURKEY, TURKMENISTAN, TUVALU, UKRAINE
    NO CLASIFICADO	VENEZUELA (BOLIVARIAN REPUBLIC OF)
    PAÍSES DE INGRESO BAJO	AFGHANISTAN, BURKINA FASO, BURUNDI, CENTRAL AFRICAN REPUBLIC, CHAD, CONGO, DEMOCRATIC REPUBLIC OF THE, ERITREA, ETHIOPIA, GAMBIA, GUINEA-BISSAU, KOREA (DEMOCRATIC PEOPLE'S REPUBLIC OF), LIBERIA, MADAGASCAR, MALAWI, MALI, MOZAMBIQUE, NIGER, RWANDA, SIERRA LEONE, SOMALIA, SOUTH SUDAN, SUDAN, SYRIAN ARAB REPUBLIC, TOGO, UGANDA, YEMEN
    PAÍSES DE INGRESO MEDIANO BAJO	ANGOLA, BANGLADESH, BENIN, BHUTAN, BOLIVIA (PLURINATIONAL STATE OF), CABO VERDE, CAMBODIA, CAMEROON, COMOROS, CONGO, CÔTE D'IVOIRE, DJIBOUTI, EGYPT, ESWATINI, GHANA, GUINEA, HAITI, HONDURAS, INDIA, JORDAN, KENYA, KIRIBATI, KYRGYZSTAN, LAO PEOPLE'S DEMOCRATIC REPUBLIC, LEBANON, LESOTHO, MAURITANIA, MICRONESIA (FEDERATED STATES OF), MOROCCO, MYANMAR, NEPAL, NICARAGUA, NIGERIA, PAKISTAN, PALESTINE, STATE OF, PAPUA NEW GUINEA, PHILIPPINES, SAMOA, SAO TOME AND PRINCIPE, SENEGAL, SOLOMON ISLANDS, SRI LANKA, TAJIKISTAN, TANZANIA, UNITED REPUBLIC OF, TIMOR-LESTE, TUNISIA, UZBEKISTAN, VANUATU, VIET NAM, ZAMBIA, ZIMBABWE

