# PR0401: MapReduce (I)

## Ejercicio 1: contando palabras

### Fichero de Entrada (Input):

Un único fichero de texto (quijote.txt) que contiene la obra completa.



```python
!mkdir ./PR0401
```


```python
!wget --no-check-certificate https://babel.upm.es/~angel/teaching/pps/quijote.txt 
```

    --2025-12-04 21:58:57--  https://babel.upm.es/~angel/teaching/pps/quijote.txt
    Resolving babel.upm.es (babel.upm.es)... 138.100.12.136
    Connecting to babel.upm.es (babel.upm.es)|138.100.12.136|:443... connected.
    WARNING: cannot verify babel.upm.es's certificate, issued by ‘CN=GEANT TLS RSA 1,O=Hellenic Academic and Research Institutions CA,C=GR’:
      Unable to locally verify the issuer's authority.
    HTTP request sent, awaiting response... 200 OK
    Length: 2141519 (2.0M) [text/plain]
    Saving to: ‘quijote.txt’
    
    quijote.txt         100%[===================>]   2.04M  1.05MB/s    in 1.9s    
    
    2025-12-04 21:59:00 (1.05 MB/s) - ‘quijote.txt’ saved [2141519/2141519]
    



```python
!head -n 40 quijote.txt > quijote_reduced.txt # Creo un archivo con las primeras 40 lineas para pruebas
```


```python
!hdfs dfs -mkdir /PR0401
```


```python
!hdfs dfs -put quijote.txt /PR0401/
```


```python
!hdfs dfs -put quijote_reduced.txt /PR0401/
```


```python
!hdfs dfs -ls /PR0401/
```

    Found 2 items
    -rw-r--r--   3 root supergroup    2141519 2025-12-04 21:59 /PR0401/quijote.txt
    -rw-r--r--   3 root supergroup       1907 2025-12-04 21:59 /PR0401/quijote_reduced.txt


### Fase MAP (Mapper):

El mapper debe leer el fichero línea por línea y realizar las siguientes
tareas de normalización antes de emitir los pares clave-valor:

-   Conversión a minúsculas: todas las palabras deben ser convertidas a
    minúsculas para que “Caballero” y “caballero” cuenten como la misma
    palabra.
-   Eliminación de puntuación: se deben eliminar todos los signos de
    puntuación (comas, puntos, punto y coma, interrogaciones, etc.). Por
    ejemplo, “aventura!” debe tratarse como “aventura”.
-   División (tokenización): la línea limpia debe dividirse en palabras
    individuales (tokens).
