# PR0402: MapReduce (II)


```python
!hdfs dfs -mkdir /PR0402/
```

    mkdir: `/PR0402': File exists



```python
!hdfs dfs -put ./city_temperature.csv /PR0402/

```

    put: `/PR0402/city_temperature.csv': File exists



```python
!hdfs dfs -ls /PR0402
```

    Found 2 items
    -rw-r--r--   3 root supergroup  140600832 2025-12-03 19:04 /PR0402/city_temperature.csv
    drwxr-xr-x   - root supergroup          0 2025-12-04 19:42 /PR0402/salida_ej1


## Ejercicio 1: temperatura máxima por ciudad
Utiliza MapReduce para encontrar la temperatura máxima registrada para cada ciudad. Para ello tienes que tener en cuenta lo siguiente:

- Lógica mapper: lee cada línea de los datos y emite el par (ciudad, temperatura)
- Lógica reducer: como recibirá todas las líneas de una misma ciudad consecutivamente, emite únicamente la línea con mayor valor en temperatura.


```python
!hdfs dfs -rm -r /PR0402/salida_ej1
```

    Deleted /PR0402/salida_ej1



```python
!head -n 40 city_temperature.csv > city_temperature_reduced.csv # Creo un archivo con las primeras 40 lineas para pruebas
```


```python
!hdfs dfs -put ./city_temperature_reduced.csv /PR0402/
```


```python
!hdfs dfs -ls /PR0402
```

    Found 2 items
    -rw-r--r--   3 root supergroup  140600832 2025-12-03 19:04 /PR0402/city_temperature.csv
    -rw-r--r--   3 root supergroup       1560 2025-12-04 20:13 /PR0402/city_temperature_reduced.csv



```python
%%writefile mapper_ej1.py
#!usr/bin/env python3
import sys

for line in sys.stdin:
    region, country, state, city, month, day, year, temp = line.strip().split(",")
    try:
        temp_c = (float(temp) - 32) / 1.8
        print(f"{city}\t{temp_c}")
    except ValueError:
        continue
```

    Overwriting mapper_ej1.py



```python
%%writefile reducer_ej1.py
#!/usr/bin/env python3
import sys

ciudad_actual = None
max_temp = None

for line in sys.stdin:
    ciudad, temp = line.strip().split("\t")
    temp = float(temp)

    if ciudad == ciudad_actual:
        max_temp = max_temp if max_temp > temp else temp
    else:
        if ciudad_actual:
            print(f"{ciudad_actual}\t{max_temp}")
        ciudad_actual = ciudad
        max_temp = float("-inf")

if ciudad_actual:
    print(f"{ciudad_actual}\t{max_temp}")
```

    Overwriting reducer_ej1.py



```python
!cat city_temperature.csv | python3 mapper_ej1.py | sort | python3 reducer_ej1.py
```

    Abidjan	31.44444444444444
    Abilene	34.55555555555556
    Abu Dhabi	41.83333333333333
    Addis Ababa	25.0
    Akron Canton	30.05555555555555
    Albany	31.11111111111111
    Albuquerque	31.888888888888893
    Algiers	35.888888888888886
    Allentown	32.83333333333333
    Almaty	32.72222222222222
    Amarillo	33.61111111111111
    Amman	35.22222222222222
    Amsterdam	29.72222222222222
    Anchorage	24.055555555555554
    Ankara	31.055555555555557
    Antananarivo	25.833333333333332
    Ashabad	39.0
    Asheville	29.499999999999996
    Athens	34.61111111111111
    Atlanta	33.77777777777778
    Atlantic City	34.05555555555555
    Auckland	24.111111111111114
    Austin	34.72222222222222
    Baltimore	33.27777777777778
    Bangkok	33.888888888888886
    Bangui	34.27777777777778
    Banjul	34.22222222222222
    Barcelona	30.33333333333333
    Baton Rouge	32.333333333333336
    Beijing	33.833333333333336
    Beirut	32.83333333333333
    Belfast	25.33333333333333
    Belgrade	33.27777777777778
    Belize City	33.833333333333336
    Bern	28.72222222222222
    Bilbao	34.77777777777777
    Billings	32.55555555555555
    Birmingham	32.77777777777778
    Bishkek	32.83333333333333
    Bismarck	33.166666666666664
    Bissau	37.83333333333333
    Bogota	19.27777777777778
    Boise	34.55555555555556
    Bombay (Mumbai)	33.666666666666664
    Bonn	30.500000000000004
    Bordeaux	31.555555555555554
    Boston	32.611111111111114
    Brasilia	30.944444444444446
    Bratislava	29.72222222222222
    Brazzaville	31.5
    Bridgeport	30.555555555555554
    Bridgetown	31.11111111111111
    Brisbane	30.72222222222222
    Brownsville	32.88888888888889
    Brussels	29.666666666666668
    Bucharest	33.0
    Budapest	31.22222222222222
    Buenos Aires	32.72222222222222
    Buffalo	29.111111111111114
    Bujumbura	31.722222222222218
    Burlington	31.555555555555554
    Cairo	37.88888888888889
    Calcutta	36.0
    Calgary	26.166666666666664
    Canberra	34.0
    Capetown	28.777777777777775
    Caracas	32.16666666666667
    Caribou	28.555555555555557
    Casper	30.611111111111107
    Charleston	33.11111111111111
    Charlotte	32.44444444444445
    Chattanooga	33.72222222222222
    Chengdu	32.55555555555555
    Chennai (Madras)	36.611111111111114
    Cheyenne	29.27777777777778
    Chicago	33.5
    Cincinnati	31.77777777777778
    Cleveland	30.666666666666668
    Colombo	31.277777777777775
    Colorado Springs	30.222222222222225
    Columbia	33.77777777777778
    Columbus	36.5
    Conakry	31.999999999999996
    Concord	32.27777777777777
    Copenhagen	25.27777777777778
    Corpus Christi	33.888888888888886
    Cotonou	31.44444444444444
    Dakar	30.555555555555554
    Dallas Ft Worth	36.77777777777778
    Damascus	35.27777777777778
    Dar Es Salaam	32.44444444444445
    Dayton	32.88888888888889
    Daytona Beach	30.999999999999996
    Delhi	39.833333333333336
    Denver	31.277777777777775
    Des Moines	33.888888888888886
    Detroit	31.44444444444444
    Dhahran	42.11111111111111
    Dhaka	33.0
    Doha	42.5
    Dubai	41.94444444444444
    Dublin	21.166666666666664
    Duluth	29.777777777777775
    Dusanbe	36.44444444444444
    Edmonton	28.22222222222222
    El Paso	36.72222222222222
    Elkins	33.61111111111111
    Erie	30.222222222222225
    Eugene	29.666666666666668
    Evansville	33.05555555555556
    Fairbanks	26.38888888888889
    Fargo	33.0
    Flagstaff	28.61111111111111
    Flint	31.888888888888893
    Fort Smith	38.166666666666664
    Fort Wayne	31.888888888888893
    Frankfurt	29.555555555555557
    Freetown	31.5
    Fresno	39.22222222222222
    Geneva	29.555555555555557
    Georgetown	32.55555555555555
    Goodland	33.22222222222222
    Grand Junction	33.5
    Grand Rapids	31.722222222222218
    Great Falls	37.83333333333333
    Green Bay	32.94444444444444
    Greensboro	32.44444444444445
    Guadalajara	31.38888888888889
    Guangzhou	34.833333333333336
    Guatemala City	26.555555555555554
    Guayaquil	32.22222222222222
    Halifax	26.944444444444443
    Hamburg	32.11111111111111
    Hamilton	29.666666666666668
    Hanoi	35.55555555555556
    Harrisburg	33.333333333333336
    Hartford Springfield	32.11111111111111
    Havana	31.277777777777775
    Helena	31.833333333333332
    Helsinki	26.555555555555554
    Hong Kong	33.55555555555556
    Honolulu	30.666666666666668
    Houston	33.888888888888886
    Huntsville	33.05555555555556
    Indianapolis	34.44444444444444
    Islamabad	39.111111111111114
    Istanbul	31.5
    Jackson	31.999999999999996
    Jacksonville	31.277777777777775
    Jakarta	32.55555555555555
    Juneau	22.22222222222222
    Kampala	28.27777777777778
    Kansas City	33.666666666666664
    Karachi	37.611111111111114
    Katmandu	30.33333333333333
    Kiev	30.500000000000004
    Knoxville	33.166666666666664
    Kuala Lumpur	31.999999999999996
    Kuwait	43.333333333333336
    La Paz	17.444444444444443
    Lagos	34.0
    Lake Charles	34.44444444444444
    Lansing	31.166666666666664
    Las Vegas	41.666666666666664
    Lexington	31.944444444444443
    Libreville	30.444444444444443
    Lilongwe	32.611111111111114
    Lima	27.666666666666664
    Lincoln	33.27777777777778
    Lisbon	35.72222222222222
    Little Rock	35.22222222222222
    Lome	32.27777777777777
    London	28.555555555555557
    Los Angeles	30.0
    Louisville	34.0
    Lubbock	34.49999999999999
    Lusaka	34.0
    Macon	32.83333333333333
    Madison	32.55555555555555
    Madrid	32.77777777777778
    Managua	34.38888888888889
    Manama	39.61111111111111
    Manila	33.27777777777778
    Maputo	35.33333333333333
    Medford	36.27777777777778
    Melbourne	33.77777777777778
    Memphis	34.22222222222222
    Mexico City	25.0
    Miami Beach	31.77777777777778
    Midland Odessa	34.77777777777777
    Milan	30.77777777777778
    Milwaukee	33.44444444444444
    Minneapolis St. Paul	33.333333333333336
    Minsk	28.61111111111111
    Mobile	31.611111111111114
    Monterrey	39.66666666666667
    Montgomery	32.88888888888889
    Montreal	29.222222222222218
    Montvideo	30.77777777777778
    Moscow	30.72222222222222
    Munich	27.666666666666664
    Muscat	41.05555555555556
    Nairobi	28.000000000000004
    Nashville	34.49999999999999
    Nassau	33.22222222222222
    New Orleans	32.27777777777777
    New York City	34.27777777777778
    Newark	35.33333333333333
    Niamey	39.33333333333333
    Nicosia	39.166666666666664
    Norfolk	34.0
    North Platte	32.83333333333333
    Nouakchott	37.5
    Oklahoma City	36.166666666666664
    Omaha	34.0
    Orlando	31.833333333333332
    Osaka	33.888888888888886
    Oslo	25.05555555555555
    Ottawa	29.388888888888893
    Paducah	33.22222222222222
    Panama City	32.55555555555555
    Paramaribo	32.5
    Paris	33.05555555555556
    Peoria	32.5
    Perth	35.111111111111114
    Philadelphia	33.833333333333336
    Phoenix	42.05555555555556
    Pittsburgh	31.333333333333336
    Pocatello	32.44444444444445
    Port au Prince	36.333333333333336
    Portland	31.888888888888893
    Prague	28.666666666666664
    Pristina	31.999999999999996
    Pueblo	34.833333333333336
    Pyongyang	31.888888888888893
    Quebec	28.27777777777778
    Quito	20.555555555555554
    Rabat	36.11111111111111
    Raleigh Durham	32.77777777777778
    Rangoon	37.388888888888886
    Rapid City	33.27777777777778
    Regina	28.444444444444446
    Reno	33.77777777777778
    Reykjavik	20.944444444444446
    Rhode Island	31.77777777777778
    Richmond	34.166666666666664
    Riga	27.333333333333336
    Rio de Janeiro	34.111111111111114
    Riyadh	40.55555555555556
    Roanoke	32.83333333333333
    Rochester	30.11111111111111
    Rockford	32.55555555555555
    Rome	29.888888888888886
    Sacramento	35.72222222222222
    Salem	32.5
    Salt Lake City	33.44444444444444
    San Angelo	35.72222222222222
    San Antonio	35.22222222222222
    San Diego	30.27777777777778
    San Francisco	28.166666666666668
    San Jose	29.777777777777775
    San Juan Puerto Rico	31.77777777777778
    Santo Domingo	30.77777777777778
    Sao Paulo	31.77777777777778
    Sapporo	28.055555555555554
    Sault Ste Marie	26.999999999999996
    Savannah	31.722222222222218
    Seattle	30.944444444444446
    Seoul	32.22222222222222
    Shanghai	36.0
    Shenyang	32.611111111111114
    Shreveport	35.22222222222222
    Singapore	31.38888888888889
    Sioux City	32.611111111111114
    Sioux Falls	34.61111111111111
    Skopje	31.11111111111111
    Sofia	30.0
    South Bend	31.888888888888893
    Spokane	34.0
    Springfield	33.77777777777778
    St Louis	35.72222222222222
    Stockholm	26.22222222222222
    Sydney	36.0
    Syracuse	30.833333333333332
    Taipei	34.44444444444444
    Tallahassee	33.77777777777778
    Tampa St. Petersburg	32.666666666666664
    Tashkent	35.22222222222222
    Tbilisi	32.55555555555555
    Tegucigalpa	31.11111111111111
    Tel Aviv	31.38888888888889
    Tirana	33.61111111111111
    Tokyo	32.55555555555555
    Toledo	32.11111111111111
    Topeka	35.33333333333333
    Toronto	31.555555555555554
    Tucson	38.666666666666664
    Tulsa	38.0
    Tunis	35.77777777777778
    Tupelo	33.77777777777778
    Ulan-bator	30.833333333333332
    Vancouver	28.388888888888886
    Vienna	30.11111111111111
    Vientiane	36.11111111111111
    Waco	35.61111111111111
    Warsaw	29.111111111111114
    Washington	33.77777777777778
    Washington DC	33.77777777777778
    West Palm Beach	31.833333333333332
    Wichita	35.61111111111111
    Wichita Falls	36.94444444444444
    Wilkes Barre	31.333333333333336
    Wilmington	32.05555555555556
    Windhoek	33.44444444444444
    Winnipeg	30.33333333333333
    Yakima	36.5
    Yerevan	33.22222222222222
    Youngstown	30.38888888888889
    Yuma	41.94444444444444
    Zagreb	30.833333333333332
    Zurich	28.000000000000004


## Ejercicio 2: media histórica por país

Calcula la temperatura media histórica para cada país. El proceso es similar al anterior, en el reducer debes ir recordando todos los datos que te lleguen de un mismo país y, cuando pase al siguiente país, calcular la media y emitirlos.


```python
%%writefile mapper_ej2.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or "Region" in line: continue
    
    parts = line.split(",")
    if len(parts) < 8: continue
        
    country = parts[1] # Campo País
    temp_str = parts[7]
    
    try:
        temp = float(temp_str)
        if temp == -99.0: continue
        # Convertimos a Celsius para que la media tenga sentido humano
        temp_c = (temp - 32) / 1.8
        print(f"{country}\t{temp_c}")
    except ValueError:
        continue
```

    Overwriting mapper_ej2.py



```python
%%writefile reducer_ej2.py
#!/usr/bin/env python3
import sys

current_country = None
accum_temp = 0.0
count = 0

for line in sys.stdin:
    try:
        country, temp = line.strip().split("\t")
        temp = float(temp)
    except ValueError:
        continue

    if country == current_country:
        accum_temp += temp
        count += 1
    else:
        if current_country and count > 0:
            print(f"{current_country}\t{accum_temp/count}")
        current_country = country
        accum_temp = temp
        count = 1

if current_country and count > 0:
    print(f"{current_country}\t{accum_temp/count}")
```

    Overwriting reducer_ej2.py



