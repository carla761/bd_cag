## PR0201: Instalación y configuración de Hadoop en modo pseudo-distribuido
### 1. Configurar los adaptadores de red de la máquina virtual y asignar la IP solicitada.
Tenemos un adaptador NAT y otro solo anfitrión
![alt](./img/Ej1a.png)
Este es nuestro adaptador de red solo anfitrión
![alt](./img/Ej1b.png)
Asignamos nuestra ip(192.168.56.10) editando el archivo .yaml con el comando: `sudo nano /etc/netplan/50-cloud-init.yaml`
![alt](./img/ip-c.png)
### 2. Cambiar el nombre del host a hadoop-{iniciales}.
Cambiamos el nombre de host editando el archivo hostame con el comando: `sudo nano /etc/hostname`
![alt](./img/4.png)
### 3. Configurar acceso SSH mediante claves.
Creamos un par de claves publica-privada
![alt](./img/Ej3a.png)
Almacenamos la clave publica en un fickero llamado authorized_keys
![alt](./img/Ej3b.png)
Asignamos permisos al fichero authorized_keys para que solo pueda acceder a ella el usuario hadoop
![alt](./img/Ej3c.png)
Comprobar
![alt](./img/Ej3d.png)
### 5. Configurar Hadoop en modo pseudo-distribuido.
```nano .bashrc```
```. ./.bashrc```
![alt](./img/EJ5a.png)
```nano /opt/hadoop/etc/hadoop/hadoop-env.sh```
![alt](./img/EJ5c.png)
### 6. Iniciar los servicios de Hadoop y verificar su funcionamiento.
Iniciamos Hadoop con el comando `start-dfs.sh` y comprobamos con `jps`
![alt](./img/Ej7a.png)
Entramos en la interfaz web
![alt](./img/Ej7b.png)