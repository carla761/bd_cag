# PR0401: MapReduce (I)

## Ejercicio 1: contando palabras

### Fichero de Entrada (Input):

Un único fichero de texto (quijote.txt) que contiene la obra completa.


```python
!mkdir ./PR0401

```

    mkdir: cannot create directory ‘./PR0401’: File exists



```python
!wget https://babel.upm.es/~angel/teaching/pps/quijote.txt
```

    --2025-11-27 09:00:31--  https://babel.upm.es/~angel/teaching/pps/quijote.txt
    Resolving babel.upm.es (babel.upm.es)... 138.100.12.136
    Connecting to babel.upm.es (babel.upm.es)|138.100.12.136|:443... connected.
    ERROR: cannot verify babel.upm.es's certificate, issued by ‘emailAddress=support@fortinet.com,CN=FG34E1TB19900078,OU=Certificate Authority,O=Fortinet,L=Sunnyvale,ST=California,C=US’:
      Self-signed certificate encountered.
    To connect to babel.upm.es insecurely, use `--no-check-certificate'.



```python
!head -n 40 quijote.txt > quijote_reduced.txt # Creo un archivo con las primeras 40 lineas para pruebas
```


```python
!hdfs dfs -mkdir /PR0401
```


```python
!hdfs dfs -put quijote_reduced.txt /PR0401/
```


```python
!hdfs dfs -rm -r /PR0401/salida_filtrada
```

    Deleted /PR0401/salida_filtrada



```python
!hdfs dfs -ls /PR0401/
```

    Found 1 items
    -rw-r--r--   3 root supergroup       1907 2025-11-27 10:05 /PR0401/quijote_reduced.txt


### Fase MAP (Mapper):

El mapper debe leer el fichero línea por línea y realizar las siguientes tareas de normalización antes de emitir los pares clave-valor:

- Conversión a minúsculas: todas las palabras deben ser convertidas a minúsculas para que “Caballero” y “caballero” cuenten como la misma palabra.
- Eliminación de puntuación: se deben eliminar todos los signos de puntuación (comas, puntos, punto y coma, interrogaciones, etc.). Por ejemplo, “aventura!” debe tratarse como “aventura”.
- División (tokenización): la línea limpia debe dividirse en palabras individuales (tokens).
- Emisión: por cada palabra válida (token), el mapper debe emitir un par (palabra, 1).


```python
%%writefile mapper_ej1.py
#!usr/bin/env python3
import sys
import re

for line in sys.stdin:
     # Convertir a minúsculas
    line = line.lower()
    # Eliminar signos de puntuación (mantener letras, números y espacios)
    line = re.sub(r'[^\w\s]', '',line)
    # Tokenizar
    tokens = line.strip().split()
    # Emitir pares (palabra, 1)
    for token in tokens:
        print(f"{token}\t1")

```

    Overwriting mapper_ej1.py



```python
!cat quijote_reduced.txt | python3 mapper_ej1.py
```

    el	1
    ingenioso	1
    hidalgo	1
    don	1
    quijote	1
    de	1
    la	1
    mancha	1
    tasa	1
    yo	1
    juan	1
    gallo	1
    de	1
    andrada	1
    escribano	1
    de	1



### Fase REDUCE (Reducer):

El reducer recibirá una palabra (clave) y una lista de ‘1’s (valores) asociados a esa palabra.

- Agregación: debe sumar todos los valores (los ‘1’s) para obtener el conteo total de esa palabra específica.
- Emisión: debe emitir el par final (palabra, conteo_total).


```python
%%writefile reducer_ej1.py
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t",1)
    count = int(count)

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}, {current_count}")
        current_word = word
        current_count = count   
if current_word:
    print(f"{current_word},{current_count}")