```python
!cat city_temperature.csv | python3 mapper_ej2.py | sort | python3 reducer_ej2.py
```

    Albania	16.186243317061823
    Algeria	17.98474343696956
    Argentina	17.175832641220886
    Australia	17.09979759334121
    Austria	10.816354016354055
    Bahamas	25.87012577472152
    Bahrain	27.343931957076148
    Bangladesh	25.955736224028904
    Barbados	27.261714643137157
    Belarus	7.439150218286847
    Belgium	10.839924466575278
    Belize	27.322744758969005
    Benin	27.616857810934274
    Bermuda	21.999910039582605
    Bolivia	7.5036434808792025
    Brazil	22.21278650631996
    Bulgaria	10.902391062012324
    Burundi	23.161010558069364
    Canada	5.855018514763016
    Central African Republic	26.01213732516476
    China	15.910204912209828
    Colombia	13.565590111642539
    Congo	25.650679138579747
    Costa Rica	22.721522453449946
    Croatia	12.451656013212776
    Cuba	24.36077511423884
    Cyprus	19.984801090792423
    Czech Republic	8.93302776574758
    Denmark	8.557137186981302
    Dominican Republic	26.512131772321993
    Egypt	22.59780475175512
    Equador	20.756860027013676
    Ethiopia	17.19465832905563
    Finland	5.928946861995133
    France	12.988705209274288
    Gabon	26.599174234076845
    Gambia	26.121881937142298
    Georgia	13.524912622937453
    Germany	9.966953613438982
    Greece	18.47486439195103
    Guatemala	19.36883531062618
    Guinea	27.547361585383733
    Guinea-Bissau	27.964185378198206
    Guyana	28.525488972118193
    Haiti	29.63801008711606
    Honduras	22.034958157718066
    Hong Kong	24.23786752321825
    Hungary	10.872391228513335
    Iceland	5.290311909831238
    India	26.9652888804587
    Indonesia	28.536794011859605
    Ireland	9.73980248517434
    Israel	21.249324753733664
    Italy	14.292362201408647
    Ivory Coast	26.803846058900348
    Japan	13.525137335097595
    Jordan	18.180847351575053
    Kazakhstan	9.934591308534948
    Kenya	19.717192652775513
    Kuwait	26.97793097624823
    Kyrgyzstan	11.930093565805192
    Laos	27.253136687175797
    Latvia	7.4262605372325545
    Lebanon	21.284444926697528
    Macedonia	12.632174143561159
    Madagascar	18.584113284047795
    Malawi	21.128886364592596
    Malaysia	27.94384582493425
    Mauritania	25.618538433337402
    Mexico	20.5933046625305
    Mongolia	-0.9315933436961312
    Morocco	17.434367513032512
    Mozambique	23.747208102279856
    Myanmar (Burma)	27.72098821972888
    Namibia	20.73661575252643
    Nepal	18.91165493708676
    New Zealand	15.51427054294435
    Nicaragua	27.65843221039506
    Nigeria	28.88064440176864
    North Korea	11.04097998009068
    Norway	5.444085049156004
    Oman	28.31448345712358
    Pakistan	24.409508617934087
    Panama	27.23135455952048
    Peru	19.49486516492826
    Philippines	27.98027488676902
    Poland	9.029353736586287
    Portugal	17.014030458565227
    Qatar	28.312342736061414
    Romania	11.577622604741816
    Russia	7.647454989401385
    Saudi Arabia	26.80721154426231
    Senegal	24.62826257151462
    Serbia-Montenegro	10.130667624816073
    Sierra Leone	27.620575863069252
    Singapore	27.911776382272315
    Slovakia	11.093236348759355
    South Africa	16.96285263816668
    South Korea	11.891277404760144
    Spain	15.533389065306505
    Sri Lanka	27.470461131095128
    Suriname	26.49699521866919
    Sweden	7.5602849681697215
    Switzerland	10.254699372614127
    Syria	17.651327059958913
    Taiwan	23.27025911968273
    Tajikistan	15.965204603215437
    Tanzania	26.235433683391705
    Thailand	28.843792777681468
    The Netherlands	10.72483879505319
    Togo	27.502626770214835
    Tunisia	19.493374494511883
    Turkey	13.155114647995786
    Turkmenistan	17.66053355635566
    US	13.685399419915418
    Uganda	22.549740515518668
    Ukraine	8.984116670276503
    United Arab Emirates	28.46746397087587
    United Kingdom	10.96601356806322
    Uruguay	16.45345589386113
    Uzbekistan	15.848885979586418
    Venezuela	27.291994055232706
    Vietnam	24.11941735885405
    Yugoslavia	12.516619748808987
    Zambia	21.159532768893076


## Ejercicio 3: conteo de días calurosos por ciudad

Calcula cuántos días calurosos (definidos como >30 grados) hubo en cada año en cada ciudad.


```python
%%writefile mapper_ej3.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or "Region" in line: continue
    
    parts = line.split(",")
    if len(parts) < 8: continue
        
    city = parts[3]
    year = parts[6]
    temp_str = parts[7]
    
    try:
        temp_f = float(temp_str)
        if temp_f == -99.0: continue
        
        # Convertir a Celsius
        temp_c = (temp_f - 32) / 1.8
        
        # Filtro de día caluroso (> 30 C)
        if temp_c > 30:
            # Clave compuesta para agrupar por ciudad Y año
            print(f"{city},{year}\t1")
            
    except ValueError:
        continue
```

    Writing mapper_ej3.py



```python
%%writefile reducer_ej3.py
#!/usr/bin/env python3
import sys

current_key = None
count = 0

for line in sys.stdin:
    try:
        key, val = line.strip().split("\t")
        val = int(val)
    except ValueError:
        continue

    if key == current_key:
        count += val
    else:
        if current_key:
            print(f"{current_key}\t{count}")
        current_key = key
        count = val

if current_key:
    print(f"{current_key}\t{count}")
```

    Writing reducer_ej3.py