-   Emisión: por cada palabra válida (token), el mapper debe emitir un
    par (palabra, 1).


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

    Writing mapper_ej1.py



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
    cámara	1
    del	1
    rey	1
    nuestro	1
    señor	1
    de	1
    los	1
    que	1
    residen	1
    en	1
    su	1
    consejo	1
    certifico	1
    y	1
    doy	1
    fe	1
    que	1
    habiendo	1
    visto	1
    por	1
    los	1
    señores	1
    dél	1
    un	1
    libro	1
    intitulado	1
    el	1
    ingenioso	1
    hidalgo	1
    de	1
    la	1
    mancha	1
    compuesto	1
    por	1
    miguel	1
    de	1
    cervantes	1
    saavedra	1
    tasaron	1
    cada	1
    pliego	1
    del	1
    dicho	1
    libro	1
    a	1
    tres	1
    maravedís	1
    y	1
    medio	1
    el	1
    cual	1
    tiene	1
    ochenta	1
    y	1
    tres	1
    pliegos	1
    que	1
    al	1
    dicho	1
    precio	1
    monta	1
    el	1
    dicho	1
    libro	1
    docientos	1
    y	1
    noventa	1
    maravedís	1
    y	1
    medio	1
    en	1
    que	1
    se	1
    ha	1
    de	1
    vender	1
    en	1
    papel	1
    y	1
    dieron	1
    licencia	1
    para	1
    que	1
    a	1
    este	1
    precio	1
    se	1
    pueda	1
    vender	1
    y	1
    mandaron	1
    que	1
    esta	1
    tasa	1
    se	1
    ponga	1
    al	1
    principio	1
    del	1
    dicho	1
    libro	1
    y	1
    no	1
    se	1
    pueda	1
    vender	1
    sin	1
    ella	1
    y	1
    para	1
    que	1
    dello	1
    conste	1
    di	1
    la	1
    presente	1
    en	1
    valladolid	1
    a	1
    veinte	1
    días	1
    del	1
    mes	1
    de	1
    deciembre	1
    de	1
    mil	1
    y	1
    seiscientos	1
    y	1
    cuatro	1
    años	1
    juan	1
    gallo	1
    de	1
    andrada	1
    testimonio	1
    de	1
    las	1
    erratas	1
    este	1
    libro	1
    no	1
    tiene	1
    cosa	1
    digna	1
    que	1
    no	1
    corresponda	1
    a	1
    su	1
    original	1
    en	1
    testimonio	1
    de	1
    lo	1
    haber	1
    correcto	1
    di	1
    esta	1
    fee	1
    en	1
    el	1
    colegio	1
    de	1
    la	1
    madre	1
    de	1
    dios	1
    de	1
    los	1
    teólogos	1
    de	1
    la	1
    universidad	1
    de	1
    alcalá	1
    en	1
    primero	1
    de	1
    diciembre	1
    de	1
    1604	1
    años	1
    el	1
    licenciado	1
    francisco	1
    murcia	1
    de	1
    la	1
    llana	1
    el	1
    rey	1
    por	1
    cuanto	1
    por	1
    parte	1
    de	1
    vos	1
    miguel	1
    de	1
    cervantes	1
    nos	1
    fue	1
    fecha	1
    relación	1
    que	1
    habíades	1
    compuesto	1
    un	1
    libro	1
    intitulado	1
    el	1
    ingenioso	1
    hidalgo	1
    de	1
    la	1
    mancha	1
    el	1
    cual	1
    os	1
    había	1
    costado	1
    mucho	1
    trabajo	1
    y	1
    era	1
    muy	1
    útil	1
    y	1
    provechoso	1
    nos	1
    pedistes	1
    y	1
    suplicastes	1
    os	1
    mandásemos	1
    dar	1
    licencia	1
    y	1
    facultad	1
    para	1
    le	1
    poder	1
    imprimir	1
    y	1
    previlegio	1
    por	1
    el	1
    tiempo	1
    que	1
    fuésemos	1
    servidos	1
    o	1
    como	1
    la	1
    nuestra	1
    merced	1
    fuese	1
    lo	1
    cual	1
    visto	1
    por	1
    los	1
    del	1
    nuestro	1
    consejo	1
    por	1
    cuanto	1
    en	1
    el	1
    dicho	1
    libro	1
    se	1
    hicieron	1
    las	1
    diligencias	1
    que	1
    la	1
    premática	1
    últimamente	1
    por	1
    nos	1
    fecha	1
    sobre	1
    la	1
    impresión	1
    de	1
    los	1
    libros	1
    dispone	1
    fue	1
    acordado	1
    que	1
    debíamos	1
    mandar	1
    dar	1
    esta	1
    nuestra	1
    cédula	1
    para	1
    vos	1
    en	1
    la	1
    dicha	1
    razón	1
    y	1
    nos	1
    tuvímoslo	1
    por	1
    bien	1
    por	1
    la	1
    cual	1
    por	1
    os	1
    hacer	1
    bien	1
    y	1
    merced	1
    os	1
    damos	1


### Fase REDUCE (Reducer):

El reducer recibirá una palabra (clave) y una lista de ’1’s (valores)
asociados a esa palabra.

-   Agregación: debe sumar todos los valores (los ’1’s) para obtener el
    conteo total de esa palabra específica.
