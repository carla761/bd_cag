# PR0203: Estructuras de datos avanzadas: hashes, sorted sets e hyperloglogs

```python
import redis
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
print("ping:", r.ping())
```
## Gestión de jugadores (Hash + Sorted Set)

**Función add_player(id, name, country, score)**

Crear el hash player:<id> con los campos:
- `name, country, games_played, score`
Insertar el jugador en el **sorted** set leaderboard con la puntuación inicial.

```python
player_key=f"player:{id}"

def add_player(id, name, country, score=0):
    player_data = {
        "name": name,
        "country": country,
        "score": score,
        "games_played": 0
    }

    r.hset(player_key, mapping=player_data)
    
    r.zadd("leaderboard", {id:score})

    print(f"[OK] Jugador añadido: {name} (ID: {id} con {score} puntos).")

```

```python
add_player(1, "Victor", "España")
add_player(2, "Jose", "Francia")
add_player(3, "Carlos", "Portugal")
```

**Función update_score(id, points)**

Incrementa el campo score del jugador, actualiza, su puntuación en el sorted set e incrementa el campo games_played.

```python
def update_score(id, points):
    
    if not r.exists(player_key):
        print(f"[Error] El jugador con ID {id}")
        return

    games_played = r.hget(player_key, "games_played")
    games_played_up = int(games_played)+1
    r.hset(player_key, "games_played", games_played_up)

    score= r.hget(player_key, "score")
    new_score= int(score) + points
    r.hset(player_key, "score", new_score)

    r.zadd("leaderboard", {id:new_score})

    print(f"[OK] Jugador {id} actualizo {points} puntos).")
    print(f"Nueva puntuacion{score}. partidos jugados")
```


```python
update_score(1,50)
update_score(2,75)
```

**Función player_info(id)**

Muestra todos los datos almacenados en el hash player:<id>.

```python
def player_info(id):
    return r.hgetall(player_key)

    if not info:
        print(f"No encontrado")
        return None
    print()
    for key,value in info.items():
        print(f" > {key.capitalize()}: {value}")
    return info
```

**Función show_top_players(n)**

Muestra los n mejores jugadores del ranking (leaderboard) con nombre, país y puntuación de cada jugador.

```python
def show_top_players(n):
    print(f"\n---TOP {n} JUGADORES")
    top = r.zrevrange("leaderboard", 0, n-1, withscores= True)

    if not top:
        print("Ranking vacio")
        return

    for i, (id,score) in enumerate(top):
        res=r.hgetall(player_key)

    print(f" #{i+1}: {res['name']}({res['country']})")
    print(f" ID :{id}| Puntuación:{int(res['score'])}")
    print("  "+ "-"*20)
    
```


```python
show_top_players(2)
```

## Registro de actividad diaria (HyperLogLog)

**Función register_login(player_id)**

Cada vez que un jugador inicia sesión, añadir su ID al HyperLogLog diario.

Por ejemplo, para la fecha actual:
  `key = f"unique:players:{fecha}"`
  `redis_client.pfadd(key, player_id)`

```python
from datetime import date

def get_date_key(date_obj):
    return f"unique:players:{date_obj.isoformat()}"

def register_login(player_id):
    today_key = get_date_key(date.today())

    changed = r.pfadd(today_key,player_id)

    if changed:
        print(f"[Login] {player_id} registrado por primera vez hoy")
    else:
        print(f"[Login] {player_id} ya habiainiciado sesion hoy")
```


```python
register_login(2)
```

**Función count_unique_logins(date)**

Obtiene el número aproximado de jugadores únicos que se conectaron ese día usando:
    `redis_client.pfcount(key)`

```python
def count_unique_logins(date_str):

    key = f"unique:players:{date_str}"
    
    count =r.pfcount(key)

    print(f"\n[Reporte Jugadores unicos(aprox.) el {date.str}: {count}")
    return count
```

**Función weekly_report(dates)**

Dada una lista de fechas, calcula el total aproximado de jugadores únicos en toda la semana con:
    `redis_client.pfmerge("unique:players:week", *keys)`
    `redis_client.pfcount("unique:players:week")`

```python
def weekly_report(dates_list):
    keys_to_merge = {f"unique:players:{d}" for d in dates_list}

    report_key ="unique:players:week_report" # Clave temporal

    r.pfmerge(report_key, *keys_to_merge)

    total_unique = r.pfcount(report_key)

    print(f"\n Reporte Semanal (Dias: {len(dates_list)})")
    print(f"Total de jugadores unicos(aprox.) {total_unique}")

    r.delete(report_key) # Borrar clave temporal

    return total_unique
```

```python
weekly_report(["2025-11-10","2025-11-11"])
```