```python
!cat city_temperature.csv | python3 mapper_ej3.py | sort | python3 reducer_ej3.py
```

    Abidjan,1995	3
    Abidjan,1996	1
    Abidjan,1998	16
    Abidjan,1999	2
    Abidjan,2000	1
    Abidjan,2003	8
    Abidjan,2004	4
    Abidjan,2005	18
    Abidjan,2006	1
    Abidjan,2010	20
    Abidjan,2015	1
    Abidjan,2016	4
    Abidjan,2017	3
    Abidjan,2019	5
    Abidjan,2020	5
    Abilene,1995	9
    Abilene,1996	21
    Abilene,1997	6
    Abilene,1998	48
    Abilene,1999	27
    Abilene,2000	51
    Abilene,2001	40
    Abilene,2002	5
    Abilene,2003	14
    Abilene,2004	2
    Abilene,2005	4
    Abilene,2006	33
    Abilene,2008	14
    Abilene,2009	33
    Abilene,2010	23
    Abilene,2011	80
    Abilene,2012	40
    Abilene,2013	24
    Abilene,2014	25
    Abilene,2015	22
    Abilene,2016	31
    Abilene,2017	13
    Abilene,2018	30
    Abilene,2019	32
    Abilene,2020	1
    Abu Dhabi,1995	144
    Abu Dhabi,1996	156
    Abu Dhabi,1997	152
    Abu Dhabi,1998	173
    Abu Dhabi,1999	170
    Abu Dhabi,2000	177
    Abu Dhabi,2001	168
    Abu Dhabi,2002	169
    Abu Dhabi,2003	172
    Abu Dhabi,2004	160
    Abu Dhabi,2005	161
    Abu Dhabi,2006	163
    Abu Dhabi,2007	170
    Abu Dhabi,2008	161
    Abu Dhabi,2009	167
    Abu Dhabi,2010	175
    Abu Dhabi,2011	180
    Abu Dhabi,2012	170
    Abu Dhabi,2013	160
    Abu Dhabi,2014	180
    Abu Dhabi,2015	187
    Abu Dhabi,2016	170
    Abu Dhabi,2017	192
    Abu Dhabi,2018	189
    Abu Dhabi,2019	185
    Abu Dhabi,2020	24
    Akron Canton,2012	2
    Albany,2011	1
    Albany,2018	1
    Albuquerque,1995	4
    Albuquerque,1996	2
    Albuquerque,1999	1
    Albuquerque,2002	2
    Albuquerque,2003	8
    Albuquerque,2009	1
    Albuquerque,2010	3
    Albuquerque,2012	3
    Albuquerque,2013	3
    Albuquerque,2014	1
    Albuquerque,2015	1
    Albuquerque,2016	2
    Albuquerque,2017	5
    Albuquerque,2018	1
    Albuquerque,2019	1
    Algiers,1996	3
    Algiers,1997	1
    Algiers,1998	3
    Algiers,1999	2
    Algiers,2000	4
    Algiers,2001	1
    Algiers,2003	6
    Algiers,2004	4
    Algiers,2005	2
    Algiers,2006	1
    Algiers,2008	1
    Algiers,2009	7
    Algiers,2011	3
    Algiers,2012	1
    Algiers,2013	1
    Algiers,2014	1
    Algiers,2015	2
    Algiers,2016	3
    Algiers,2017	6
    Algiers,2019	6
    Allentown,1995	1
    Allentown,1999	3
    Allentown,2010	1
    Allentown,2011	3
    Allentown,2018	1
    Allentown,2019	1
    Almaty,1996	2
    Almaty,1997	4
    Almaty,2000	1
    Almaty,2001	1
    Almaty,2002	1
    Almaty,2005	2
    Almaty,2006	1
    Almaty,2007	1
    Almaty,2008	1
    Almaty,2013	1
    Almaty,2014	3
    Almaty,2015	11
    Almaty,2017	5
    Almaty,2018	4
    Almaty,2019	4
    Amarillo,1996	4
    Amarillo,1998	9
    Amarillo,2000	3
    Amarillo,2001	12
    Amarillo,2002	1
    Amarillo,2003	5
    Amarillo,2008	1
    Amarillo,2009	4
    Amarillo,2011	36
    Amarillo,2012	16
    Amarillo,2013	4
    Amarillo,2016	5
    Amarillo,2017	1
    Amarillo,2018	7
    Amarillo,2019	5
    Amman,1995	4
    Amman,1996	3
    Amman,1997	1
    Amman,1998	6
    Amman,1999	3
    Amman,2000	15
    Amman,2001	5
    Amman,2002	7
    Amman,2003	1
    Amman,2004	4
    Amman,2005	3
    Amman,2006	3
    Amman,2007	10
    Amman,2008	5
    Amman,2009	3
    Amman,2010	14
    Amman,2011	6
    Amman,2012	15
    Amman,2014	4
    Amman,2015	21
    Amman,2016	12
    Amman,2017	18
    Amman,2018	2
    Amman,2019	9
    Ankara,2006	1
    Ankara,2010	1
    Ankara,2012	2
    Ashabad,1995	54
    Ashabad,1996	47
    Ashabad,1997	58
    Ashabad,1998	59
    Ashabad,1999	67
    Ashabad,2000	63
    Ashabad,2001	54
    Ashabad,2002	50
    Ashabad,2003	40
    Ashabad,2004	41
    Ashabad,2005	60
    Ashabad,2006	72
    Ashabad,2007	60
    Ashabad,2008	59
    Ashabad,2009	57
    Ashabad,2010	72
    Ashabad,2011	62
    Ashabad,2012	73
    Ashabad,2013	62
    Ashabad,2014	75
    Ashabad,2015	73
    Ashabad,2016	64
    Ashabad,2017	69
    Ashabad,2018	70
    Ashabad,2019	64
    Athens,1995	5
    Athens,1996	9
    Athens,1997	3
    Athens,1998	24
    Athens,1999	13
    Athens,2000	22
    Athens,2001	19
    Athens,2002	13
    Athens,2003	15
    Athens,2004	5
    Athens,2005	6
    Athens,2006	12
    Athens,2007	25
    Athens,2008	23
    Athens,2009	7
    Athens,2010	27
    Athens,2011	52
    Athens,2012	9
    Atlanta,1995	19
    Atlanta,1996	5
    Atlanta,1999	4
    Atlanta,2000	3
    Atlanta,2002	1
    Atlanta,2006	1
    Atlanta,2007	12
    Atlanta,2008	1
    Atlanta,2010	2
    Atlanta,2011	3
    Atlanta,2012	5
    Atlanta,2016	4
    Atlanta,2019	4
    Atlantic City,1995	1
    Atlantic City,1997	1
    Atlantic City,1999	2
    Atlantic City,2001	2
    Atlantic City,2002	3
    Atlantic City,2005	1
    Atlantic City,2006	5
    Atlantic City,2007	1
    Atlantic City,2008	2
    Atlantic City,2010	4
    Atlantic City,2011	4
    Atlantic City,2012	1
    Atlantic City,2013	1
    Atlantic City,2016	4
    Atlantic City,2017	1
    Atlantic City,2018	1
    Atlantic City,2019	3
    Austin,1995	12
    Austin,1996	28
    Austin,1998	54
    Austin,1999	16
    Austin,2000	29
    Austin,2001	18
    Austin,2002	1
    Austin,2003	5
    Austin,2004	1
    Austin,2005	24
    Austin,2006	29
    Austin,2007	1
    Austin,2008	13
    Austin,2009	61
    Austin,2010	18
    Austin,2011	65
    Austin,2012	20
    Austin,2013	35
    Austin,2014	16
    Austin,2015	13
    Austin,2016	21
    Austin,2017	37
    Austin,2018	43
    Austin,2019	30
    Baltimore,1995	5
    Baltimore,1997	2
    Baltimore,1999	3
    Baltimore,2001	1
    Baltimore,2002	4
    Baltimore,2005	1
    Baltimore,2006	5
    Baltimore,2007	1
    Baltimore,2010	5
    Baltimore,2011	7
    Baltimore,2012	9
    Baltimore,2013	1
    Baltimore,2014	1
    Baltimore,2016	4
    Baltimore,2017	2
    Baltimore,2018	1
    Baltimore,2019	2
    Bangkok,1996	136
    Bangkok,1997	198
    Bangkok,1998	86
    Bangkok,1999	24
    Bangkok,2000	34
    Bangkok,2001	47
    Bangkok,2002	109
    Bangkok,2003	114
    Bangkok,2004	135
    Bangkok,2005	159
    Bangkok,2006	161
    Bangkok,2007	93
    Bangkok,2008	59
    Bangkok,2009	67
    Bangkok,2010	100
    Bangkok,2011	37
    Bangui,1995	6
    Bangui,1996	2
    Bangui,1997	7
    Bangui,1998	23
    Bangui,1999	7
    Bangui,2000	7
    Bangui,2001	1
    Bangui,2002	4
    Bangui,2003	3
    Bangui,2004	7
    Bangui,2005	10
    Bangui,2006	3
    Bangui,2007	17
    Bangui,2008	7
    Bangui,2009	2
    Bangui,2010	14
    Bangui,2011	9
    Bangui,2012	5
    Bangui,2013	2
    Bangui,2014	2
    Bangui,2015	3
    Bangui,2016	19
    Bangui,2017	1
    Bangui,2018	3
    Bangui,2019	6
    Bangui,2020	9
    Banjul,1995	1
    Banjul,1996	3
    Banjul,1997	5
    Banjul,1998	8
    Banjul,1999	3
    Banjul,2000	8
    Banjul,2001	5
    Banjul,2002	1
    Banjul,2003	2
    Banjul,2004	3
    Banjul,2005	9
    Banjul,2006	5
    Banjul,2007	5
    Banjul,2010	3
    Banjul,2012	1
    Banjul,2013	1
    Banjul,2014	1
    Banjul,2017	5
    Banjul,2019	1
    Banjul,2020	2
    Barcelona,2018	2
    Baton Rouge,1995	4
    Baton Rouge,1996	1
    Baton Rouge,1998	9
    Baton Rouge,1999	5
    Baton Rouge,2000	11
    Baton Rouge,2004	2
    Baton Rouge,2006	1
    Baton Rouge,2007	7
    Baton Rouge,2008	2
    Baton Rouge,2009	13
    Baton Rouge,2010	10
    Beijing,1995	1
    Beijing,1997	6
    Beijing,1998	1
    Beijing,1999	11
    Beijing,2000	15
    Beijing,2001	3
    Beijing,2002	6
    Beijing,2003	3
    Beijing,2004	2
    Beijing,2005	6
    Beijing,2006	1
    Beijing,2007	3
    Beijing,2009	3
    Beijing,2010	10
    Beijing,2011	2
    Beijing,2012	2
    Beijing,2013	5
    Beijing,2014	8
    Beijing,2015	2
    Beijing,2016	8
    Beijing,2017	7
    Beijing,2018	15
    Beijing,2019	10
    Beirut,1995	1
    Beirut,1998	4
    Beirut,1999	1
    Beirut,2000	4
    Beirut,2002	6
    Beirut,2003	2
    Beirut,2007	2
    Beirut,2009	2
    Beirut,2010	6
    Beirut,2011	1
    Beirut,2012	6
    Beirut,2014	2
    Beirut,2015	10
    Beirut,2016	1
    Beirut,2018	3
    Beirut,2019	2
    Belgrade,1998	3
    Belgrade,2000	4
    Belgrade,2002	1
    Belgrade,2003	1
    Belgrade,2007	7
    Belgrade,2008	2
    Belgrade,2011	2
    Belgrade,2012	7
    Belgrade,2013	3
    Belgrade,2015	1
    Belgrade,2017	8
    Belize City,1995	3
    Belize City,1996	6
    Belize City,1997	28
    Belize City,1998	55
    Belize City,1999	4
    Belize City,2000	4
    Belize City,2001	5
    Belize City,2002	19
    Belize City,2003	44
    Belize City,2004	26
    Belize City,2005	52
    Belize City,2006	34
    Belize City,2007	49
    Belize City,2008	32
    Belize City,2009	55
    Belize City,2010	61
    Belize City,2011	35
    Belize City,2012	12
    Belize City,2013	1
    Belize City,2014	8
    Belize City,2015	18
    Belize City,2016	24
    Belize City,2017	27
    Belize City,2018	6
    Belize City,2019	48
    Belize City,2020	4
    Bilbao,2003	3
    Bilbao,2005	2
    Bilbao,2006	1
    Bilbao,2016	1
    Billings,2000	1
    Billings,2002	3
    Billings,2003	6
    Billings,2006	1
    Billings,2007	3
    Billings,2012	1
    Billings,2015	1
    Billings,2017	1
    Birmingham,1995	9
    Birmingham,1998	1
    Birmingham,1999	8
    Birmingham,2000	7
    Birmingham,2005	1
    Birmingham,2006	7
    Birmingham,2007	14
    Birmingham,2008	1
    Birmingham,2009	1
    Birmingham,2010	16
    Birmingham,2011	10
    Birmingham,2012	8
    Birmingham,2015	4
    Birmingham,2016	4
    Birmingham,2019	4
    Bishkek,1998	3
    Bishkek,1999	1
    Bishkek,2000	8
    Bishkek,2001	1
    Bishkek,2002	6
    Bishkek,2003	1
    Bishkek,2005	5
    Bishkek,2006	2
    Bishkek,2007	4
    Bishkek,2008	8
    Bishkek,2010	1
    Bishkek,2011	3
    Bishkek,2012	1
    Bishkek,2013	3
    Bishkek,2014	5
    Bishkek,2015	9
    Bishkek,2016	2
    Bishkek,2017	5
    Bishkek,2018	5
    Bishkek,2019	15
    Bismarck,2000	1
    Bismarck,2002	2
    Bismarck,2003	1
    Bismarck,2006	1
    Bismarck,2007	3
    Bissau,1995	41
    Bissau,1996	37
    Bissau,1997	30
    Bissau,1998	9
    Bissau,2006	14
    Bissau,2007	80
    Bissau,2008	53
    Bissau,2009	54
    Bissau,2010	40
    Bissau,2011	17
    Bissau,2012	25
    Bissau,2013	34
    Bissau,2014	17
    Bissau,2015	17
    Bissau,2016	18
    Bissau,2017	14
    Bissau,2018	6
    Bissau,2019	20
    Bissau,2020	45
    Boise,1996	2
    Boise,1998	1
    Boise,2000	2
    Boise,2001	2
    Boise,2002	5
    Boise,2003	7
    Boise,2004	3
    Boise,2005	7
    Boise,2006	5
    Boise,2007	8
    Boise,2008	3
    Boise,2009	3
    Boise,2011	1
    Boise,2012	8
    Boise,2013	6
    Boise,2014	7
    Boise,2015	16
    Boise,2016	1
    Boise,2017	4
    Boise,2018	5
    Boise,2019	1
    Bombay (Mumbai),1995	65
    Bombay (Mumbai),1996	28
    Bombay (Mumbai),1997	46
    Bombay (Mumbai),1998	54
    Bombay (Mumbai),1999	22
    Bombay (Mumbai),2000	25
    Bombay (Mumbai),2001	16
    Bombay (Mumbai),2002	44
    Bombay (Mumbai),2003	37
    Bombay (Mumbai),2004	24
    Bombay (Mumbai),2005	33
    Bombay (Mumbai),2006	12
    Bombay (Mumbai),2007	46
    Bombay (Mumbai),2008	49
    Bombay (Mumbai),2009	72
    Bombay (Mumbai),2010	71
    Bombay (Mumbai),2011	37
    Bombay (Mumbai),2012	26
    Bombay (Mumbai),2013	37
    Bombay (Mumbai),2014	93
    Bombay (Mumbai),2015	111
    Bombay (Mumbai),2016	68
    Bombay (Mumbai),2017	81
    Bombay (Mumbai),2018	107
    Bombay (Mumbai),2019	54
    Bombay (Mumbai),2020	39
    Bonn,1995	1
    Bordeaux,2003	4
    Bordeaux,2006	2
    Bordeaux,2019	1
    Boston,1995	1
    Boston,1999	3
    Boston,2001	1
    Boston,2002	3
    Boston,2006	1
    Boston,2007	1
    Boston,2011	1
    Boston,2012	2
    Boston,2013	2
    Boston,2018	2
    Boston,2019	2
    Brasilia,2002	1
    Brazzaville,1996	1
    Brazzaville,1998	2
    Brazzaville,1999	4
    Brazzaville,2000	1
    Brazzaville,2003	1
    Brazzaville,2008	1
    Brazzaville,2010	1
    Brazzaville,2016	1
    Brazzaville,2020	4
    Bridgeport,1995	1
    Bridgeport,2006	1
    Bridgeport,2011	1
    Bridgeport,2013	1
    Bridgetown,1995	2
    Bridgetown,2003	1
    Bridgetown,2004	1
    Bridgetown,2005	4
    Brisbane,2004	1
    Brownsville,1995	4
    Brownsville,1996	10
    Brownsville,1997	5
    Brownsville,1998	35
    Brownsville,1999	2
    Brownsville,2000	4
    Brownsville,2001	31
    Brownsville,2002	15
    Brownsville,2003	6
    Brownsville,2004	27
    Brownsville,2005	25
    Brownsville,2006	12
    Brownsville,2007	4
    Brownsville,2009	17
    Brownsville,2010	21
    Brownsville,2011	30
    Brownsville,2012	27
    Brownsville,2013	10
    Brownsville,2014	5
    Brownsville,2015	8
    Brownsville,2016	37
    Brownsville,2017	16
    Brownsville,2018	60
    Brownsville,2019	61
    Bucharest,2000	1
    Bucharest,2002	2
    Bucharest,2007	4
    Bucharest,2012	2
    Budapest,2007	2
    Budapest,2013	1
    Buenos Aires,1995	1
    Buenos Aires,2000	1
    Buenos Aires,2001	1
    Buenos Aires,2002	1
    Buenos Aires,2003	2
    Buenos Aires,2004	1
    Buenos Aires,2006	1
    Buenos Aires,2007	1
    Buenos Aires,2008	1
    Buenos Aires,2009	1
    Buenos Aires,2012	4
    Buenos Aires,2013	2
    Buenos Aires,2014	3
    Buenos Aires,2016	2
    Buenos Aires,2018	2
    Buenos Aires,2019	2
    Bujumbura,1995	3
    Bujumbura,1997	1
    Bujumbura,2005	2
    Burlington,1995	1
    Burlington,2011	1
    Burlington,2018	2
    Cairo,1995	18
    Cairo,1996	10
    Cairo,1997	11
    Cairo,1998	41
    Cairo,1999	13
    Cairo,2000	15
    Cairo,2001	21
    Cairo,2002	29
    Cairo,2003	22
    Cairo,2004	20
    Cairo,2005	20
    Cairo,2006	21
    Cairo,2007	38
    Cairo,2008	50
    Cairo,2009	43
    Cairo,2010	59
    Cairo,2011	21
    Cairo,2012	33
    Cairo,2013	14
    Cairo,2014	32
    Cairo,2015	41
    Cairo,2016	49
    Cairo,2017	60
    Cairo,2018	64
    Cairo,2019	55
    Calcutta,1995	77
    Calcutta,1996	68
    Calcutta,1997	46
    Calcutta,1998	81
    Calcutta,1999	64
    Calcutta,2000	71
    Calcutta,2001	44
    Calcutta,2002	72
    Calcutta,2003	64
    Calcutta,2004	96
    Calcutta,2005	61
    Calcutta,2006	78
    Calcutta,2007	87
    Calcutta,2008	51
    Calcutta,2009	79
    Calcutta,2010	105
    Calcutta,2011	56
    Calcutta,2012	99
    Calcutta,2013	77
    Calcutta,2014	106
    Calcutta,2015	90
    Calcutta,2016	106
    Calcutta,2017	85
    Calcutta,2018	73
    Calcutta,2019	83
    Calcutta,2020	19
    Canberra,1999	2
    Canberra,2007	1
    Canberra,2009	2
    Canberra,2010	2
    Canberra,2016	1
    Canberra,2017	1
    Canberra,2019	4
    Canberra,2020	3
    Caracas,1996	2
    Caracas,1998	2
    Caracas,2000	4
    Caracas,2001	20
    Caracas,2002	17
    Caracas,2003	2
    Caracas,2004	4
    Caracas,2005	24
    Caracas,2006	1
    Caracas,2007	4
    Caracas,2008	12
    Caracas,2009	43
    Caracas,2010	7
    Caracas,2011	5
    Caracas,2012	10
    Caracas,2013	1
    Caracas,2015	5
    Caracas,2016	2
    Caracas,2017	10
    Caracas,2019	1
    Caracas,2020	1
    Casper,2006	1
    Charleston,1995	3
    Charleston,1996	3
    Charleston,1998	7
    Charleston,1999	8
    Charleston,2000	1
    Charleston,2002	3
    Charleston,2004	2
    Charleston,2005	3
    Charleston,2007	7
    Charleston,2008	1
    Charleston,2010	2
    Charleston,2011	11
    Charleston,2012	3
    Charleston,2013	2
    Charleston,2014	5
    Charleston,2015	6
    Charleston,2016	11
    Charleston,2017	1
    Charleston,2018	1
    Charleston,2019	3
    Charlotte,1995	1
    Charlotte,1998	5
    Charlotte,1999	1
    Charlotte,2002	2
    Charlotte,2005	2
    Charlotte,2007	6
    Charlotte,2010	3
    Charlotte,2011	6
    Charlotte,2012	4
    Charlotte,2015	4
    Charlotte,2016	4
    Chattanooga,1996	2
    Chattanooga,1999	3
    Chattanooga,2000	1
    Chattanooga,2002	1
    Chattanooga,2006	1
    Chattanooga,2007	13
    Chattanooga,2009	1
    Chattanooga,2010	9
    Chattanooga,2011	3
    Chattanooga,2012	7
    Chattanooga,2016	4
    Chattanooga,2019	1
    Chengdu,1995	2
    Chengdu,1997	1
    Chengdu,1998	2
    Chengdu,1999	1
    Chengdu,2000	2
    Chengdu,2001	4
    Chengdu,2002	3
    Chengdu,2006	14
    Chengdu,2007	1
    Chengdu,2009	2
    Chengdu,2010	4
    Chengdu,2011	3
    Chengdu,2012	6
    Chengdu,2013	5
    Chengdu,2014	1
    Chengdu,2015	2
    Chengdu,2016	12
    Chengdu,2017	9
    Chengdu,2018	8
    Chengdu,2019	7
    Chengdu,2020	1
    Chennai (Madras),1995	92
    Chennai (Madras),1996	105
    Chennai (Madras),1997	119
    Chennai (Madras),1998	115
    Chennai (Madras),1999	122
    Chennai (Madras),2000	83
    Chennai (Madras),2001	110
    Chennai (Madras),2002	114
    Chennai (Madras),2003	116
    Chennai (Madras),2004	104
    Chennai (Madras),2005	106
    Chennai (Madras),2006	111
    Chennai (Madras),2007	65
    Chennai (Madras),2008	93
    Chennai (Madras),2009	154
    Chennai (Madras),2010	97
    Chennai (Madras),2011	100
    Chennai (Madras),2012	128
    Chennai (Madras),2013	102
    Chennai (Madras),2014	117
    Chennai (Madras),2015	145
    Chennai (Madras),2016	144
    Chennai (Madras),2017	158
    Chennai (Madras),2018	169
    Chennai (Madras),2019	169
    Chennai (Madras),2020	33
    Chicago,1995	5
    Chicago,1998	1
    Chicago,1999	2
    Chicago,2002	1
    Chicago,2005	1
    Chicago,2006	3
    Chicago,2011	3
    Chicago,2012	9
    Chicago,2013	2
    Chicago,2018	2
    Cincinnati,1999	2
    Cincinnati,2007	4
    Cincinnati,2010	1
    Cincinnati,2011	2
    Cincinnati,2012	5
    Cleveland,1995	1
    Cleveland,2011	1
    Cleveland,2012	1
    Cleveland,2019	1
    Colombo,1995	12
    Colombo,1996	13
    Colombo,1997	7
    Colombo,1998	32
    Colombo,1999	2
    Colombo,2000	4
    Colombo,2001	4
    Colombo,2002	5
    Colombo,2003	3
    Colombo,2004	6
    Colombo,2005	1
    Colombo,2006	5
    Colombo,2007	1
    Colombo,2009	4
    Colombo,2010	3
    Colombo,2012	2
    Colombo,2013	3
    Colombo,2016	8
    Colombo,2017	7
    Colombo,2019	1
    Colombo,2020	5
    Colorado Springs,2002	1
    Columbia,1995	6
    Columbia,1996	5
    Columbia,1997	2
    Columbia,1998	14
    Columbia,1999	13
    Columbia,2000	2
    Columbia,2001	2
    Columbia,2002	13
    Columbia,2004	1
    Columbia,2005	3
    Columbia,2006	6
    Columbia,2007	12
    Columbia,2008	3
    Columbia,2009	2
    Columbia,2010	15
    Columbia,2011	17
    Columbia,2012	11
    Columbia,2013	1
    Columbia,2014	8
    Columbia,2015	19
    Columbia,2016	24
    Columbia,2017	7
    Columbia,2018	3
    Columbia,2019	7
    Columbus,1995	9
    Columbus,1996	4
    Columbus,1997	3
    Columbus,1998	18
    Columbus,1999	20
    Columbus,2000	14
    Columbus,2001	2
    Columbus,2002	8
    Columbus,2004	1
    Columbus,2005	4
    Columbus,2006	11
    Columbus,2007	10
    Columbus,2008	3
    Columbus,2009	3
    Columbus,2010	19
    Columbus,2011	19
    Columbus,2012	11
    Columbus,2013	1
    Columbus,2014	1
    Columbus,2015	6
    Columbus,2016	4
    Columbus,2017	1
    Columbus,2018	2
    Columbus,2019	8
    Conakry,1995	7
    Conakry,1996	2
    Conakry,1997	2
    Conakry,1998	1
    Conakry,2000	4
    Conakry,2001	11
    Conakry,2002	6
    Conakry,2003	2
    Conakry,2004	4
    Conakry,2005	9
    Conakry,2006	1
    Conakry,2007	18
    Conakry,2008	16
    Conakry,2009	7
    Conakry,2010	39
    Conakry,2011	32
    Conakry,2012	3
    Conakry,2013	5
    Conakry,2015	1
    Conakry,2016	12
    Conakry,2019	2
    Conakry,2020	20
    Concord,2011	1
    Concord,2019	1
    Corpus Christi,1995	4
    Corpus Christi,1996	9
    Corpus Christi,1997	8
    Corpus Christi,1998	31
    Corpus Christi,1999	3
    Corpus Christi,2000	10
    Corpus Christi,2001	8
    Corpus Christi,2002	5
    Corpus Christi,2003	2
    Corpus Christi,2004	8
    Corpus Christi,2005	19
    Corpus Christi,2006	5
    Corpus Christi,2007	1
    Corpus Christi,2008	2
    Corpus Christi,2009	51
    Corpus Christi,2010	5
    Corpus Christi,2011	50
    Corpus Christi,2012	48
    Corpus Christi,2013	52
    Corpus Christi,2014	11
    Corpus Christi,2015	16
    Corpus Christi,2016	21
    Corpus Christi,2017	10
    Corpus Christi,2019	28
    Cotonou,1995	16
    Cotonou,1996	12
    Cotonou,1998	50
    Cotonou,1999	5
    Cotonou,2000	17
    Cotonou,2001	5
    Cotonou,2002	4
    Cotonou,2003	9
    Cotonou,2004	1
    Cotonou,2005	16
    Cotonou,2006	19
    Cotonou,2007	1
    Cotonou,2008	8
    Cotonou,2009	2
    Cotonou,2010	54
    Cotonou,2011	5
    Cotonou,2012	5
    Cotonou,2013	1
    Cotonou,2014	3
    Cotonou,2015	15
    Cotonou,2016	23
    Cotonou,2017	23
    Cotonou,2018	11
    Cotonou,2019	33
    Cotonou,2020	23
    Dakar,2007	1
    Dakar,2011	1
    Dakar,2015	1
    Dakar,2017	2
    Dallas Ft Worth,1995	34
    Dallas Ft Worth,1996	29
    Dallas Ft Worth,1997	23
    Dallas Ft Worth,1998	84
    Dallas Ft Worth,1999	45
    Dallas Ft Worth,2000	57
    Dallas Ft Worth,2001	39
    Dallas Ft Worth,2002	22
    Dallas Ft Worth,2003	31
    Dallas Ft Worth,2004	14
    Dallas Ft Worth,2005	43
    Dallas Ft Worth,2006	54
    Dallas Ft Worth,2007	26
    Dallas Ft Worth,2008	69
    Dallas Ft Worth,2009	42
    Dallas Ft Worth,2010	61
    Dallas Ft Worth,2011	84
    Dallas Ft Worth,2012	50
    Dallas Ft Worth,2013	49
    Dallas Ft Worth,2014	37
    Dallas Ft Worth,2015	50
    Dallas Ft Worth,2016	53
    Dallas Ft Worth,2017	38
    Dallas Ft Worth,2018	55
    Dallas Ft Worth,2019	39
    Damascus,1996	4
    Damascus,1997	2
    Damascus,1998	13
    Damascus,1999	3
    Damascus,2000	25
    Damascus,2001	9
    Damascus,2002	10
    Damascus,2003	1
    Damascus,2004	4
    Damascus,2005	6
    Damascus,2006	4
    Damascus,2007	11
    Damascus,2008	9
    Damascus,2009	3
    Damascus,2010	21
    Damascus,2011	6
    Damascus,2012	13
    Damascus,2013	2
    Damascus,2014	7
    Damascus,2015	17
    Damascus,2016	26
    Damascus,2017	20
    Damascus,2018	4
    Damascus,2019	5
    Dar Es Salaam,1995	4
    Dar Es Salaam,1996	1
    Dar Es Salaam,1997	3
    Dar Es Salaam,1998	2
    Dar Es Salaam,2002	1
    Dar Es Salaam,2003	4
    Dar Es Salaam,2005	1
    Dar Es Salaam,2006	5
    Dar Es Salaam,2010	2
    Dar Es Salaam,2011	1
    Dar Es Salaam,2014	4
    Dar Es Salaam,2015	6
    Dar Es Salaam,2016	14
    Dar Es Salaam,2017	2
    Dar Es Salaam,2019	6
    Dayton,1999	2
    Dayton,2011	2
    Dayton,2012	4
    Daytona Beach,1996	1
    Daytona Beach,1998	7
    Daytona Beach,1999	2
    Daytona Beach,2007	1
    Daytona Beach,2009	2
    Delhi,1995	105
    Delhi,1996	86
    Delhi,1997	83
    Delhi,1998	108
    Delhi,1999	113
    Delhi,2000	109
    Delhi,2001	103
    Delhi,2002	119
    Delhi,2003	102
    Delhi,2004	120
    Delhi,2005	110
    Delhi,2006	119
    Delhi,2007	122
    Delhi,2008	99
    Delhi,2009	132
    Delhi,2010	118
    Delhi,2011	94
    Delhi,2012	102
    Delhi,2013	111
    Delhi,2014	137
    Delhi,2015	122
    Delhi,2016	158
    Delhi,2017	151
    Delhi,2018	117
    Delhi,2019	137
    Delhi,2020	14
    Denver,2008	1
    Denver,2012	2
    Des Moines,1995	3
    Des Moines,1997	1
    Des Moines,1998	1
    Des Moines,1999	3
    Des Moines,2001	3
    Des Moines,2002	1
    Des Moines,2005	2
    Des Moines,2006	3
    Des Moines,2008	1
    Des Moines,2009	1
    Des Moines,2010	1
    Des Moines,2011	6
    Des Moines,2012	15
    Des Moines,2013	4
    Des Moines,2015	1
    Des Moines,2016	1
    Des Moines,2017	3
    Des Moines,2019	1
    Detroit,2001	1
    Detroit,2002	1
    Detroit,2006	2
    Detroit,2011	1
    Detroit,2012	2
    Detroit,2013	1
    Detroit,2018	1
    Dhahran,1995	140
    Dhahran,1996	155
    Dhahran,1997	161
    Dhahran,1998	159
    Dhahran,1999	170
    Dhahran,2000	165
    Dhahran,2001	158
    Dhahran,2002	161
    Dhahran,2003	155
    Dhahran,2004	149
    Dhahran,2005	145
    Dhahran,2006	186
    Dhahran,2007	178
    Dhahran,2008	172
    Dhahran,2009	169
    Dhahran,2010	163
    Dhahran,2011	155
    Dhahran,2012	164
    Dhahran,2013	149
    Dhahran,2014	178
    Dhahran,2015	183
    Dhahran,2016	154
    Dhahran,2017	182
    Dhahran,2018	170
    Dhahran,2019	178
    Dhahran,2020	11
    Dhaka,1995	50
    Dhaka,1996	33
    Dhaka,1997	8
    Dhaka,1998	23
    Dhaka,1999	3
    Dhaka,2000	24
    Dhaka,2001	28
    Dhaka,2002	12
    Dhaka,2003	27
    Dhaka,2004	22
    Dhaka,2005	19
    Dhaka,2006	35
    Dhaka,2007	23
    Dhaka,2008	8
    Dhaka,2009	39
    Dhaka,2010	58
    Doha,1995	149
    Doha,1996	162
    Doha,1997	160
    Doha,1998	169
    Doha,1999	180
    Doha,2000	175
    Doha,2001	177
    Doha,2002	176
    Doha,2003	173
    Doha,2004	174
    Doha,2005	162
    Doha,2006	188
    Doha,2007	182
    Doha,2008	169
    Doha,2009	167
    Doha,2010	175
    Doha,2011	172
    Doha,2012	186
    Doha,2013	162
    Doha,2014	192
    Doha,2015	191
    Doha,2016	173
    Doha,2017	195
    Doha,2018	179
    Doha,2019	180
    Doha,2020	14
    Dubai,1995	152
    Dubai,1996	162
    Dubai,1997	152
    Dubai,1998	172
    Dubai,1999	164
    Dubai,2000	167
    Dubai,2001	168
    Dubai,2002	172
    Dubai,2003	176
    Dubai,2004	170
    Dubai,2005	171
    Dubai,2006	177
    Dubai,2007	182
    Dubai,2008	182
    Dubai,2009	176
    Dubai,2010	185
    Dubai,2011	185
    Dubai,2012	185
    Dubai,2013	175
    Dubai,2014	191
    Dubai,2015	190
    Dubai,2016	180
    Dubai,2017	203
    Dubai,2018	195
    Dubai,2019	188
    Dubai,2020	24
    Dusanbe,1997	21
    Dusanbe,1998	17
    Dusanbe,1999	25
    Dusanbe,2000	4
    Dusanbe,2001	10
    Dusanbe,2002	4
    Dusanbe,2003	7
    Dusanbe,2004	2
    Dusanbe,2005	5
    Dusanbe,2006	11
    Dusanbe,2007	6
    Dusanbe,2008	18
    Dusanbe,2009	4
    Dusanbe,2010	3
    Dusanbe,2011	16
    Dusanbe,2012	2
    Dusanbe,2013	18
    Dusanbe,2014	6
    Dusanbe,2015	20
    Dusanbe,2016	15
    Dusanbe,2017	22
    Dusanbe,2018	22
    Dusanbe,2019	29
    El Paso,1995	15
    El Paso,1996	29
    El Paso,1997	16
    El Paso,1998	16
    El Paso,1999	7
    El Paso,2000	19
    El Paso,2001	19
    El Paso,2002	29
    El Paso,2003	33
    El Paso,2004	18
    El Paso,2005	36
    El Paso,2006	30
    El Paso,2007	18
    El Paso,2008	22
    El Paso,2009	34
    El Paso,2010	37
    El Paso,2011	66
    El Paso,2012	41
    El Paso,2013	39
    El Paso,2014	37
    El Paso,2015	37
    El Paso,2016	42
    El Paso,2017	32
    El Paso,2018	60
    El Paso,2019	57
    Elkins,1995	1
    Elkins,2012	2
    Erie,2011	1
    Evansville,1995	7
    Evansville,1996	2
    Evansville,1997	1
    Evansville,1999	2
    Evansville,2001	1
    Evansville,2005	1
    Evansville,2007	7
    Evansville,2008	1
    Evansville,2009	1
    Evansville,2010	4
    Evansville,2011	5
    Evansville,2012	11
    Evansville,2015	1
    Evansville,2016	1
    Evansville,2017	2
    Evansville,2018	3
    Fargo,1995	1
    Fargo,2000	1
    Fargo,2002	1
    Fargo,2011	1
    Flint,2011	1
    Flint,2012	1
    Fort Smith,1995	3
    Fort Smith,1996	1
    Fort Smith,1997	5
    Fort Smith,1998	33
    Fort Smith,1999	15
    Fort Smith,2000	32
    Fort Smith,2001	24
    Fort Smith,2002	1
    Fort Smith,2003	18
    Fort Smith,2005	12
    Fort Smith,2006	22
    Fort Smith,2007	11
    Fort Smith,2008	15
    Fort Smith,2009	14
    Fort Smith,2010	35
    Fort Smith,2011	56
    Fort Smith,2012	41
    Fort Smith,2013	10
    Fort Smith,2014	2
    Fort Smith,2015	18
    Fort Smith,2016	20
    Fort Smith,2017	6
    Fort Smith,2018	14
    Fort Smith,2019	6
    Fort Wayne,1995	1
    Fort Wayne,1999	1
    Fort Wayne,2011	1
    Fort Wayne,2012	3
    Freetown,1995	12
    Freetown,1996	3
    Freetown,1997	1
    Freetown,2002	1
    Freetown,2003	2
    Freetown,2004	7
    Freetown,2005	7
    Freetown,2006	6
    Freetown,2007	10
    Freetown,2008	3
    Freetown,2009	1
    Freetown,2010	20
    Freetown,2011	1
    Fresno,1995	20
    Fresno,1996	32
    Fresno,1997	11
    Fresno,1998	27
    Fresno,1999	11
    Fresno,2000	17
    Fresno,2001	21
    Fresno,2002	13
    Fresno,2003	31
    Fresno,2004	11
    Fresno,2005	31
    Fresno,2006	24
    Fresno,2007	17
    Fresno,2008	20
    Fresno,2009	20
    Fresno,2010	10
    Fresno,2011	16
    Fresno,2012	29
    Fresno,2013	32
    Fresno,2014	39
    Fresno,2015	33
    Fresno,2016	29
    Fresno,2017	45
    Fresno,2018	44
    Fresno,2019	37
    Georgetown,1996	6
    Georgetown,1999	31
    Georgetown,2000	9
    Georgetown,2001	41
    Georgetown,2002	16
    Georgetown,2003	8
    Georgetown,2004	31
    Georgetown,2005	57
    Georgetown,2006	13
    Georgetown,2010	5
    Georgetown,2011	4
    Goodland,1995	1
    Goodland,1998	1
    Goodland,2002	6
    Goodland,2003	3
    Goodland,2005	4
    Goodland,2006	2
    Goodland,2008	2
    Goodland,2009	1
    Goodland,2011	1
    Goodland,2012	5
    Goodland,2013	1
    Goodland,2016	2
    Goodland,2019	1
    Grand Junction,1995	2
    Grand Junction,1996	1
    Grand Junction,1998	2
    Grand Junction,1999	2
    Grand Junction,2000	3
    Grand Junction,2001	4
    Grand Junction,2002	10
    Grand Junction,2003	13
    Grand Junction,2004	3
    Grand Junction,2005	7
    Grand Junction,2006	6
    Grand Junction,2007	2
    Grand Junction,2008	2
    Grand Junction,2010	3
    Grand Junction,2011	1
    Grand Junction,2012	4
    Grand Junction,2013	1
    Grand Junction,2014	1
    Grand Junction,2015	1
    Grand Junction,2016	2
    Grand Junction,2017	5
    Grand Junction,2018	4
    Grand Junction,2019	2
    Grand Rapids,1995	1
    Grand Rapids,2006	1
    Grand Rapids,2011	1
    Grand Rapids,2012	5
    Grand Rapids,2013	1
    Great Falls,2002	1
    Great Falls,2005	1
    Great Falls,2007	3
    Green Bay,1995	1
    Green Bay,2018	1
    Greensboro,1995	1
    Greensboro,1996	2
    Greensboro,1999	1
    Greensboro,2005	2
    Greensboro,2006	1
    Greensboro,2007	5
    Greensboro,2008	2
    Greensboro,2010	3
    Greensboro,2011	3
    Greensboro,2012	3
    Greensboro,2016	1
    Guadalajara,2016	1
    Guangzhou,1995	31
    Guangzhou,1996	24
    Guangzhou,1997	13
    Guangzhou,1998	41
    Guangzhou,1999	37
    Guangzhou,2000	30
    Guangzhou,2001	21
    Guangzhou,2002	17
    Guangzhou,2003	34
    Guangzhou,2004	23
    Guangzhou,2005	35
    Guangzhou,2006	41
    Guangzhou,2007	48
    Guangzhou,2008	48
    Guangzhou,2009	59
    Guangzhou,2010	46
    Guangzhou,2011	56
    Guangzhou,2012	44
    Guangzhou,2013	38
    Guangzhou,2014	68
    Guangzhou,2015	46
    Guangzhou,2016	42
    Guangzhou,2017	61
    Guangzhou,2018	46
    Guangzhou,2019	48
    Guangzhou,2020	6
    Guayaquil,1995	2
    Guayaquil,1996	2
    Guayaquil,1997	4
    Guayaquil,1998	3
    Guayaquil,1999	1
    Guayaquil,2005	1
    Guayaquil,2016	2
    Guayaquil,2020	1
    Hamburg,2006	1
    Hamburg,2010	2
    Hanoi,1995	27
    Hanoi,1996	23
    Hanoi,1997	34
    Hanoi,1998	55
    Hanoi,1999	29
    Hanoi,2000	9
    Hanoi,2001	17
    Hanoi,2002	20
    Hanoi,2003	40
    Hanoi,2004	16
    Hanoi,2005	35
    Hanoi,2006	28
    Hanoi,2007	40
    Hanoi,2008	26
    Hanoi,2009	54
    Hanoi,2010	39
    Hanoi,2011	27
    Hanoi,2012	42
    Hanoi,2013	35
    Hanoi,2014	43
    Hanoi,2015	65
    Hanoi,2016	57
    Hanoi,2017	27
    Hanoi,2018	41
    Hanoi,2019	63
    Hanoi,2020	1
    Harrisburg,1995	1
    Harrisburg,1997	4
    Harrisburg,1999	4
    Harrisburg,2001	1
    Harrisburg,2002	2
    Harrisburg,2006	2
    Harrisburg,2010	4
    Hartford Springfield,1995	1
    Hartford Springfield,1999	2
    Hartford Springfield,2001	1
    Hartford Springfield,2002	2
    Hartford Springfield,2006	2
    Hartford Springfield,2010	2
    Hartford Springfield,2011	1
    Hartford Springfield,2012	1
    Hartford Springfield,2013	1
    Hartford Springfield,2019	2
    Havana,1996	2
    Havana,1997	1
    Havana,1998	2
    Havana,1999	2
    Havana,2005	1
    Helena,2006	1
    Helena,2015	1
    Hong Kong,1995	24
    Hong Kong,1996	26
    Hong Kong,1997	18
    Hong Kong,1998	50
    Hong Kong,1999	39
    Hong Kong,2000	48
    Hong Kong,2001	30
    Hong Kong,2002	31
    Hong Kong,2003	38
    Hong Kong,2004	36
    Hong Kong,2005	34
    Hong Kong,2006	38
    Hong Kong,2007	55
    Hong Kong,2008	38
    Hong Kong,2009	69
    Hong Kong,2010	46
    Hong Kong,2011	64
    Hong Kong,2012	47
    Hong Kong,2013	44
    Hong Kong,2014	90
    Hong Kong,2015	73
    Hong Kong,2016	65
    Hong Kong,2017	84
    Hong Kong,2018	60
    Hong Kong,2019	59
    Hong Kong,2020	1
    Honolulu,2015	4
    Honolulu,2019	1
    Houston,1995	13
    Houston,1996	5
    Houston,1997	2
    Houston,1998	32
    Houston,1999	11
    Houston,2000	17
    Houston,2001	5
    Houston,2002	7
    Houston,2003	6
    Houston,2004	12
    Houston,2005	13
    Houston,2006	6
    Houston,2007	9
    Houston,2008	9
    Houston,2009	45
    Houston,2010	31
    Houston,2011	70
    Houston,2012	25
    Houston,2013	24
    Houston,2014	8
    Houston,2015	21
    Houston,2016	34
    Houston,2017	17
    Houston,2018	23
    Houston,2019	25
    Huntsville,1996	1
    Huntsville,1998	1
    Huntsville,2000	1
    Huntsville,2002	1
    Huntsville,2006	5
    Huntsville,2007	13
    Huntsville,2008	1
    Huntsville,2009	1
    Huntsville,2010	11
    Huntsville,2011	1
    Huntsville,2012	6
    Huntsville,2015	7
    Huntsville,2016	2
    Indianapolis,1999	1
    Indianapolis,2010	3
    Indianapolis,2011	6
    Indianapolis,2012	10
    Islamabad,1995	51
    Islamabad,1996	44
    Islamabad,1997	47
    Islamabad,1998	67
    Islamabad,1999	77
    Islamabad,2000	73
    Islamabad,2001	69
    Islamabad,2002	79
    Islamabad,2003	57
    Islamabad,2004	57
    Islamabad,2005	49
    Islamabad,2006	74
    Islamabad,2007	61
    Islamabad,2008	49
    Islamabad,2009	81
    Islamabad,2010	64
    Islamabad,2011	79
    Islamabad,2012	84
    Islamabad,2013	59
    Islamabad,2014	62
    Islamabad,2015	50
    Islamabad,2016	83
    Islamabad,2017	71
    Islamabad,2018	75
    Islamabad,2019	13
    Istanbul,2000	1
    Istanbul,2002	3
    Istanbul,2007	2
    Istanbul,2010	1
    Istanbul,2015	1
    Istanbul,2017	2
    Jackson,1998	3
    Jackson,1999	8
    Jackson,2000	16
    Jackson,2001	1
    Jackson,2005	3
    Jackson,2006	2
    Jackson,2007	10
    Jackson,2008	2
    Jackson,2009	5
    Jackson,2010	3
    Jackson,2011	15
    Jackson,2012	8
    Jackson,2013	3
    Jackson,2015	13
    Jackson,2016	4
    Jackson,2019	3
    Jacksonville,1996	1
    Jacksonville,1998	8
    Jacksonville,1999	5
    Jacksonville,2007	1
    Jacksonville,2009	1
    Jacksonville,2010	2
    Jacksonville,2016	4
    Jacksonville,2019	2
    Jakarta,1995	5
    Jakarta,1996	8
    Jakarta,1997	11
    Jakarta,1998	17
    Jakarta,1999	11
    Jakarta,2000	7
    Jakarta,2001	2
    Jakarta,2002	19
    Jakarta,2003	46
    Jakarta,2004	33
    Jakarta,2005	8
    Jakarta,2006	39
    Jakarta,2007	21
    Jakarta,2008	16
    Jakarta,2009	32
    Jakarta,2010	35
    Jakarta,2011	12
    Jakarta,2012	24
    Jakarta,2013	14
    Jakarta,2014	45
    Jakarta,2015	8
    Jakarta,2016	20
    Jakarta,2017	18
    Jakarta,2018	28
    Jakarta,2019	38
    Jakarta,2020	10
    Kansas City,1995	1
    Kansas City,1996	2
    Kansas City,1998	1
    Kansas City,1999	5
    Kansas City,2000	6
    Kansas City,2001	4
    Kansas City,2002	6
    Kansas City,2003	10
    Kansas City,2005	1
    Kansas City,2006	12
    Kansas City,2007	5
    Kansas City,2008	2
    Kansas City,2009	3
    Kansas City,2010	6
    Kansas City,2011	13
    Kansas City,2012	20
    Kansas City,2016	2
    Kansas City,2017	2
    Kansas City,2018	5
    Kansas City,2019	3
    Karachi,1995	84
    Karachi,1996	85
    Karachi,1997	95
    Karachi,1998	117
    Karachi,1999	93
    Karachi,2000	92
    Karachi,2001	92
    Karachi,2002	86
    Karachi,2003	114
    Karachi,2004	106
    Karachi,2005	83
    Karachi,2006	111
    Karachi,2007	120
    Karachi,2008	87
    Karachi,2009	101
    Karachi,2010	113
    Karachi,2011	77
    Karachi,2012	72
    Karachi,2013	98
    Karachi,2014	104
    Karachi,2015	123
    Karachi,2016	90
    Karachi,2017	91
    Karachi,2018	104
    Karachi,2019	121
    Karachi,2020	26
    Katmandu,1995	1
    Katmandu,2012	1
    Kiev,2000	1
    Kiev,2010	1
    Knoxville,2007	4
    Knoxville,2010	2
    Knoxville,2012	4
    Kuala Lumpur,1995	3
    Kuala Lumpur,1996	2
    Kuala Lumpur,1997	3
    Kuala Lumpur,1998	35
    Kuala Lumpur,2000	2
    Kuala Lumpur,2002	6
    Kuala Lumpur,2004	3
    Kuala Lumpur,2005	23
    Kuala Lumpur,2007	1
    Kuala Lumpur,2009	6
    Kuala Lumpur,2010	40
    Kuala Lumpur,2011	30
    Kuala Lumpur,2012	32
    Kuala Lumpur,2013	16
    Kuala Lumpur,2014	22
    Kuala Lumpur,2015	26
    Kuala Lumpur,2016	39
    Kuala Lumpur,2017	11
    Kuala Lumpur,2018	7
    Kuala Lumpur,2019	25
    Kuala Lumpur,2020	13
    Kuwait,1995	148
    Kuwait,1996	155
    Kuwait,1997	156
    Kuwait,1998	156
    Kuwait,1999	168
    Kuwait,2000	169
    Kuwait,2001	153
    Kuwait,2002	161
    Kuwait,2003	164
    Kuwait,2004	155
    Kuwait,2005	152
    Kuwait,2006	168
    Kuwait,2007	163
    Kuwait,2008	161
    Kuwait,2009	159
    Kuwait,2010	166
    Kuwait,2011	155
    Kuwait,2012	169
    Kuwait,2013	147
    Kuwait,2014	178
    Kuwait,2015	171
    Kuwait,2016	154
    Kuwait,2017	172
    Kuwait,2018	160
    Kuwait,2019	166
    Kuwait,2020	9
    Lagos,1998	1
    Lagos,1999	13
    Lagos,2000	9
    Lagos,2001	11
    Lagos,2002	8
    Lagos,2003	4
    Lagos,2004	11
    Lagos,2005	39
    Lagos,2006	57
    Lagos,2007	13
    Lagos,2009	1
    Lagos,2010	23
    Lagos,2012	2
    Lagos,2014	7
    Lagos,2015	7
    Lagos,2016	22
    Lagos,2017	7
    Lagos,2018	7
    Lagos,2019	18
    Lagos,2020	22
    Lake Charles,1995	18
    Lake Charles,1998	7
    Lake Charles,1999	5
    Lake Charles,2000	9
    Lake Charles,2003	1
    Lake Charles,2004	2
    Lake Charles,2005	4
    Lake Charles,2007	7
    Lake Charles,2009	10
    Lake Charles,2010	17
    Lake Charles,2011	21
    Lake Charles,2012	2
    Lake Charles,2013	6
    Lake Charles,2015	9
    Lake Charles,2016	5
    Lake Charles,2017	2
    Lake Charles,2018	14
    Lake Charles,2019	10
    Lansing,2011	1
    Lansing,2012	2
    Las Vegas,1995	81
    Las Vegas,1996	92
    Las Vegas,1997	84
    Las Vegas,1998	69
    Las Vegas,1999	73
    Las Vegas,2000	99
    Las Vegas,2001	106
    Las Vegas,2002	89
    Las Vegas,2003	95
    Las Vegas,2004	91
    Las Vegas,2005	89
    Las Vegas,2006	105
    Las Vegas,2007	106
    Las Vegas,2008	89
    Las Vegas,2009	97
    Las Vegas,2010	90
    Las Vegas,2011	90
    Las Vegas,2012	96
    Las Vegas,2013	90
    Las Vegas,2014	101
    Las Vegas,2015	102
    Las Vegas,2016	95
    Las Vegas,2017	99
    Las Vegas,2018	118
    Las Vegas,2019	94
    Las Vegas,2020	2
    Lexington,1999	2
    Lexington,2005	1
    Lexington,2007	2
    Lexington,2012	4
    Libreville,1999	1
    Libreville,2004	1
    Libreville,2020	1
    Lilongwe,2010	1
    Lilongwe,2011	4
    Lincoln,1995	6
    Lincoln,1996	1
    Lincoln,1997	2
    Lincoln,1998	3
    Lincoln,1999	5
    Lincoln,2000	1
    Lincoln,2001	8
    Lincoln,2002	6
    Lincoln,2003	3
    Lincoln,2004	1
    Lincoln,2005	7
    Lincoln,2006	8
    Lincoln,2008	1
    Lincoln,2009	2
    Lincoln,2010	1
    Lincoln,2011	9
    Lincoln,2012	12
    Lincoln,2014	2
    Lincoln,2015	1
    Lincoln,2016	6
    Lincoln,2017	2
    Lincoln,2018	4
    Lincoln,2019	4
    Lisbon,1995	4
    Lisbon,1998	2
    Lisbon,2003	9
    Lisbon,2004	2
    Lisbon,2005	2
    Lisbon,2006	6
    Lisbon,2007	2
    Lisbon,2010	7
    Lisbon,2012	1
    Lisbon,2013	3
    Lisbon,2016	2
    Lisbon,2017	2
    Lisbon,2018	4
    Little Rock,1995	18
    Little Rock,1996	4
    Little Rock,1997	8
    Little Rock,1998	33
    Little Rock,1999	16
    Little Rock,2000	28
    Little Rock,2001	7
    Little Rock,2002	1
    Little Rock,2003	3
    Little Rock,2004	1
    Little Rock,2005	14
    Little Rock,2006	22
    Little Rock,2007	21
    Little Rock,2008	9
    Little Rock,2009	6
    Little Rock,2010	32
    Little Rock,2011	29
    Little Rock,2012	31
    Little Rock,2013	6
    Little Rock,2015	18
    Little Rock,2016	26
    Little Rock,2017	3
    Little Rock,2018	5
    Lome,1995	8
    Lome,1996	4
    Lome,1997	1
    Lome,1998	34
    Lome,1999	7
    Lome,2000	12
    Lome,2001	1
    Lome,2002	2
    Lome,2003	5
    Lome,2004	1
    Lome,2005	9
    Lome,2006	5
    Lome,2008	9
    Lome,2010	31
    Lome,2011	1
    Lome,2012	1
    Lome,2013	3
    Lome,2014	1
    Lome,2015	15
    Lome,2016	13
    Lome,2017	28
    Lome,2018	1
    Lome,2019	30
    Lome,2020	22
    Louisville,1995	1
    Louisville,1996	1
    Louisville,1997	1
    Louisville,1998	1
    Louisville,1999	8
    Louisville,2001	1
    Louisville,2002	6
    Louisville,2005	4
    Louisville,2006	4
    Louisville,2007	11
    Louisville,2008	1
    Louisville,2010	14
    Louisville,2011	13
    Louisville,2012	14
    Louisville,2016	1
    Louisville,2017	2
    Louisville,2018	4
    Louisville,2019	2
    Lubbock,1995	8
    Lubbock,1996	12
    Lubbock,1998	23
    Lubbock,1999	2
    Lubbock,2000	7
    Lubbock,2001	20
    Lubbock,2002	3
    Lubbock,2003	14
    Lubbock,2004	1
    Lubbock,2005	1
    Lubbock,2006	10
    Lubbock,2008	5
    Lubbock,2009	10
    Lubbock,2011	57
    Lubbock,2012	13
    Lubbock,2013	11
    Lubbock,2014	6
    Lubbock,2015	4
    Lubbock,2016	16
    Lubbock,2017	4
    Lubbock,2018	17
    Lubbock,2019	15
    Lusaka,1995	11
    Lusaka,1996	10
    Lusaka,1997	7
    Lusaka,1998	11
    Lusaka,1999	9
    Lusaka,2000	2
    Lusaka,2001	1
    Lusaka,2002	1
    Lusaka,2003	4
    Lusaka,2004	1
    Lusaka,2005	1
    Lusaka,2006	2
    Lusaka,2011	2
    Lusaka,2012	1
    Lusaka,2013	1
    Macon,1995	3
    Macon,1996	3
    Macon,1998	5
    Macon,1999	4
    Macon,2000	3
    Macon,2002	5
    Macon,2004	2
    Macon,2005	4
    Macon,2006	3
    Macon,2007	7
    Macon,2008	1
    Macon,2009	2
    Macon,2010	7
    Macon,2011	5
    Macon,2012	5
    Macon,2015	3
    Macon,2016	8
    Macon,2019	1
    Madison,1995	3
    Madison,2012	7
    Madrid,1995	9
    Madrid,1996	2
    Madrid,1997	2
    Madrid,2003	1
    Madrid,2004	3
    Madrid,2005	4
    Madrid,2006	1
    Madrid,2008	1
    Madrid,2010	1
    Madrid,2011	3
    Madrid,2012	13
    Madrid,2013	2
    Madrid,2014	2
    Madrid,2015	22
    Madrid,2016	13
    Madrid,2017	15
    Madrid,2018	6
    Madrid,2019	13
    Managua,1995	1
    Managua,1996	4
    Managua,1997	25
    Managua,1998	80
    Managua,1999	9
    Managua,2000	10
    Managua,2001	34
    Managua,2002	27
    Managua,2003	18
    Managua,2004	22
    Managua,2005	43
    Managua,2006	20
    Managua,2007	22
    Managua,2008	18
    Managua,2009	10
    Managua,2010	31
    Managua,2011	15
    Managua,2012	7
    Managua,2013	31
    Managua,2014	53
    Managua,2015	27
    Managua,2016	54
    Managua,2017	22
    Managua,2018	7
    Managua,2019	23
    Managua,2020	13
    Manama,1995	136
    Manama,1996	149
    Manama,1997	158
    Manama,1998	160
    Manama,1999	170
    Manama,2000	163
    Manama,2001	160
    Manama,2002	165
    Manama,2003	161
    Manama,2004	157
    Manama,2005	144
    Manama,2006	174
    Manama,2007	167
    Manama,2008	159
    Manama,2009	156
    Manama,2010	164
    Manama,2011	162
    Manama,2012	182
    Manama,2013	152
    Manama,2014	179
    Manama,2015	181
    Manama,2016	158
    Manama,2017	182
    Manama,2018	168
    Manama,2019	176
    Manama,2020	7
    Manila,1995	11
    Manila,1996	11
    Manila,1997	22
    Manila,1998	50
    Manila,1999	7
    Manila,2000	21
    Manila,2001	40
    Manila,2002	25
    Manila,2003	39
    Manila,2004	25
    Manila,2005	32
    Manila,2006	35
    Manila,2007	48
    Manila,2008	24
    Manila,2009	11
    Manila,2010	53
    Manila,2011	22
    Manila,2012	28
    Manila,2013	56
    Manila,2014	46
    Manila,2015	53
    Manila,2016	73
    Manila,2017	60
    Manila,2018	55
    Manila,2019	67
    Manila,2020	41
    Maputo,1995	3
    Maputo,1996	5
    Maputo,1997	3
    Maputo,1998	4
    Maputo,1999	10
    Maputo,2000	3
    Maputo,2001	2
    Maputo,2002	6
    Maputo,2003	10
    Maputo,2004	7
    Maputo,2005	8
    Maputo,2006	6
    Maputo,2007	4
    Maputo,2008	4
    Maputo,2009	10
    Maputo,2010	2
    Maputo,2011	4
    Maputo,2013	6
    Maputo,2014	8
    Maputo,2015	2
    Maputo,2016	6
    Maputo,2017	6
    Maputo,2018	3
    Maputo,2019	6
    Maputo,2020	2
    Medford,1996	2
    Medford,1998	2
    Medford,2002	3
    Medford,2003	3
    Medford,2004	2
    Medford,2006	3
    Medford,2008	3
    Medford,2009	3
    Medford,2012	1
    Medford,2013	2
    Medford,2014	4
    Medford,2015	10
    Medford,2016	3
    Medford,2017	5
    Medford,2018	2
    Melbourne,1997	1
    Melbourne,2000	1
    Melbourne,2006	2
    Melbourne,2010	2
    Melbourne,2011	2
    Melbourne,2013	1
    Melbourne,2016	1
    Melbourne,2017	2
    Melbourne,2020	2
    Memphis,1995	5
    Memphis,1996	4
    Memphis,1997	3
    Memphis,1998	15
    Memphis,1999	14
    Memphis,2000	31
    Memphis,2001	2
    Memphis,2002	7
    Memphis,2003	2
    Memphis,2004	2
    Memphis,2005	20
    Memphis,2006	24
    Memphis,2007	24
    Memphis,2008	10
    Memphis,2009	9
    Memphis,2010	33
    Memphis,2011	31
    Memphis,2012	26
    Memphis,2013	8
    Memphis,2014	4
    Memphis,2015	17
    Memphis,2016	27
    Memphis,2017	5
    Memphis,2018	5
    Memphis,2019	4
    Miami Beach,1995	5
    Miami Beach,1997	3
    Miami Beach,1998	17
    Miami Beach,1999	3
    Miami Beach,2001	2
    Miami Beach,2004	8
    Miami Beach,2005	8
    Miami Beach,2006	2
    Miami Beach,2007	5
    Miami Beach,2009	13
    Miami Beach,2010	14
    Miami Beach,2011	10
    Miami Beach,2014	5
    Miami Beach,2015	3
    Miami Beach,2016	8
    Miami Beach,2017	36
    Miami Beach,2019	23
    Midland Odessa,1995	8
    Midland Odessa,1996	29
    Midland Odessa,1997	5
    Midland Odessa,1998	47
    Midland Odessa,1999	22
    Midland Odessa,2000	26
    Midland Odessa,2001	33
    Midland Odessa,2002	16
    Midland Odessa,2003	22
    Midland Odessa,2004	5
    Midland Odessa,2005	7
    Midland Odessa,2006	28
    Midland Odessa,2008	17
    Midland Odessa,2009	19
    Midland Odessa,2010	17
    Midland Odessa,2011	73
    Midland Odessa,2012	34
    Midland Odessa,2013	24
    Midland Odessa,2014	23
    Midland Odessa,2015	27
    Midland Odessa,2016	39
    Midland Odessa,2017	24
    Midland Odessa,2018	52
    Midland Odessa,2019	38
    Midland Odessa,2020	3
    Milan,2017	1
    Milan,2019	1
    Milwaukee,1995	2
    Milwaukee,1999	1
    Milwaukee,2002	1
    Milwaukee,2006	2
    Milwaukee,2011	1
    Milwaukee,2012	5
    Milwaukee,2013	3
    Milwaukee,2018	1
    Minneapolis St. Paul,1995	2
    Minneapolis St. Paul,1996	1
    Minneapolis St. Paul,1999	2
    Minneapolis St. Paul,2001	5
    Minneapolis St. Paul,2002	4
    Minneapolis St. Paul,2005	4
    Minneapolis St. Paul,2006	6
    Minneapolis St. Paul,2011	5
    Minneapolis St. Paul,2012	4
    Minneapolis St. Paul,2013	3
    Minneapolis St. Paul,2018	1
    Mobile,1995	1
    Mobile,1996	1
    Mobile,1997	1
    Mobile,1998	3
    Mobile,1999	1
    Mobile,2000	8
    Mobile,2007	2
    Mobile,2009	8
    Mobile,2010	4
    Mobile,2011	3
    Mobile,2018	2
    Mobile,2019	3
    Monterrey,1995	111
    Monterrey,1996	123
    Monterrey,1997	101
    Monterrey,1998	121
    Monterrey,1999	103
    Monterrey,2000	116
    Monterrey,2001	101
    Monterrey,2002	91
    Monterrey,2003	82
    Monterrey,2004	75
    Monterrey,2005	86
    Monterrey,2006	106
    Monterrey,2007	47
    Monterrey,2008	84
    Monterrey,2009	105
    Monterrey,2010	64
    Monterrey,2011	106
    Monterrey,2012	60
    Monterrey,2013	54
    Monterrey,2014	53
    Monterrey,2015	27
    Monterrey,2016	32
    Monterrey,2017	50
    Monterrey,2018	43
    Monterrey,2019	59
    Monterrey,2020	4
    Montgomery,1995	2
    Montgomery,1996	1
    Montgomery,1997	1
    Montgomery,1998	6
    Montgomery,1999	6
    Montgomery,2000	8
    Montgomery,2004	5
    Montgomery,2006	5
    Montgomery,2007	15
    Montgomery,2008	2
    Montgomery,2009	4
    Montgomery,2010	7
    Montgomery,2011	9
    Montgomery,2012	7
    Montgomery,2014	3
    Montgomery,2015	4
    Montgomery,2016	4
    Montgomery,2017	1
    Montgomery,2019	5
    Montvideo,2003	1
    Moscow,2010	4
    Muscat,1995	3
    Muscat,2001	133
    Muscat,2002	133
    Muscat,2003	116
    Muscat,2004	136
    Muscat,2005	137
    Muscat,2006	142
    Muscat,2007	57
    Muscat,2008	127
    Muscat,2009	160
    Muscat,2010	166
    Muscat,2011	97
    Muscat,2012	48
    Muscat,2013	121
    Muscat,2014	117
    Muscat,2015	162
    Muscat,2016	117
    Muscat,2017	75
    Muscat,2018	123
    Muscat,2019	36
    Nashville,1995	2
    Nashville,1996	1
    Nashville,1997	2
    Nashville,1999	4
    Nashville,2000	2
    Nashville,2005	5
    Nashville,2006	6
    Nashville,2007	17
    Nashville,2008	1
    Nashville,2009	1
    Nashville,2010	2
    Nashville,2011	3
    Nashville,2012	9
    Nashville,2016	1
    Nashville,2017	2
    Nashville,2018	1
    Nassau,1995	2
    Nassau,1998	8
    Nassau,1999	4
    Nassau,2000	4
    Nassau,2001	4
    Nassau,2002	4
    Nassau,2003	11
    Nassau,2004	18
    Nassau,2005	65
    Nassau,2006	21
    Nassau,2007	44
    Nassau,2008	36
    Nassau,2009	52
    Nassau,2010	61
    Nassau,2011	49
    Nassau,2012	9
    Nassau,2014	5
    Nassau,2015	5
    Nassau,2016	27
    Nassau,2017	76
    Nassau,2019	4
    New Orleans,1995	7
    New Orleans,1997	2
    New Orleans,1998	14
    New Orleans,1999	4
    New Orleans,2000	17
    New Orleans,2001	1
    New Orleans,2002	3
    New Orleans,2003	2
    New Orleans,2005	6
    New Orleans,2006	2
    New Orleans,2007	10
    New Orleans,2008	2
    New Orleans,2009	13
    New Orleans,2010	17
    New Orleans,2011	32
    New Orleans,2012	5
    New Orleans,2013	4
    New Orleans,2014	3
    New Orleans,2015	18
    New Orleans,2016	31
    New Orleans,2017	1
    New Orleans,2018	11
    New Orleans,2019	27
    New York City,1995	6
    New York City,1997	3
    New York City,1998	1
    New York City,1999	8
    New York City,2000	1
    New York City,2001	5
    New York City,2002	3
    New York City,2003	2
    New York City,2005	5
    New York City,2006	5
    New York City,2007	3
    New York City,2008	5
    New York City,2010	11
    New York City,2011	3
    New York City,2012	7
    New York City,2013	8
    New York City,2015	2
    New York City,2016	8
    New York City,2017	5
    New York City,2018	7
    New York City,2019	4
    Newark,1995	3
    Newark,1997	3
    Newark,1999	9
    Newark,2001	5
    Newark,2002	8
    Newark,2003	1
    Newark,2005	8
    Newark,2006	5
    Newark,2008	4
    Newark,2010	10
    Newark,2011	7
    Newark,2012	6
    Newark,2013	8
    Newark,2015	1
    Newark,2016	5
    Newark,2017	2
    Newark,2018	5
    Newark,2019	3
    Niamey,1995	179
    Niamey,1996	169
    Niamey,1997	176
    Niamey,1998	139
    Niamey,1999	157
    Niamey,2000	164
    Niamey,2001	167
    Niamey,2002	167
    Niamey,2003	179
    Niamey,2004	187
    Niamey,2005	178
    Niamey,2006	176
    Niamey,2007	180
    Niamey,2008	159
    Niamey,2009	202
    Niamey,2010	196
    Niamey,2011	207
    Niamey,2012	196
    Niamey,2013	188
    Niamey,2014	186
    Niamey,2015	188
    Niamey,2016	197
    Niamey,2017	177
    Niamey,2018	194
    Niamey,2019	191
    Niamey,2020	75
    Nicosia,1995	23
    Nicosia,1996	48
    Nicosia,1997	12
    Nicosia,1998	49
    Nicosia,1999	6
    Nicosia,2000	38
    Nicosia,2001	29
    Nicosia,2002	32
    Nicosia,2003	2
    Nicosia,2004	14
    Nicosia,2005	11
    Nicosia,2006	15
    Nicosia,2007	32
    Nicosia,2008	36
    Nicosia,2009	27
    Nicosia,2010	1
    Norfolk,1995	7
    Norfolk,1996	1
    Norfolk,1997	3
    Norfolk,1998	2
    Norfolk,1999	6
    Norfolk,2001	2
    Norfolk,2002	2
    Norfolk,2003	2
    Norfolk,2005	1
    Norfolk,2006	5
    Norfolk,2007	3
    Norfolk,2008	3
    Norfolk,2010	9
    Norfolk,2011	7
    Norfolk,2012	6
    Norfolk,2014	2
    Norfolk,2015	2
    Norfolk,2016	7
    Norfolk,2017	4
    Norfolk,2019	7
    North Platte,1995	3
    North Platte,2000	1
    North Platte,2002	3
    North Platte,2003	2
    North Platte,2005	1
    North Platte,2006	3
    North Platte,2011	1
    North Platte,2012	8
    North Platte,2013	1
    North Platte,2017	1
    Nouakchott,1995	42
    Nouakchott,1996	29
    Nouakchott,1997	42
    Nouakchott,1998	34
    Nouakchott,1999	32
    Nouakchott,2000	25
    Nouakchott,2001	37
    Nouakchott,2002	35
    Nouakchott,2003	27
    Nouakchott,2004	25
    Nouakchott,2005	43
    Nouakchott,2006	43
    Nouakchott,2007	34
    Nouakchott,2008	45
    Nouakchott,2009	37
    Nouakchott,2010	30
    Nouakchott,2011	29
    Nouakchott,2012	41
    Nouakchott,2013	38
    Nouakchott,2014	36
    Nouakchott,2015	39
    Nouakchott,2016	30
    Nouakchott,2017	38
    Oklahoma City,1995	3
    Oklahoma City,1996	10
    Oklahoma City,1997	1
    Oklahoma City,1998	52
    Oklahoma City,1999	12
    Oklahoma City,2000	24
    Oklahoma City,2001	22
    Oklahoma City,2003	14
    Oklahoma City,2005	1
    Oklahoma City,2006	32
    Oklahoma City,2007	6
    Oklahoma City,2008	11
    Oklahoma City,2009	13
    Oklahoma City,2010	18
    Oklahoma City,2011	65
    Oklahoma City,2012	30
    Oklahoma City,2013	10
    Oklahoma City,2014	6
    Oklahoma City,2015	3
    Oklahoma City,2016	7
    Oklahoma City,2017	6
    Oklahoma City,2018	3
    Oklahoma City,2019	7
    Omaha,1995	7
    Omaha,1996	2
    Omaha,1997	2
    Omaha,1999	4
    Omaha,2001	4
    Omaha,2002	4
    Omaha,2003	4
    Omaha,2005	3
    Omaha,2006	7
    Omaha,2007	3
    Omaha,2008	1
    Omaha,2009	2
    Omaha,2010	4
    Omaha,2011	8
    Omaha,2012	16
    Omaha,2013	2
    Omaha,2014	1
    Omaha,2015	1
    Omaha,2016	6
    Omaha,2017	4
    Omaha,2018	5
    Omaha,2019	5
    Orlando,1995	1
    Orlando,1997	1
    Orlando,1998	6
    Orlando,2002	1
    Orlando,2007	1
    Orlando,2009	2
    Orlando,2010	2
    Orlando,2015	1
    Orlando,2016	6
    Orlando,2019	2
    Osaka,1995	22
    Osaka,1996	6
    Osaka,1998	8
    Osaka,1999	5
    Osaka,2000	13
    Osaka,2001	17
    Osaka,2002	17
    Osaka,2003	5
    Osaka,2004	17
    Osaka,2005	8
    Osaka,2006	25
    Osaka,2007	28
    Osaka,2008	34
    Osaka,2009	9
    Osaka,2010	44
    Osaka,2011	32
    Osaka,2012	32
    Osaka,2013	33
    Osaka,2014	14
    Osaka,2015	21
    Osaka,2016	29
    Osaka,2017	33
    Osaka,2018	39
    Osaka,2019	32
    Paducah,1995	1
    Paducah,1996	2
    Paducah,1997	3
    Paducah,1999	4
    Paducah,2001	1
    Paducah,2003	1
    Paducah,2005	1
    Paducah,2007	4
    Paducah,2008	2
    Paducah,2009	1
    Paducah,2010	6
    Paducah,2011	3
    Paducah,2012	15
    Paducah,2014	1
    Paducah,2016	1
    Paducah,2017	2
    Paducah,2018	1
    Panama City,1997	6
    Panama City,1998	22
    Panama City,1999	5
    Panama City,2002	8
    Panama City,2003	8
    Panama City,2004	6
    Panama City,2006	1
    Panama City,2007	3
    Panama City,2008	4
    Panama City,2009	2
    Panama City,2010	4
    Panama City,2012	1
    Panama City,2013	4
    Panama City,2014	5
    Panama City,2015	20
    Panama City,2016	3
    Panama City,2017	4
    Panama City,2020	6
    Paramaribo,1995	1
    Paramaribo,1996	1
    Paramaribo,1999	3
    Paramaribo,2000	4
    Paramaribo,2001	2
    Paramaribo,2002	2
    Paramaribo,2003	15
    Paramaribo,2004	3
    Paramaribo,2005	2
    Paramaribo,2007	1
    Paramaribo,2009	4
    Paramaribo,2010	3
    Paramaribo,2015	2
    Paramaribo,2016	1
    Paramaribo,2017	2
    Paramaribo,2019	1
    Paris,1995	1
    Paris,1998	2
    Paris,2003	5
    Paris,2019	2
    Peoria,1995	2
    Peoria,1997	2
    Peoria,1999	1
    Peoria,2002	2
    Peoria,2005	2
    Peoria,2006	3
    Peoria,2011	3
    Peoria,2012	10
    Perth,1995	5
    Perth,1996	7
    Perth,1997	10
    Perth,1998	7
    Perth,1999	3
    Perth,2000	5
    Perth,2001	5
    Perth,2002	4
    Perth,2003	7
    Perth,2004	8
    Perth,2005	2
    Perth,2006	4
    Perth,2007	11
    Perth,2008	7
    Perth,2009	3
    Perth,2010	11
    Perth,2011	7
    Perth,2012	9
    Perth,2013	6
    Perth,2014	3
    Perth,2015	5
    Perth,2016	8
    Perth,2017	3
    Perth,2018	2
    Perth,2019	8
    Perth,2020	3
    Philadelphia,1995	8
    Philadelphia,1997	3
    Philadelphia,1999	6
    Philadelphia,2001	3
    Philadelphia,2002	9
    Philadelphia,2003	1
    Philadelphia,2005	3
    Philadelphia,2006	5
    Philadelphia,2007	1
    Philadelphia,2008	2
    Philadelphia,2010	6
    Philadelphia,2011	4
    Philadelphia,2012	6
    Philadelphia,2013	5
    Philadelphia,2015	1
    Philadelphia,2016	4
    Philadelphia,2017	3
    Philadelphia,2019	2
    Phoenix,1995	105
    Phoenix,1996	115
    Phoenix,1997	126
    Phoenix,1998	91
    Phoenix,1999	99
    Phoenix,2000	126
    Phoenix,2001	138
    Phoenix,2002	118
    Phoenix,2003	139
    Phoenix,2004	119
    Phoenix,2005	116
    Phoenix,2006	122
    Phoenix,2007	129
    Phoenix,2008	118
    Phoenix,2009	131
    Phoenix,2010	116
    Phoenix,2011	118
    Phoenix,2012	125
    Phoenix,2013	123
    Phoenix,2014	123
    Phoenix,2015	124
    Phoenix,2016	113
    Phoenix,2017	117
    Phoenix,2018	131
    Phoenix,2019	112
    Phoenix,2020	14
    Pittsburgh,1995	1
    Pittsburgh,2002	1
    Pittsburgh,2011	1
    Pittsburgh,2012	1
    Pocatello,2000	1
    Pocatello,2003	2
    Pocatello,2014	1
    Port au Prince,1995	150
    Port au Prince,1996	94
    Port au Prince,1997	109
    Port au Prince,1999	19
    Port au Prince,2000	36
    Port au Prince,2001	53
    Port au Prince,2002	120
    Port au Prince,2003	116
    Port au Prince,2004	91
    Port au Prince,2005	140
    Port au Prince,2006	55
    Port au Prince,2007	40
    Port au Prince,2008	37
    Port au Prince,2009	154
    Port au Prince,2010	162
    Port au Prince,2011	109
    Port au Prince,2012	85
    Port au Prince,2013	124
    Port au Prince,2014	29
    Port au Prince,2015	187
    Port au Prince,2016	132
    Port au Prince,2017	136
    Port au Prince,2018	129
    Port au Prince,2019	65
    Port au Prince,2020	6
    Portland,1998	1
    Portland,2009	2
    Portland,2011	1
    Portland,2015	1
    Pristina,1999	1
    Pristina,2000	1
    Pueblo,2001	1
    Pueblo,2002	2
    Pueblo,2003	9
    Pueblo,2005	2
    Pueblo,2006	1
    Pueblo,2008	1
    Pueblo,2012	3
    Pueblo,2013	1
    Pueblo,2016	2
    Pueblo,2018	3
    Pueblo,2019	2
    Pyongyang,1997	1
    Pyongyang,2000	1
    Pyongyang,2014	1
    Pyongyang,2018	7
    Pyongyang,2019	2
    Rabat,1995	2
    Rabat,2000	2
    Rabat,2003	3
    Rabat,2004	3
    Rabat,2006	1
    Rabat,2009	2
    Rabat,2010	3
    Rabat,2011	2
    Rabat,2012	2
    Rabat,2015	1
    Raleigh Durham,1995	1
    Raleigh Durham,1996	2
    Raleigh Durham,1998	1
    Raleigh Durham,1999	3
    Raleigh Durham,2001	1
    Raleigh Durham,2002	3
    Raleigh Durham,2005	2
    Raleigh Durham,2006	1
    Raleigh Durham,2007	8
    Raleigh Durham,2008	3
    Raleigh Durham,2010	6
    Raleigh Durham,2011	10
    Raleigh Durham,2012	8
    Raleigh Durham,2015	3
    Raleigh Durham,2017	3
    Rangoon,1996	32
    Rangoon,1997	57
    Rangoon,1998	65
    Rangoon,1999	38
    Rangoon,2000	16
    Rangoon,2001	39
    Rangoon,2002	51
    Rangoon,2003	51
    Rangoon,2004	48
    Rangoon,2005	64
    Rangoon,2006	64
    Rangoon,2007	46
    Rangoon,2008	31
    Rangoon,2009	60
    Rangoon,2010	80
    Rangoon,2011	26
    Rangoon,2012	66
    Rangoon,2013	64
    Rangoon,2014	37
    Rangoon,2015	47
    Rangoon,2016	66
    Rangoon,2017	52
    Rangoon,2018	40
    Rangoon,2019	55
    Rangoon,2020	32
    Rapid City,2001	1
    Rapid City,2002	5
    Rapid City,2003	3
    Rapid City,2005	1
    Rapid City,2006	6
    Rapid City,2007	7
    Rapid City,2011	1
    Rapid City,2012	4
    Reno,1998	1
    Reno,2002	3
    Reno,2003	4
    Reno,2005	4
    Reno,2006	4
    Reno,2007	2
    Reno,2013	6
    Reno,2014	4
    Reno,2015	2
    Reno,2016	1
    Reno,2017	3
    Reno,2018	2
    Rhode Island,1995	1
    Rhode Island,1999	2
    Rhode Island,2001	1
    Rhode Island,2002	2
    Rhode Island,2006	1
    Rhode Island,2011	1
    Rhode Island,2019	1
    Richmond,1995	1
    Richmond,1997	1
    Richmond,1998	2
    Richmond,1999	3
    Richmond,2002	3
    Richmond,2005	2
    Richmond,2006	7
    Richmond,2007	3
    Richmond,2008	4
    Richmond,2009	2
    Richmond,2010	10
    Richmond,2011	7
    Richmond,2012	6
    Richmond,2013	1
    Richmond,2014	3
    Richmond,2015	3
    Richmond,2016	2
    Richmond,2017	5
    Richmond,2018	1
    Richmond,2019	2
    Rio de Janeiro,1995	8
    Rio de Janeiro,1996	13
    Rio de Janeiro,1997	7
    Rio de Janeiro,1998	9
    Rio de Janeiro,1999	2
    Rio de Janeiro,2000	1
    Rio de Janeiro,2001	2
    Rio de Janeiro,2002	6
    Rio de Janeiro,2003	8
    Rio de Janeiro,2005	6
    Rio de Janeiro,2006	3
    Rio de Janeiro,2010	11
    Rio de Janeiro,2011	3
    Rio de Janeiro,2012	3
    Rio de Janeiro,2013	10
    Rio de Janeiro,2014	9
    Rio de Janeiro,2015	28
    Rio de Janeiro,2016	8
    Rio de Janeiro,2017	16
    Rio de Janeiro,2018	4
    Rio de Janeiro,2019	11
    Riyadh,1995	137
    Riyadh,1996	147
    Riyadh,1997	151
    Riyadh,1998	160
    Riyadh,1999	164
    Riyadh,2000	163
    Riyadh,2001	151
    Riyadh,2002	152
    Riyadh,2003	153
    Riyadh,2004	142
    Riyadh,2005	144
    Riyadh,2006	154
    Riyadh,2007	160
    Riyadh,2008	152
    Riyadh,2009	155
    Riyadh,2010	164
    Riyadh,2011	154
    Riyadh,2012	154
    Riyadh,2013	141
    Riyadh,2014	162
    Riyadh,2015	177
    Riyadh,2016	152
    Riyadh,2017	169
    Riyadh,2018	152
    Riyadh,2019	160
    Riyadh,2020	16
    Roanoke,1999	2
    Roanoke,2007	3
    Roanoke,2010	1
    Roanoke,2011	1
    Roanoke,2012	4
    Roanoke,2017	1
    Rochester,2006	1
    Rockford,1995	2
    Rockford,1999	1
    Rockford,2002	1
    Rockford,2011	3
    Rockford,2012	5
    Sacramento,1996	6
    Sacramento,1997	1
    Sacramento,1998	2
    Sacramento,1999	2
    Sacramento,2000	3
    Sacramento,2001	1
    Sacramento,2002	1
    Sacramento,2006	5
    Sacramento,2008	2
    Sacramento,2009	1
    Sacramento,2010	1
    Sacramento,2013	5
    Sacramento,2015	2
    Sacramento,2017	7
    Sacramento,2018	1
    Salem,2006	1
    Salem,2009	2
    Salem,2015	2
    Salt Lake City,1995	1
    Salt Lake City,1996	2
    Salt Lake City,1997	1
    Salt Lake City,1998	3
    Salt Lake City,1999	2
    Salt Lake City,2000	8
    Salt Lake City,2001	6
    Salt Lake City,2002	13
    Salt Lake City,2003	19
    Salt Lake City,2004	1
    Salt Lake City,2005	5
    Salt Lake City,2006	10
    Salt Lake City,2007	14
    Salt Lake City,2008	6
    Salt Lake City,2009	2
    Salt Lake City,2010	1
    Salt Lake City,2011	1
    Salt Lake City,2012	10
    Salt Lake City,2013	20
    Salt Lake City,2014	6
    Salt Lake City,2015	10
    Salt Lake City,2016	20
    Salt Lake City,2017	21
    Salt Lake City,2018	9
    Salt Lake City,2019	14
    San Angelo,1995	13
    San Angelo,1996	31
    San Angelo,1997	7
    San Angelo,1998	43
    San Angelo,1999	17
    San Angelo,2000	57
    San Angelo,2001	41
    San Angelo,2002	18
    San Angelo,2003	15
    San Angelo,2004	4
    San Angelo,2005	3
    San Angelo,2006	35
    San Angelo,2007	1
    San Angelo,2008	26
    San Angelo,2009	36
    San Angelo,2010	41
    San Angelo,2011	92
    San Angelo,2012	53
    San Angelo,2013	33
    San Angelo,2014	20
    San Angelo,2015	36
    San Angelo,2016	36
    San Angelo,2017	25
    San Angelo,2018	58
    San Angelo,2019	36
    San Angelo,2020	2
    San Antonio,1995	8
    San Antonio,1996	35
    San Antonio,1997	14
    San Antonio,1998	37
    San Antonio,1999	13
    San Antonio,2000	27
    San Antonio,2001	25
    San Antonio,2002	4
    San Antonio,2003	2
    San Antonio,2004	10
    San Antonio,2005	21
    San Antonio,2006	30
    San Antonio,2008	18
    San Antonio,2009	64
    San Antonio,2010	22
    San Antonio,2011	69
    San Antonio,2012	33
    San Antonio,2013	46
    San Antonio,2014	25
    San Antonio,2015	29
    San Antonio,2016	23
    San Antonio,2017	29
    San Antonio,2018	36
    San Antonio,2019	34
    San Diego,2016	1
    San Juan Puerto Rico,1995	6
    San Juan Puerto Rico,2004	1
    San Juan Puerto Rico,2005	3
    San Juan Puerto Rico,2009	2
    San Juan Puerto Rico,2010	2
    San Juan Puerto Rico,2012	2
    Santo Domingo,1998	2
    Santo Domingo,1999	1
    Santo Domingo,2001	1
    Santo Domingo,2005	2
    Santo Domingo,2007	1
    Santo Domingo,2009	1
    Santo Domingo,2010	1
    Santo Domingo,2012	1
    Santo Domingo,2013	1
    Santo Domingo,2014	2
    Santo Domingo,2015	7
    Santo Domingo,2016	3
    Santo Domingo,2017	2
    Santo Domingo,2019	8
    Sao Paulo,1997	2
    Savannah,1995	6
    Savannah,1996	3
    Savannah,1997	1
    Savannah,1998	10
    Savannah,1999	6
    Savannah,2000	1
    Savannah,2002	2
    Savannah,2007	2
    Savannah,2008	2
    Savannah,2009	2
    Savannah,2010	9
    Savannah,2011	13
    Savannah,2012	5
    Savannah,2013	1
    Savannah,2014	4
    Savannah,2015	2
    Savannah,2016	12
    Savannah,2017	4
    Savannah,2019	8
    Seattle,2009	1
    Seattle,2015	1
    Seoul,2002	1
    Seoul,2008	1
    Seoul,2012	7
    Seoul,2014	2
    Seoul,2016	1
    Seoul,2017	1
    Seoul,2018	18
    Seoul,2019	5
    Shanghai,1995	18
    Shanghai,1996	6
    Shanghai,1997	10
    Shanghai,1998	32
    Shanghai,1999	6
    Shanghai,2000	18
    Shanghai,2001	26
    Shanghai,2002	11
    Shanghai,2003	40
    Shanghai,2004	28
    Shanghai,2005	26
    Shanghai,2006	27
    Shanghai,2007	32
    Shanghai,2008	30
    Shanghai,2009	22
    Shanghai,2010	34
    Shanghai,2011	20
    Shanghai,2012	34
    Shanghai,2013	55
    Shanghai,2014	14
    Shanghai,2015	16
    Shanghai,2016	44
    Shanghai,2017	46
    Shanghai,2018	43
    Shanghai,2019	25
    Shenyang,1999	1
    Shenyang,2002	1
    Shenyang,2018	7
    Shreveport,1995	19
    Shreveport,1996	3
    Shreveport,1997	4
    Shreveport,1998	47
    Shreveport,1999	16
    Shreveport,2000	30
    Shreveport,2001	6
    Shreveport,2002	5
    Shreveport,2003	3
    Shreveport,2004	4
    Shreveport,2005	29
    Shreveport,2006	24
    Shreveport,2007	8
    Shreveport,2008	14
    Shreveport,2009	17
    Shreveport,2010	33
    Shreveport,2011	61
    Shreveport,2012	20
    Shreveport,2013	22
    Shreveport,2014	1
    Shreveport,2015	23
    Shreveport,2016	19
    Shreveport,2017	3
    Shreveport,2018	28
    Shreveport,2019	12
    Singapore,1995	4
    Singapore,1996	2
    Singapore,1997	13
    Singapore,1998	39
    Singapore,1999	1
    Singapore,2000	5
    Singapore,2001	2
    Singapore,2002	7
    Singapore,2003	17
    Singapore,2004	20
    Singapore,2005	12
    Singapore,2007	1
    Singapore,2009	11
    Singapore,2010	15
    Singapore,2011	2
    Singapore,2013	10
    Singapore,2014	5
    Singapore,2015	6
    Singapore,2016	21
    Singapore,2017	2
    Singapore,2018	11
    Singapore,2019	9
    Singapore,2020	3
    Sioux City,1995	4
    Sioux City,1997	1
    Sioux City,2002	1
    Sioux City,2003	1
    Sioux City,2004	1
    Sioux City,2005	3
    Sioux City,2006	1
    Sioux City,2007	1
    Sioux City,2011	6
    Sioux City,2012	3
    Sioux City,2016	2
    Sioux City,2017	2
    Sioux City,2019	1
    Sioux Falls,1995	4
    Sioux Falls,2002	3
    Sioux Falls,2003	1
    Sioux Falls,2006	2
    Sioux Falls,2011	2
    Sioux Falls,2012	9
    Sioux Falls,2016	1
    Skopje,1996	3
    Skopje,1997	1
    Skopje,1998	4
    Skopje,2002	1
    Skopje,2005	1
    Skopje,2007	3
    Skopje,2012	1
    Skopje,2015	1
    Skopje,2017	2
    South Bend,1995	3
    South Bend,1999	1
    South Bend,2011	1
    South Bend,2012	5
    Spokane,1998	1
    Spokane,2006	1
    Spokane,2015	4
    Spokane,2017	1
    Spokane,2018	1
    Springfield,1995	6
    Springfield,1997	1
    Springfield,1998	3
    Springfield,1999	4
    Springfield,2000	2
    Springfield,2003	1
    Springfield,2005	6
    Springfield,2006	14
    Springfield,2007	4
    Springfield,2010	6
    Springfield,2011	24
    Springfield,2012	27
    Springfield,2014	2
    Springfield,2016	3
    Springfield,2017	1
    Springfield,2018	3
    St Louis,1995	16
    St Louis,1996	2
    St Louis,1997	7
    St Louis,1998	8
    St Louis,1999	12
    St Louis,2000	3
    St Louis,2001	9
    St Louis,2002	12
    St Louis,2003	8
    St Louis,2004	3
    St Louis,2005	13
    St Louis,2006	13
    St Louis,2007	11
    St Louis,2008	3
    St Louis,2009	6
    St Louis,2010	17
    St Louis,2011	28
    St Louis,2012	25
    St Louis,2013	10
    St Louis,2014	7
    St Louis,2015	7
    St Louis,2016	14
    St Louis,2017	12
    St Louis,2018	9
    St Louis,2019	3
    Sydney,1997	5
    Sydney,1998	1
    Sydney,2000	1
    Sydney,2003	2
    Sydney,2004	1
    Sydney,2005	1
    Sydney,2006	4
    Sydney,2007	3
    Sydney,2008	3
    Sydney,2009	5
    Sydney,2010	1
    Sydney,2012	2
    Sydney,2013	3
    Sydney,2014	5
    Sydney,2015	2
    Sydney,2016	3
    Sydney,2017	2
    Sydney,2018	2
    Sydney,2019	4
    Sydney,2020	2
    Syracuse,2011	2
    Syracuse,2012	1
    Taipei,1995	36
    Taipei,1996	31
    Taipei,1997	11
    Taipei,1998	36
    Taipei,1999	8
    Taipei,2000	22
    Taipei,2001	37
    Taipei,2002	40
    Taipei,2003	61
    Taipei,2004	33
    Taipei,2005	35
    Taipei,2006	42
    Taipei,2007	30
    Taipei,2008	51
    Taipei,2009	42
    Taipei,2010	44
    Taipei,2011	38
    Taipei,2012	29
    Taipei,2013	37
    Taipei,2014	58
    Taipei,2015	36
    Taipei,2016	47
    Taipei,2017	75
    Taipei,2018	69
    Taipei,2019	63
    Taipei,2020	1
    Tallahassee,1995	1
    Tallahassee,1996	2
    Tallahassee,1997	2
    Tallahassee,1998	11
    Tallahassee,1999	3
    Tallahassee,2000	7
    Tallahassee,2002	3
    Tallahassee,2007	5
    Tallahassee,2009	6
    Tallahassee,2010	7
    Tallahassee,2011	9
    Tallahassee,2013	3
    Tallahassee,2014	9
    Tallahassee,2015	8
    Tallahassee,2016	3
    Tallahassee,2017	1
    Tallahassee,2018	2
    Tallahassee,2019	1
    Tampa St. Petersburg,1997	2
    Tampa St. Petersburg,1998	13
    Tampa St. Petersburg,1999	3
    Tampa St. Petersburg,2002	1
    Tampa St. Petersburg,2004	1
    Tampa St. Petersburg,2006	1
    Tampa St. Petersburg,2007	7
    Tampa St. Petersburg,2008	1
    Tampa St. Petersburg,2009	3
    Tampa St. Petersburg,2010	14
    Tampa St. Petersburg,2011	14
    Tampa St. Petersburg,2013	1
    Tampa St. Petersburg,2014	2
    Tampa St. Petersburg,2015	2
    Tampa St. Petersburg,2016	6
    Tampa St. Petersburg,2017	9
    Tampa St. Petersburg,2018	12
    Tampa St. Petersburg,2019	8
    Tashkent,1995	7
    Tashkent,1996	11
    Tashkent,1997	26
    Tashkent,1998	15
    Tashkent,1999	13
    Tashkent,2000	25
    Tashkent,2001	25
    Tashkent,2002	23
    Tashkent,2003	15
    Tashkent,2004	23
    Tashkent,2005	30
    Tashkent,2006	28
    Tashkent,2007	32
    Tashkent,2008	45
    Tashkent,2009	20
    Tashkent,2010	35
    Tashkent,2011	34
    Tashkent,2012	25
    Tashkent,2013	21
    Tashkent,2014	23
    Tashkent,2015	36
    Tashkent,2016	32
    Tashkent,2017	29
    Tashkent,2018	34
    Tashkent,2019	38
    Tbilisi,1998	1
    Tbilisi,1999	7
    Tbilisi,2000	7
    Tbilisi,2001	6
    Tbilisi,2005	3
    Tbilisi,2006	1
    Tegucigalpa,1995	1
    Tegucigalpa,2007	1
    Tegucigalpa,2020	5
    Tel Aviv,1998	2
    Tel Aviv,1999	2
    Tel Aviv,2004	1
    Tel Aviv,2005	1
    Tirana,1997	1
    Tirana,1998	3
    Tirana,1999	2
    Tirana,2000	4
    Tirana,2001	6
    Tirana,2002	3
    Tirana,2003	12
    Tirana,2004	2
    Tirana,2005	2
    Tirana,2007	5
    Tirana,2015	1
    Tirana,2016	1
    Tokyo,1995	6
    Tokyo,1996	2
    Tokyo,1997	3
    Tokyo,2000	1
    Tokyo,2001	1
    Tokyo,2002	1
    Tokyo,2004	4
    Tokyo,2007	3
    Tokyo,2008	3
    Tokyo,2010	7
    Tokyo,2011	6
    Tokyo,2013	7
    Tokyo,2014	3
    Tokyo,2015	3
    Tokyo,2016	1
    Tokyo,2017	1
    Tokyo,2018	10
    Tokyo,2019	3
    Toledo,1995	3
    Toledo,2011	1
    Toledo,2012	2
    Toledo,2019	1
    Topeka,1995	9
    Topeka,1996	3
    Topeka,1997	3
    Topeka,1998	8
    Topeka,1999	12
    Topeka,2000	20
    Topeka,2001	16
    Topeka,2002	8
    Topeka,2003	15
    Topeka,2004	2
    Topeka,2005	6
    Topeka,2006	14
    Topeka,2007	11
    Topeka,2008	5
    Topeka,2009	4
    Topeka,2010	18
    Topeka,2011	27
    Topeka,2012	22
    Topeka,2013	9
    Topeka,2014	8
    Topeka,2015	3
    Topeka,2016	9
    Topeka,2017	5
    Topeka,2018	13
    Topeka,2019	4
    Toronto,1999	1
    Toronto,2001	1
    Toronto,2006	1
    Toronto,2011	1
    Toronto,2012	1
    Tucson,1995	54
    Tucson,1996	58
    Tucson,1997	59
    Tucson,1998	50
    Tucson,1999	32
    Tucson,2000	68
    Tucson,2001	56
    Tucson,2002	65
    Tucson,2003	68
    Tucson,2004	67
    Tucson,2005	58
    Tucson,2006	48
    Tucson,2007	62
    Tucson,2008	48
    Tucson,2009	64
    Tucson,2010	70
    Tucson,2011	70
    Tucson,2012	63
    Tucson,2013	76
    Tucson,2014	72
    Tucson,2015	63
    Tucson,2016	63
    Tucson,2017	70
    Tucson,2018	77
    Tucson,2019	71
    Tucson,2020	2
    Tulsa,1995	16
    Tulsa,1996	12
    Tulsa,1997	10
    Tulsa,1998	36
    Tulsa,1999	19
    Tulsa,2000	33
    Tulsa,2001	35
    Tulsa,2002	19
    Tulsa,2003	30
    Tulsa,2004	8
    Tulsa,2005	16
    Tulsa,2006	32
    Tulsa,2007	14
    Tulsa,2008	19
    Tulsa,2009	20
    Tulsa,2010	30
    Tulsa,2011	58
    Tulsa,2012	40
    Tulsa,2013	19
    Tulsa,2014	14
    Tulsa,2015	26
    Tulsa,2016	31
    Tulsa,2017	10
    Tulsa,2018	24
    Tulsa,2019	14
    Tunis,1995	8
    Tunis,1996	5
    Tunis,1997	4
    Tunis,1998	14
    Tunis,1999	19
    Tunis,2000	14
    Tunis,2001	5
    Tunis,2002	8
    Tunis,2003	33
    Tunis,2004	9
    Tunis,2005	11
    Tunis,2006	13
    Tunis,2007	9
    Tunis,2008	17
    Tunis,2009	16
    Tunis,2010	10
    Tunis,2011	15
    Tunis,2012	28
    Tunis,2013	5
    Tunis,2014	14
    Tunis,2015	11
    Tunis,2016	4
    Tunis,2017	26
    Tunis,2018	7
    Tunis,2019	18
    Tupelo,1996	2
    Tupelo,1998	5
    Tupelo,1999	11
    Tupelo,2000	12
    Tupelo,2001	1
    Tupelo,2005	7
    Tupelo,2006	22
    Tupelo,2007	17
    Tupelo,2008	3
    Tupelo,2009	1
    Tupelo,2010	9
    Tupelo,2011	11
    Tupelo,2012	5
    Tupelo,2015	5
    Tupelo,2016	4
    Tupelo,2017	1
    Tupelo,2019	2
    Ulan-bator,1999	1
    Ulan-bator,2005	1
    Ulan-bator,2007	1
    Vienna,2013	1
    Vientiane,1995	89
    Vientiane,1996	44
    Vientiane,1997	57
    Vientiane,1998	92
    Vientiane,1999	36
    Vientiane,2000	39
    Vientiane,2001	45
    Vientiane,2002	45
    Vientiane,2003	44
    Vientiane,2004	38
    Vientiane,2005	44
    Vientiane,2006	35
    Vientiane,2007	44
    Vientiane,2008	12
    Vientiane,2009	38
    Vientiane,2010	72
    Vientiane,2011	29
    Vientiane,2012	42
    Vientiane,2013	63
    Vientiane,2014	59
    Vientiane,2015	68
    Vientiane,2016	70
    Vientiane,2017	32
    Vientiane,2018	22
    Vientiane,2019	59
    Vientiane,2020	32
    Waco,1995	13
    Waco,1996	32
    Waco,1997	27
    Waco,1998	65
    Waco,1999	46
    Waco,2000	50
    Waco,2001	50
    Waco,2002	26
    Waco,2003	26
    Waco,2004	6
    Waco,2005	22
    Waco,2006	47
    Waco,2007	7
    Waco,2008	28
    Waco,2009	59
    Waco,2010	56
    Waco,2011	93
    Waco,2012	47
    Waco,2013	46
    Waco,2014	20
    Waco,2015	35
    Waco,2016	38
    Waco,2017	31
    Waco,2018	73
    Waco,2019	41
    Washington DC,1995	8
    Washington DC,1997	16
    Washington DC,1999	20
    Washington DC,2001	4
    Washington DC,2002	28
    Washington DC,2005	4
    Washington DC,2006	12
    Washington DC,2007	8
    Washington DC,2008	4
    Washington DC,2009	2
    Washington DC,2010	24
    Washington DC,2011	22
    Washington DC,2012	32
    Washington DC,2013	10
    Washington DC,2014	6
    Washington DC,2015	8
    Washington DC,2016	22
    Washington DC,2017	6
    Washington DC,2018	6
    Washington DC,2019	6
    Washington,1995	8
    Washington,1997	16
    Washington,1999	20
    Washington,2001	4
    Washington,2002	28
    Washington,2005	4
    Washington,2006	12
    Washington,2007	8
    Washington,2008	4
    Washington,2009	2
    Washington,2010	24
    Washington,2011	22
    Washington,2012	32
    Washington,2013	10
    Washington,2014	6
    Washington,2015	8
    Washington,2016	22
    Washington,2017	6
    Washington,2018	6
    Washington,2019	6
    West Palm Beach,1998	8
    West Palm Beach,2004	1
    West Palm Beach,2005	7
    West Palm Beach,2007	1
    West Palm Beach,2009	2
    West Palm Beach,2010	5
    West Palm Beach,2011	17
    West Palm Beach,2013	10
    West Palm Beach,2014	2
    West Palm Beach,2015	1
    West Palm Beach,2016	23
    West Palm Beach,2017	11
    West Palm Beach,2019	4
    Wichita Falls,1995	20
    Wichita Falls,1996	33
    Wichita Falls,1997	17
    Wichita Falls,1998	68
    Wichita Falls,1999	37
    Wichita Falls,2000	60
    Wichita Falls,2001	43
    Wichita Falls,2002	14
    Wichita Falls,2003	34
    Wichita Falls,2004	5
    Wichita Falls,2005	18
    Wichita Falls,2006	51
    Wichita Falls,2007	13
    Wichita Falls,2008	42
    Wichita Falls,2009	34
    Wichita Falls,2010	29
    Wichita Falls,2011	90
    Wichita Falls,2012	44
    Wichita Falls,2013	32
    Wichita Falls,2014	21
    Wichita Falls,2015	18
    Wichita Falls,2016	28
    Wichita Falls,2017	10
    Wichita Falls,2018	39
    Wichita Falls,2019	25
    Wichita,1995	4
    Wichita,1996	5
    Wichita,1998	18
    Wichita,1999	13
    Wichita,2000	27
    Wichita,2001	27
    Wichita,2002	9
    Wichita,2003	17
    Wichita,2004	1
    Wichita,2005	9
    Wichita,2006	19
    Wichita,2007	7
    Wichita,2008	5
    Wichita,2009	8
    Wichita,2010	20
    Wichita,2011	47
    Wichita,2012	35
    Wichita,2013	7
    Wichita,2014	6
    Wichita,2015	11
    Wichita,2016	12
    Wichita,2017	8
    Wichita,2018	10
    Wichita,2019	5
    Wilkes Barre,1995	1
    Wilkes Barre,2011	1
    Wilmington,1995	2
    Wilmington,1997	1
    Wilmington,1999	3
    Wilmington,2001	2
    Wilmington,2002	1
    Wilmington,2006	2
    Wilmington,2007	1
    Wilmington,2008	1
    Wilmington,2010	3
    Windhoek,1995	2
    Windhoek,2001	1
    Windhoek,2002	10
    Windhoek,2003	13
    Windhoek,2009	3
    Windhoek,2012	3
    Windhoek,2013	1
    Windhoek,2016	1
    Windhoek,2018	1
    Windhoek,2019	4
    Windhoek,2020	1
    Winnipeg,1995	2
    Yakima,1998	1
    Yakima,2002	2
    Yakima,2003	2
    Yakima,2006	1
    Yakima,2012	3
    Yakima,2013	1
    Yakima,2014	5
    Yakima,2015	14
    Yakima,2016	5
    Yakima,2017	1
    Yerevan,1995	4
    Yerevan,1996	4
    Yerevan,1997	3
    Yerevan,1998	5
    Yerevan,1999	6
    Yerevan,2000	19
    Yerevan,2001	9
    Yerevan,2003	3
    Youngstown,1995	1
    Yuma,1995	109
    Yuma,1996	118
    Yuma,1997	127
    Yuma,1998	97
    Yuma,1999	113
    Yuma,2000	123
    Yuma,2001	132
    Yuma,2002	111
    Yuma,2003	132
    Yuma,2004	84
    Yuma,2005	81
    Yuma,2006	92
    Zagreb,2007	1
    Zagreb,2011	1
    Zagreb,2013	2
    Zagreb,2015	2
    Zagreb,2017	2