-   Emisión: debe emitir el par final (palabra, conteo_total).


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

    Writing reducer_ej1.py



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
    como, 1
    compuesto, 2
    consejo, 2
    conste, 1
    correcto, 1
    corresponda, 1
    cosa, 1
    costado, 1
    cual, 4
    cuanto, 2
    cuatro, 1
    cámara, 1
    cédula, 1
    damos, 1
    dar, 2
    de, 24
    debíamos, 1
    deciembre, 1
    del, 5
    dello, 1
    di, 2
    dicha, 1
    dicho, 5
    diciembre, 1
    dieron, 1
    digna, 1
    diligencias, 1
    dios, 1
    dispone, 1
    docientos, 1
    don, 1
    doy, 1
    dél, 1
    días, 1
    el, 11
    ella, 1
    en, 9
    era, 1
    erratas, 1
    escribano, 1
    esta, 3
    este, 2
    facultad, 1
    fe, 1
    fecha, 2
    fee, 1
    francisco, 1
    fue, 2
    fuese, 1
    fuésemos, 1
    gallo, 2
    ha, 1
    haber, 1
    habiendo, 1
    había, 1
    habíades, 1
    hacer, 1
    hicieron, 1
    hidalgo, 3
    impresión, 1
    imprimir, 1
    ingenioso, 3
    intitulado, 2
    juan, 2
    la, 12
    las, 2
    le, 1
    libro, 7
    libros, 1
    licencia, 2
    licenciado, 1
    llana, 1
    lo, 2
    los, 5
    madre, 1
    mancha, 3
    mandar, 1
    mandaron, 1
    mandásemos, 1
    maravedís, 2
    medio, 2
    merced, 2
    mes, 1
    miguel, 2
    mil, 1
    monta, 1
    mucho, 1
    murcia, 1
    muy, 1
    no, 3
    nos, 4
    noventa, 1
    nuestra, 2
    nuestro, 2
    o, 1
    ochenta, 1
    original, 1
    os, 4
    papel, 1
    para, 4
    parte, 1
    pedistes, 1
    pliego, 1
    pliegos, 1
    poder, 1
    ponga, 1
    por, 11
    precio, 2
    premática, 1
    presente, 1
    previlegio, 1
    primero, 1
    principio, 1
    provechoso, 1
    pueda, 2
    que, 12
    quijote, 1
    razón, 1
    relación, 1
    residen, 1
    rey, 2
    saavedra, 1
    se, 5
    seiscientos, 1
    servidos, 1
    señor, 1
    señores, 1
    sin, 1
    sobre, 1
    su, 2
    suplicastes, 1
    tasa, 2
    tasaron, 1
    testimonio, 2
    teólogos, 1
    tiempo, 1
    tiene, 2
    trabajo, 1
    tres, 2
    tuvímoslo, 1
    un, 2
    universidad, 1
    valladolid, 1
    veinte, 1
    vender, 3
    visto, 2
    vos, 2
    y, 18
    yo, 1
    últimamente, 1
    útil,1



