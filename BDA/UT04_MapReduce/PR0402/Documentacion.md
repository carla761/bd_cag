# PR0401: MapReduce (I)

## Ejercicio 1: contando palabras


```python
1. Fichero de Entrada (Input):

Un único fichero de texto (quijote.txt) que contiene la obra completa.
```


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


2. Fase MAP (Mapper):

El mapper debe leer el fichero línea por línea y realizar las siguientes tareas de normalización antes de emitir los pares clave-valor:

- Conversión a minúsculas: todas las palabras deben ser convertidas a minúsculas para que “Caballero” y “caballero” cuenten como la misma palabra.
- Eliminación de puntuación: se deben eliminar todos los signos de puntuación (comas, puntos, punto y coma, interrogaciones, etc.). Por ejemplo, “aventura!” debe tratarse como “aventura”.
- División (tokenización): la línea limpia debe dividirse en palabras individuales (tokens).
- Emisión: por cada palabra válida (token), el mapper debe emitir un par (palabra, 1).


```python
%%writefile mapper_ej1.py
#!usr/bin/env python3
import sys

for line in sys.stdin:
     # Convertir a minúsculas
    line = line.lower()
    # Eliminar signos de puntuación (mantener letras, números y espacios)
    line = re.sub(r'[^\w\s]', '')
    # Tokenizar
    tokens = line.strip().split()
    # Emitir pares (palabra, 1)
    for token in tokens:
        print(f"{token}\t1")

```

    Overwriting mapper_ej0101.py



```python
!cat city_temperature_reduced.csv | python3 mapper_ej0101.py
```

    Overwriting mapper_ej0101.py


3. Fase REDUCE (Reducer):

El reducer recibirá una palabra (clave) y una lista de ‘1’s (valores) asociados a esa palabra.

- Agregación: debe sumar todos los valores (los ‘1’s) para obtener el conteo total de esa palabra específica.
- Emisión: debe emitir el par final (palabra, conteo_total).


```python
%%writefile reducer_ej0101.py
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t",1)
    count = int(count)

    if current_word == word:
        current_word += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word:
        current_count = count   
if current_word:
    print(f"{current_word}\t{current_count}")

```


```python

```