```

    Overwriting reducer_ej1.py



```python
!cat quijote_reduced.txt | python3 mapper_ej1.py | sort | python3 reducer_ej1.py
```

    1604, 1
    a, 4
    acordado, 1
    al, 2
    alcalá, 1
    andrada, 2
    años, 2
    bien, 2
    cada, 1
    certifico, 1
    cervantes, 2
    colegio, 1
    

### Ejercicio 2: Filtrado de palabras representativas
En este ejercicio tienes que:

- Crear una lista (o carga desde un fichero) de palabras no significativas comunes en español (ej. “de”, “la”, “el”, “y”, “en”, “que”, “a”, “los”, “del”, “se”).
- Modificra el mapper para que no emita ningún par clave-valor si la palabra se encuentra en tu lista de palabras no significativas.
- El resultado final será un conteo de palabras significativas, excluyendo las más comunes y menos informativas.

NOTA: si optas por cargar la lista de palabras comunes desde un fichero, éste se deberá ubicar en el sistema de ficheros local y tendrás que referenciarlo mediante el parámetro -file (de forma análoga a como haces con mapper.py y reducer-.py) para que Hadoop lo inyecte a cada uno de los nodos en que se ejecute el mapper. Una vez hecho esto, desde dentro del código Python simplemente debes referenciarlo por su nombre.

### Fase MAP (Mapper):


```python
%%writefile mapper_ej2.py
#!usr/bin/env python3
import sys
import re

# Lista de palabras no significativas
no_words = {"de", "al", "la", "el", "y", "en", "que", "a", "los", "del", "se"}

for line in sys.stdin:
     # Convertir a minúsculas
    line = line.lower()
    # Eliminar signos de puntuación (mantener letras, números y espacios)
    line = re.sub(r'[^\w\s]', '',line)
    # Tokenizar
    tokens = line.strip().split()
    # Emitir pares (palabra, 1)
    for token in tokens:
        if token not in no_words:
            print(f"{token}\t1")
```

    Overwriting mapper_ej2.py



```python
!cat quijote_reduced.txt | python3 mapper_ej2.py
```

    ingenioso	1
    hidalgo	1
    don	1
    quijote	1
    mancha	1
    tasa	1
    yo	1
    juan	1
    gallo	1
    andrada	1
    escribano	1
    cámara	1
    rey	1
    

### Fase REDUCE (Reducer):


```python
%%writefile reducer_ej2.py
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t",1)
    count = int(count)

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word},{current_count}")
        current_word = word
        current_count = count   
if current_word:
    print(f"{current_word},{current_count}")
```

    Overwriting reducer_ej2.py



```python
!cat quijote_reduced.txt | python3 mapper_ej2.py | sort | python3 reducer_ej2.py
```

    1604,1
    acordado,1
    alcalá,1
    andrada,2
    años,2
    bien,2
    cada,1
    certifico,1
    cervantes,2


```python
!hdfs dfs -rm -r /PR0401/salida_filtrada

```

    Deleted /PR0401/salida_filtrada



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_ej2.py \
-file reducer_ej2.py \
-mapper mapper_ej2.py \
-reducer reducer_ej2.py \
-input /PR0401/quijote_reduced.txt \
-output /PR0401/salida_filtrada 

```

```python
!hdfs dfs -ls /PR0401/salida_filtrada/
```


```python
!hdfs dfs -cat /PR0401/salida_filtrada/PART_00000
```


## Ejercicio 3: Ordenación por Frecuencia (Top-N)

En este último ejercicio debes:

- Implementar un segundo trabajo de MapReduce que tome la salida del primero.
- Este segundo trabajo debe reordenar los datos para que la salida final esté ordenada por frecuencia de forma ascendente, mostrando las palabras más usadas primero.
- Tienes que aprovecharte de que Hadoop se encarga de ordenar por la clave, así que en el mapper del segundo trabajo deberías invertir el par (clave, valor) para que sea (valor, clave)

NOTA: en este ejercicio no es necesario el reducer, ya que todo el trabajo se realizará en el mapper y en el shuffle. Si quieres omitir el reducer al ejecutar Hadoop Streaming debes utilizar el parámetro -D mapreduce.job.reduces=0

### Fase MAP (Mapper):


```python
%%writefile mapper_ej3.py
#!usr/bin/env python3
import sys
import re

# Lista de palabras no significativas
no_words = {"de", "al", "la", "el", "y", "en", "que", "a", "los", "del", "se"}

for line in sys.stdin:
     # Convertir a minúsculas
    line = line.lower()
    # Eliminar signos de puntuación (mantener letras, números y espacios)
    line = re.sub(r'[^\w\s]', '',line)
    # Tokenizar
    tokens = line.strip().split()
    # Emitir pares (palabra, 1)
    for token in tokens:
        if token not in no_words:
            print(f"{token}\t1")
```