## Ejercicio 4: rango de temperaturas por ciudad (Min/Max)

Encuentra la temperatura mínima y máxima registrada para cada región.


```python
%%writefile mapper_ej4.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or "Region" in line: continue
    
    parts = line.split(",")
    if len(parts) < 8: continue
        
    region = parts[0] # Campo Región
    temp_str = parts[7]
    
    try:
        temp = float(temp_str)
        if temp == -99.0: continue
        
        # Convertimos a Celsius
        temp_c = (temp - 32) / 1.8
        print(f"{region}\t{temp_c}")
    except ValueError:
        continue
```

    Writing mapper_ej4.py



```python
%%writefile reducer_ej4.py
#!/usr/bin/env python3
import sys

current_region = None
min_temp = float('inf')
max_temp = -float('inf')

for line in sys.stdin:
    try:
        region, temp = line.strip().split("\t")
        temp = float(temp)
    except ValueError:
        continue

    if region == current_region:
        if temp < min_temp: min_temp = temp
        if temp > max_temp: max_temp = temp
    else:
        if current_region:
            print(f"{current_region}\tMin:{min_temp:.2f}\tMax:{max_temp:.2f}")
        current_region = region
        min_temp = temp
        max_temp = temp

if current_region:
    print(f"{current_region}\tMin:{min_temp:.2f}\tMax:{max_temp:.2f}")
```

    Writing reducer_ej4.py



```python
!cat city_temperature.csv | python3 mapper_ej4.py | sort | python3 reducer_ej4.py
```

    Africa	Min:0.72	Max:39.33
    Asia	Min:-38.44	Max:39.83
    Australia/South Pacific	Min:-0.72	Max:36.00
    Europe	Min:-29.11	Max:39.17
    Middle East	Min:-16.00	Max:43.33
    North America	Min:-45.56	Max:42.06
    South/Central America & Carribean	Min:0.44	Max:36.33



```python

```
