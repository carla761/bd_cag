#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[ ]:

