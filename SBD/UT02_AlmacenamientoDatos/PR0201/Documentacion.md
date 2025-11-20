# PR0201: Cadenas en Redis

## 1. Trabajo con Redis CLI

1. Crea una clave usuario:nombre con tu nombre.

``` SET "usuario:nombre" "Carla" ```

2. Crea una clave usuario:apellido con tu apellido.

``` SET "usuario:apellido" "Alvarez" ```

3. Recupera el valor de ambas claves con GET.

``` GET usuario:nombre ```
``` GET usuario:apellido ```

4. Almacena en usuario:email un correo ficticio y recupéralo.

``` SET "usuario:email" "carlafp@gmail.com" ```
``` GET email ```

5. Cambia el valor de usuario:nombre para que aparezca en mayúsculas.


```SET "usuario:nombre" "CARLA"```

6. Crea la clave contador:visitas con valor 0.

``` SET "contador:visitas" 0 ```

7. Incrementa en 1 el valor de contador:visitas tres veces.

```INCR contador:visitas```
```INCR contador:visitas```
```INCR contador:visitas```

8. Decrementa en 1 el valor de contador:visitas.

```DECR contador:visitas```

9. Guarda en la clave mensaje el texto "Bienvenido a Redis".

``` SET "mensaje" "Bienvenido a Redis" ```

10. Establece un tiempo de expiración de 60 segundos para la clave mensaje.

``` EXPIRE mensaje 60 ```

11. Elimina la clave usuario:apellido.

``` DEL "usuario:apellido" ``` 

12. Elimina el resto de claves que hayas creado

``` DEL "usuario:nombre" ```
``` DEL "usuario:email" ```
``` DEL "contador:visitas" ```

## 2. Trabajo con Python
``` python
import redis

r = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)

print(r.ping())
```
1. Inserta la clave app:version con el valor "1.0".

```r.set("app:version","1.0"``` 

2. Recupera y muestra el valor de app:version.

```print(r.get("app:version"))```

3. Modifica el valor de app:version a "1.1".

```r.set("app:version","1.1", xx=True)```

4. Crea la clave contador:descargas con valor 0.

```r.set("contador:descargas",0)``` 

5. Incrementa en 5 el valor de contador:descargas.

```r.incr("contador:descargas", 5) ```

6. Decrementa en 2 el valor de contador:descargas.

```r.decr("contador:descargas", 2) ```

7. Inserta la clave app:estado con el valor "activo".

```r.set("app:estado","activo")``` 

8. Cambia el valor de app:estado a "mantenimiento".

```r.set("app:estado","mantenimiento", xx=True)``` 

9. Inserta la clave mensaje:bienvenida con el texto "Hola alumno".

```r.set("mensaje:bienvenida","Hola alumno")```

10. Establece un tiempo de expiración de 30 segundos para la clave app:estado.

```r.expire("app:estado", 30)```

11. Verifica si la clave app:estado todavía existe después de unos segundos.

```print(r.exists("app:estado"))```

12. Elimina la clave app:version y muestra un mensaje confirmando su eliminación.

``` python
    borrada = r.delete("app:version")
    if deleted:
        print("app:version eliminada")
    else:
        print("app:version no existía")    
```

# SCRIPT PYTHON 


```python
import redis
import time

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

print("ping:", r.ping())

# app:version
r.set("app:version", "1.0")
print("app:version (antes):", r.get("app:version"))
r.set("app:version", "1.1", xx=True)
print("app:version (después):", r.get("app:version"))

# contador:descargas
r.set("contador:descargas", "0")
r.incr("contador:descargas", 5)
r.decr("contador:descargas", 2)
print("contador:descargas:", r.get("contador:descargas"))

# app:estado y expiración
r.set("app:estado", "activo")
r.set("app:estado", "mantenimiento", xx=True)
r.expire("app:estado", 30)
print("existe app:estado?", bool(r.exists("app:estado")))
print("valor app:estado:", r.get("app:estado"))

# mensaje bienvenida
r.set("mensaje:bienvenida", "Hola alumno")
print("mensaje:bienvenida:", r.get("mensaje:bienvenida"))

# esperar unos segundos si quieres probar expiración (opcional)
# time.sleep(31)
# print("valor app:estado tras espera:", r.get("app:estado"))

# eliminar app:version
borrada = r.delete("app:version")
if (borrada==0):
    print("app:version eliminada")
else:
    print("app:version no existía")    
```
