# PR0205: Monitorización de rendimiento del servidor con Python
### PARTE I: Obtención de métricas
Para esta práctica, utilizaremos la librería psutil para obtener las métricas de rendimiento de la máquina en la que se ejecuta el script.

El siguiente código muestra cómo obtener los porcentajes de uso de CPU y RAM, así como el total de RAM utilizada:

### PARTE II: Modelado y escritura en lote

#### 1\. Diseño del modelo InfluxDB

El modelo debe asegurar que las métricas sean fáciles de consultar por máquina (host).

| Componente       | Clave                  | Valor de Ejemplo | Tipo en InfluxDB  |
| :--------------- | :--------------------- | :--------------- | :---------------- |
| **Measurement**  | `rendimiento_servidor` | Fijo             | Fijo              |
| **TAG**          | `host_id`              | `servidor_01`    | String (Indexado) |
| **TAG**          | `entorno`              | `produccion`     | String (Indexado) |
| **FIELD**        | `cpu_percent`          | `45.8`           | Float (Medición)  |
| **FIELD**        | `ram_percent`          | `82.1`           | Float (Medición)  |
| **FIELD**        | `disk_percent`         | `65.4`           | Float (Medición)  |

#### 2\. Tareas de Implementación

Desarrolla el script Python principal (`agente_monitoreo.py`) para:

1.  **Inicialización:** configurar el cliente y la `WriteAPI` en **modo Batching** (asíncrono) para optimizar el rendimiento.
2.  **Bucle de lectura:** crear un bucle infinito que:
    a. Llame a `obtener_metricas_sistema("servidor_A")` **cada segundo**.
    b. Construya un nuevo objeto `Point` por cada lectura, respetando el modelo de datos anterior.
    c. Use la `write_api.write()` para enviar el punto al buffer.
3.  **Cierre:** Asegurarse de que el script llama a `write_api.close()` antes de salir (p.ej., en una [excepción de teclado](https://www.geeksforgeeks.org/python/how-to-catch-a-keyboardinterrupt-in-python/)) para vaciar cualquier punto que quede en el buffer.


```python
import influxdb_client
from influxdb_client import Point, WriteOptions
from influxdb_client.client.write_api import ASYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from urllib3.exceptions import NewConnectionError
import psutil
import time


# -------------------------------
# Función para obtener métricas
# -------------------------------

# Obtener estadísticas de uso
def obtener_metricas_sistema(host_id):
    # Uso de CPU (promedio de los últimos segundos)
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Uso de RAM
    mem = psutil.virtual_memory()
    ram_used_gb = round(mem.used / (1024**3), 2) # Conversión a GB
    ram_percent = mem.percent
    
    # Uso de disco (en el punto de montaje raíz)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    
    return {
        'host': host_id,
        'cpu_percent': cpu_usage,
        'ram_used_gb': ram_used_gb,
        'ram_percent': ram_percent,
        'disk_percent': disk_percent
    }

# -------------------------------
# Configuración de InfluxDB
# -------------------------------

INFLUX_URL = "http://influxdb2:8086"
INFLUX_TOKEN = "AdminToken123="
INFLUX_ORG = "docs"
bucket='PR0205'
print("--- Iniciando conexión a InfluxDB ---")

client = None
write_api = None
try:
    # 1. Inicializar el cliente
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )
    print("Conexión establecida")

    # Opciones asincrónas
    write_options= WriteOptions(
        batch_size=500, # Agrupa 500 puntos antes de enviarlos
        flush_interval=1000, # Espera 1 segundo antes de enviar los datos
        write_type=ASYNCHRONOUS
    )

    write_api = client.write_api(write_options=write_options)
    print("Agente de monitoreo iniciado. Presione Ctrl + C para detener")


    while True:
        metricas = obtener_metricas_sistema("servidor_A")
            
        punto = (
            Point("rendimiento_servidor")
            .tag("host_id", "servidor_01")
            .tag("entorno", "producción")
            .field("cpu_percent", metricas['cpu_percent'])
            .field("ram_used_gb", metricas['ram_used_gb'])
            .field("ram_percent", metricas['ram_percent'])
            .field("disk_percent", metricas['disk_percent'])
        )
    
        write_api.write(bucket=bucket, org=INFLUX_ORG, record=punto)
            
except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")

finally:
    write_api.close()
    print("Se ha salido exitosamente del programa")
```

