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

9.  Guarda en la clave mensaje el texto "Bienvenido a Redis".
``` SET "mensaje" "Bienvenido a Redis" ```

10.  Establece un tiempo de expiración de 60 segundos para la clave mensaje.
``` EXPIRE mensaje 60 ```

11.  Elimina la clave usuario:apellido.
``` DEL "usuario:apellido" ```

12.  Elimina el resto de claves que hayas creado
``` DEL "usuario:nombre" ```
``` DEL "usuario:email" ```
``` DEL "contador:visitas" ```