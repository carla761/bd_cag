# PR0202: Listas en Redis

```python
import redis
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
print("ping:", r.ping())
```


```python
import json

key="PR0202:pedidos"
actual_id=1

def icr_id():
    global actual_id
    id = "id_" + str(actual_id).zfill(4)
    actual_id += 1
    return id

def agregar_pedido(cliente,producto,cantidad=1,urgente=False):
    pedido = {
     "id": icr_id(),
     "cliente": cliente,
     "producto": producto,
     "cantidad": cantidad,
     "urgente": urgente
    }
    
    pedido_json = json.dumps(pedido)
    if (urgente == True):
        r.lpush(key, pedido_json)
    else:
        r.rpush(key, pedido_json)  
    
def procesar_pedido():
    pedido_json = r.lpop(key)
    pedido = json.loads(pedido_json)
    print(pedido)

def procesar_todos():
    while True:
        pedido = procesar_pedido()
        if pedido is None:
            break
            
agregar_pedido("Juan Pérez", "Portátil Lenovo")
agregar_pedido("Maria Lopez", "Ratón inalámbrico")
agregar_pedido("Luis Barros", "Pantalla HP")
agregar_pedido("Laia García", "Cascos inalámbricos")
agregar_pedido("Carlos Rodriguez", "Teclado HP")

tarea = r.lrange(key,0,-1)
print("Lista completa de pedidos:", tarea)

agregar_pedido("Jose Luis", "Cascos Gammer")
agregar_pedido("Marcos Susvilla", "Teclado Gammer")

procesar_todos()

agregar_pedido("Ana Fuertes", "Raton", urgente=True)
```