```python
!hdfs dfs -rm -r /PR0401/salida_ej1
```

    Deleted /PR0401/salida_ej1



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapper_ej1.py,reducer_ej1.py \
-mapper mapper_ej2.py \
-reducer reducer_ej2.py \
-input /PR0401/quijote_reduced.txt \
-output /PR0401/salida_ej1
```

    2025-12-04 22:26:04,939 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    File: file:/media/notebooks/pr0401/mapper_ej1.py,reducer_ej1.py does not exist.
    Try -help for more information
    Streaming Command Failed!


### Ejercicio 2: Filtrado de palabras representativas

En este ejercicio tienes que:

-   Crear una lista (o carga desde un fichero) de palabras no
    significativas comunes en español (ej. “de”, “la”, “el”, “y”, “en”,
    “que”, “a”, “los”, “del”, “se”).
-   Modificra el mapper para que no emita ningún par clave-valor si la
    palabra se encuentra en tu lista de palabras no significativas.
-   El resultado final será un conteo de palabras significativas,
    excluyendo las más comunes y menos informativas.

NOTA: si optas por cargar la lista de palabras comunes desde un fichero,
éste se deberá ubicar en el sistema de ficheros local y tendrás que
referenciarlo mediante el parámetro -file (de forma análoga a como haces
con mapper.py y reducer-.py) para que Hadoop lo inyecte a cada uno de
los nodos en que se ejecute el mapper. Una vez hecho esto, desde dentro
del código Python simplemente debes referenciarlo por su nombre.


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

    Writing mapper_ej2.py



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
    nuestro	1
    señor	1
    residen	1
    su	1
    consejo	1
    certifico	1
    doy	1
    fe	1
    habiendo	1
    visto	1
    por	1
    señores	1
    dél	1
    un	1
    libro	1
    intitulado	1
    ingenioso	1
    hidalgo	1
    mancha	1
    compuesto	1
    por	1
    miguel	1
    cervantes	1
    saavedra	1
    tasaron	1
    cada	1
    pliego	1
    dicho	1
    libro	1
    tres	1
    maravedís	1
    medio	1
    cual	1
    tiene	1
    ochenta	1
    tres	1
    pliegos	1
    dicho	1
    precio	1
    monta	1
    dicho	1
    libro	1
    docientos	1
    noventa	1
    maravedís	1
    medio	1
    ha	1
    vender	1
    papel	1
    dieron	1
    licencia	1
    para	1
    este	1
    precio	1
    pueda	1
    vender	1
    mandaron	1
    esta	1
    tasa	1
    ponga	1
    principio	1
    dicho	1
    libro	1
    no	1
    pueda	1
    vender	1
    sin	1
    ella	1
    para	1
    dello	1
    conste	1
    di	1
    presente	1
    valladolid	1
    veinte	1
    días	1
    mes	1
    deciembre	1
    mil	1
    seiscientos	1
    cuatro	1
    años	1
    juan	1
    gallo	1
    andrada	1
    testimonio	1
    las	1
    erratas	1
    este	1
    libro	1
    no	1
    tiene	1
    cosa	1
    digna	1
    no	1
    corresponda	1
    su	1
    original	1
    testimonio	1
    lo	1
    haber	1
    correcto	1
    di	1
    esta	1
    fee	1
    colegio	1
    madre	1
    dios	1
    teólogos	1
    universidad	1
    alcalá	1
    primero	1
    diciembre	1
    1604	1
    años	1
    licenciado	1
    francisco	1
    murcia	1
    llana	1
    rey	1
    por	1
    cuanto	1
    por	1
    parte	1
    vos	1
    miguel	1
    cervantes	1
    nos	1
    fue	1
    fecha	1
    relación	1
    habíades	1
    compuesto	1
    un	1
    libro	1
    intitulado	1
    ingenioso	1
    hidalgo	1
    mancha	1
    cual	1
    os	1
    había	1
    costado	1
    mucho	1
    trabajo	1
    era	1
    muy	1
    útil	1
    provechoso	1
    nos	1
    pedistes	1
    suplicastes	1
    os	1
    mandásemos	1
    dar	1
    licencia	1
    facultad	1
    para	1
    le	1
    poder	1
    imprimir	1
    previlegio	1
    por	1
    tiempo	1
    fuésemos	1
    servidos	1
    o	1
    como	1
    nuestra	1
    merced	1
    fuese	1
    lo	1
    cual	1
    visto	1
    por	1
    nuestro	1
    consejo	1
    por	1
    cuanto	1
    dicho	1
    libro	1
    hicieron	1
    las	1
    diligencias	1
    premática	1
    últimamente	1
    por	1
    nos	1
    fecha	1
    sobre	1
    impresión	1
    libros	1
    dispone	1
    fue	1
    acordado	1
    debíamos	1
    mandar	1
    dar	1
    esta	1
    nuestra	1
    cédula	1
    para	1
    vos	1
    dicha	1
    razón	1
    nos	1
    tuvímoslo	1
    por	1
    bien	1
    por	1
    cual	1
    por	1
    os	1
    hacer	1
    bien	1
    merced	1
    os	1
    damos	1


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

    Writing reducer_ej2.py



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
    colegio,1
    como,1
    compuesto,2
    consejo,2
    conste,1
    correcto,1
    corresponda,1
    cosa,1
    costado,1
    cual,4
    cuanto,2
    cuatro,1
    cámara,1
    cédula,1
    damos,1
    dar,2
    debíamos,1
    deciembre,1
    dello,1
    di,2
    dicha,1
    dicho,5
    diciembre,1
    dieron,1
    digna,1
    diligencias,1
    dios,1
    dispone,1
    docientos,1
    don,1
    doy,1
    dél,1
    días,1
    ella,1
    era,1
    erratas,1
    escribano,1
    esta,3
    este,2
    facultad,1
    fe,1
    fecha,2
    fee,1
    francisco,1
    fue,2
    fuese,1
    fuésemos,1
    gallo,2
    ha,1
    haber,1
    habiendo,1
    había,1
    habíades,1
    hacer,1
    hicieron,1
    hidalgo,3
    impresión,1
    imprimir,1
    ingenioso,3
    intitulado,2
    juan,2
    las,2
    le,1
    libro,7
    libros,1
    licencia,2
    licenciado,1
    llana,1
    lo,2
    madre,1
    mancha,3
    mandar,1
    mandaron,1
    mandásemos,1
    maravedís,2
    medio,2
    merced,2
    mes,1
    miguel,2
    mil,1
    monta,1
    mucho,1
    murcia,1
    muy,1
    no,3
    nos,4
    noventa,1
    nuestra,2
    nuestro,2
    o,1
    ochenta,1
    original,1
    os,4
    papel,1
    para,4
    parte,1
    pedistes,1
    pliego,1
    pliegos,1
    poder,1
    ponga,1
    por,11
    precio,2
    premática,1
    presente,1
    previlegio,1
    primero,1
    principio,1
    provechoso,1
    pueda,2
    quijote,1
    razón,1
    relación,1
    residen,1
    rey,2
    saavedra,1
    seiscientos,1
    servidos,1
    señor,1
    señores,1
    sin,1
    sobre,1
    su,2
    suplicastes,1
    tasa,2
    tasaron,1
    testimonio,2
    teólogos,1
    tiempo,1
    tiene,2
    trabajo,1
    tres,2
    tuvímoslo,1
    un,2
    universidad,1
    valladolid,1
    veinte,1
    vender,3
    visto,2
    vos,2
    yo,1
    últimamente,1
    útil,1


## Ejercicio 3: Ordenación por Frecuencia (Top-N)

En este último ejercicio debes:

-   Implementar un segundo trabajo de MapReduce que tome la salida del
    primero.
-   Este segundo trabajo debe reordenar los datos para que la salida
    final esté ordenada por frecuencia de forma ascendente, mostrando
    las palabras más usadas primero.
-   Tienes que aprovecharte de que Hadoop se encarga de ordenar por la
    clave, así que en el mapper del segundo trabajo deberías invertir el
    par (clave, valor) para que sea (valor, clave)

NOTA: en este ejercicio no es necesario el reducer, ya que todo el
trabajo se realizará en el mapper y en el shuffle. Si quieres omitir el
reducer al ejecutar Hadoop Streaming debes utilizar el parámetro -D
mapreduce.job.reduces=0

### Fase MAP (Mapper):


```python
%%writefile mapper_ej3.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            word, count = line.split(',')
            print(f"{int(count)}\t{word}")
        except ValueError:
            continue
```

    Writing mapper_ej3.py



```python
!cat quijote_reduced.txt | python3 mapper_ej2.py | sort | python3 reducer_ej2.py | python3 mapper_ej3.py | sort -n
```

    1	1604
    1	acordado
    1	alcalá
    1	cada
    1	certifico
    1	colegio
    1	como
    1	conste
    1	correcto
    1	corresponda
    1	cosa
    1	costado
    1	cuatro
    1	cámara
    1	cédula
    1	damos
    1	debíamos
    1	deciembre
    1	dello
    1	dicha
    1	diciembre
    1	dieron
    1	digna
    1	diligencias
    1	dios
    1	dispone
    1	docientos
    1	don
    1	doy
    1	dél
    1	días
    1	ella
    1	era
    1	erratas
    1	escribano
    1	facultad
    1	fe
    1	fee
    1	francisco
    1	fuese
    1	fuésemos
    1	ha
    1	haber
    1	habiendo
    1	había
    1	habíades
    1	hacer
    1	hicieron
    1	impresión
    1	imprimir
    1	le
    1	libros
    1	licenciado
    1	llana
    1	madre
    1	mandar
    1	mandaron
    1	mandásemos
    1	mes
    1	mil
    1	monta
    1	mucho
    1	murcia
    1	muy
    1	noventa
    1	o
    1	ochenta
    1	original
    1	papel
    1	parte
    1	pedistes
    1	pliego
    1	pliegos
    1	poder
    1	ponga
    1	premática
    1	presente
    1	previlegio
    1	primero
    1	principio
    1	provechoso
    1	quijote
    1	razón
    1	relación
    1	residen
    1	saavedra
    1	seiscientos
    1	servidos
    1	señor
    1	señores
    1	sin
    1	sobre
    1	suplicastes
    1	tasaron
    1	teólogos
    1	tiempo
    1	trabajo
    1	tuvímoslo
    1	universidad
    1	valladolid
    1	veinte
    1	yo
    1	últimamente
    1	útil
    2	andrada
    2	años
    2	bien
    2	cervantes
    2	compuesto
    2	consejo
    2	cuanto
    2	dar
    2	di
    2	este
    2	fecha
    2	fue
    2	gallo
    2	intitulado
    2	juan
    2	las
    2	licencia
    2	lo
    2	maravedís
    2	medio
    2	merced
    2	miguel
    2	nuestra
    2	nuestro
    2	precio
    2	pueda
    2	rey
    2	su
    2	tasa
    2	testimonio
    2	tiene
    2	tres
    2	un
    2	visto
    2	vos
    3	esta
    3	hidalgo
    3	ingenioso
    3	mancha
    3	no
    3	vender
    4	cual
    4	nos
    4	os
    4	para
    5	dicho
    7	libro
    11	por

