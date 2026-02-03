# PR0302: Lectura avanzada de datos de archivos

## Objetivo de la Práctica

Esta práctica es una revisión de la anterior donde aumentamos el nivel de dificultad ya que los archivos de origen tienen sus *peculiaridades*.

Nuevamente tienes que leer datos de tres fuentes diferentes (CSV, Excel y JSON) y volcar el resultado a un archivo CSV.



```python
import pandas as pd
```

### Ventas_Norte (CSV)

1. **Norte ([`ventas_norte_v2.csv`](./data/ventas_norte_v2.csv)):** 

- Formato CSV delimitado por punto y coma (`;`).
- El campo `Direccion_Envio` contiene comas reales (ej: "Calle Mayor, 12"). Debes asegurarte de que Pandas no rompa las filas al leerlo.
- El campo `Total_Factura` viene como texto con símbolos de moneda (ej: "$1,200.50"). Deberás limpiarlo y convertirlo a `float`.



```python
df_norte = pd.read_csv(
    "ventas_norte_v2.csv",
    sep=";",
    quotechar='"'
    )
df_norte
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID_Pedido</th>
      <th>Fecha_Transaccion</th>
      <th>Cliente_Nombre</th>
      <th>Direccion_Envio</th>
      <th>Producto</th>
      <th>Unidades</th>
      <th>Precio_Unitario</th>
      <th>Total_Factura</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>N-1000</td>
      <td>2023-05-10 03:00:00</td>
      <td>Usuario_0</td>
      <td>Gran Vía, 49, Piso 4</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>970</td>
      <td>$970.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>N-1001</td>
      <td>2023-06-18 09:00:00</td>
      <td>Usuario_1</td>
      <td>Av. Libertad, 30, Piso 4</td>
      <td>Mouse Ergonómico</td>
      <td>4</td>
      <td>927</td>
      <td>$3708.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>N-1002</td>
      <td>2023-03-10 05:00:00</td>
      <td>Usuario_2</td>
      <td>Av. Libertad, 98, Piso 2</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1410</td>
      <td>$2820.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>N-1003</td>
      <td>2023-05-10 03:00:00</td>
      <td>Usuario_3</td>
      <td>Paseo Gracia, 94, Piso 7</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>1269</td>
      <td>$2538.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>N-1004</td>
      <td>2023-02-25 17:00:00</td>
      <td>Usuario_4</td>
      <td>Calle Mayor, 80, Piso 8</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>454</td>
      <td>$908.00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>145</th>
      <td>N-1145</td>
      <td>2023-04-17 10:00:00</td>
      <td>Usuario_145</td>
      <td>Paseo Gracia, 99, Piso 10</td>
      <td>Teclado Mecánico</td>
      <td>4</td>
      <td>1051</td>
      <td>$4204.00</td>
    </tr>
    <tr>
      <th>146</th>
      <td>N-1146</td>
      <td>2023-04-08 00:00:00</td>
      <td>Usuario_146</td>
      <td>Paseo Gracia, 64, Piso 4</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1229</td>
      <td>$2458.00</td>
    </tr>
    <tr>
      <th>147</th>
      <td>N-1147</td>
      <td>2023-02-01 22:00:00</td>
      <td>Usuario_147</td>
      <td>Calle Mayor, 81, Piso 1</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>1040</td>
      <td>$1040.00</td>
    </tr>
    <tr>
      <th>148</th>
      <td>N-1148</td>
      <td>2023-06-13 03:00:00</td>
      <td>Usuario_148</td>
      <td>Calle Mayor, 56, Piso 1</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>297</td>
      <td>$297.00</td>
    </tr>
    <tr>
      <th>149</th>
      <td>N-1149</td>
      <td>2023-02-24 01:00:00</td>
      <td>Usuario_149</td>
      <td>Paseo Gracia, 25, Piso 1</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>909</td>
      <td>$909.00</td>
    </tr>
  </tbody>
</table>
<p>150 rows × 8 columns</p>
</div>




```python
df_norte["Total_Factura"] = df_norte["Total_Factura"].str.replace("$","",regex=False)
```


```python
df_norte["Total_Factura"] = df_norte["Total_Factura"].astype(float)
```


```python
df_norte.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID_Pedido</th>
      <th>Fecha_Transaccion</th>
      <th>Cliente_Nombre</th>
      <th>Direccion_Envio</th>
      <th>Producto</th>
      <th>Unidades</th>
      <th>Precio_Unitario</th>
      <th>Total_Factura</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>N-1000</td>
      <td>2023-05-10 03:00:00</td>
      <td>Usuario_0</td>
      <td>Gran Vía, 49, Piso 4</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>970</td>
      <td>970.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>N-1001</td>
      <td>2023-06-18 09:00:00</td>
      <td>Usuario_1</td>
      <td>Av. Libertad, 30, Piso 4</td>
      <td>Mouse Ergonómico</td>
      <td>4</td>
      <td>927</td>
      <td>3708.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>N-1002</td>
      <td>2023-03-10 05:00:00</td>
      <td>Usuario_2</td>
      <td>Av. Libertad, 98, Piso 2</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1410</td>
      <td>2820.0</td>
    </tr>
  </tbody>
</table>
</div>



### Ventas Sur(Excel)
2. **Sur ([`ventas_sur.xlsx`](./data/ventas_sur_v2.xlsx)):**

- Archivo Excel con **múltiples hojas** (`Q1_2023`, `Q2_2023`).
- Contiene columnas booleanas (`Es_Cliente_Corporativo`) y de estado (`Estado_Envio`) que deben conservarse.
- Debes calcular una columna `Total` que no existe explícitamente (`Precio_Base` * `Cantidad` * (1 - `Descuento_Aplicado`)).



```python
!pip install openpyxl
```

    Requirement already satisfied: openpyxl in /opt/conda/lib/python3.11/site-packages (3.1.2)
    Requirement already satisfied: et-xmlfile in /opt/conda/lib/python3.11/site-packages (from openpyxl) (1.1.0)



```python
df_list = pd.read_excel(
    './ventas_sur_v2.xlsx',
    sheet_name=None,
    header=0,
    usecols='A:H',
    names = ['Id', 'Fecha', 'Articulo', 'Cantidad', 'Precio_Base','Descuento',"Es_Cliente","Estado_Envio"],
    parse_dates = ['Fecha'],
    engine='openpyxl'
)
```


```python
df_sur = pd.concat(
    df_list.values(), # Values nos da los datos del diccionario 
    ignore_index=True # Ignora los indices 
)
df_sur.head(3)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>Fecha</th>
      <th>Articulo</th>
      <th>Cantidad</th>
      <th>Precio_Base</th>
      <th>Descuento</th>
      <th>Es_Cliente</th>
      <th>Estado_Envio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>S-5000</td>
      <td>2023-02-11 00:00:00</td>
      <td>Webcam HD</td>
      <td>9</td>
      <td>425.12</td>
      <td>0.2</td>
      <td>False</td>
      <td>Enviado</td>
    </tr>
    <tr>
      <th>1</th>
      <td>S-5001</td>
      <td>2023-02-03 12:00:00</td>
      <td>Teclado Mecánico</td>
      <td>8</td>
      <td>599.60</td>
      <td>0.0</td>
      <td>True</td>
      <td>Devuelto</td>
    </tr>
    <tr>
      <th>2</th>
      <td>S-5002</td>
      <td>2023-04-06 07:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>6</td>
      <td>971.36</td>
      <td>0.0</td>
      <td>False</td>
      <td>Completado</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_sur["Es_Cliente"] = df_sur["Es_Cliente"].astype(bool) 
df_sur["Estado_Envio"] = df_sur["Estado_Envio"].astype("category")
```


```python
df_sur["Total"] = df_sur["Precio_Base"] * df_sur["Cantidad"] * (1 - df_sur["Descuento"])
```


```python
df_sur
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>Fecha</th>
      <th>Articulo</th>
      <th>Cantidad</th>
      <th>Precio_Base</th>
      <th>Descuento</th>
      <th>Es_Cliente</th>
      <th>Estado_Envio</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>S-5000</td>
      <td>2023-02-11 00:00:00</td>
      <td>Webcam HD</td>
      <td>9</td>
      <td>425.12</td>
      <td>0.20</td>
      <td>False</td>
      <td>Enviado</td>
      <td>3060.864</td>
    </tr>
    <tr>
      <th>1</th>
      <td>S-5001</td>
      <td>2023-02-03 12:00:00</td>
      <td>Teclado Mecánico</td>
      <td>8</td>
      <td>599.60</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>4796.800</td>
    </tr>
    <tr>
      <th>2</th>
      <td>S-5002</td>
      <td>2023-04-06 07:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>6</td>
      <td>971.36</td>
      <td>0.00</td>
      <td>False</td>
      <td>Completado</td>
      <td>5828.160</td>
    </tr>
    <tr>
      <th>3</th>
      <td>S-5003</td>
      <td>2023-04-02 05:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>799.66</td>
      <td>0.10</td>
      <td>True</td>
      <td>Pendiente</td>
      <td>719.694</td>
    </tr>
    <tr>
      <th>4</th>
      <td>S-5004</td>
      <td>2023-06-17 12:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>2</td>
      <td>619.99</td>
      <td>0.05</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>1177.981</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>155</th>
      <td>S-5075</td>
      <td>2023-05-17 22:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1150.01</td>
      <td>0.10</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2070.018</td>
    </tr>
    <tr>
      <th>156</th>
      <td>S-5076</td>
      <td>2023-01-29 13:00:00</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>874.12</td>
      <td>0.10</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>786.708</td>
    </tr>
    <tr>
      <th>157</th>
      <td>S-5077</td>
      <td>2023-06-09 11:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>145.92</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>145.920</td>
    </tr>
    <tr>
      <th>158</th>
      <td>S-5078</td>
      <td>2023-02-07 13:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1152.24</td>
      <td>0.00</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2304.480</td>
    </tr>
    <tr>
      <th>159</th>
      <td>S-5079</td>
      <td>2023-05-01 11:00:00</td>
      <td>Docking Station</td>
      <td>7</td>
      <td>261.88</td>
      <td>0.10</td>
      <td>True</td>
      <td>Enviado</td>
      <td>1649.844</td>
    </tr>
  </tbody>
</table>
<p>160 rows × 9 columns</p>
</div>



Ventas Este (Json)
3. **Este ([`ventas_este.json`](./data/ventas_este_v2.json)):**

- JSON de con varios niveles de anidamiento
- La información útil está sepultada bajo `data -> payload -> transaccion`.
- Debes extraer:
   - ID del registro.
   - Fecha.
   - Ciudad del comprador.
   - Nombre del producto.
   - Cantidad.
   - Precio de lista y el monto del IVA (que está en un sub-diccionario).
- Debes descartar metadatos técnicos (`latency_ms`, `source_system`).



```python
import json
import pandas as pd

with open('./ventas_este_v2.json') as f:
    data = json.load(f)

df_este = pd.json_normalize(data)

# Eliminamos metadatos técnicos
df_este = df_este.drop(columns=[c for c in df_este.columns if 'metadata' in c], errors='ignore')

df_este

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data.id_registro</th>
      <th>data.payload.fecha_evento</th>
      <th>data.payload.comprador.perfil.id_usuario</th>
      <th>data.payload.comprador.perfil.tipo_suscripcion</th>
      <th>data.payload.comprador.ubicacion.ciudad</th>
      <th>data.payload.comprador.ubicacion.codigo_postal</th>
      <th>data.payload.transaccion.detalles_producto.sku</th>
      <th>data.payload.transaccion.detalles_producto.nombre_comercial</th>
      <th>data.payload.transaccion.detalles_producto.precio_lista</th>
      <th>data.payload.transaccion.detalles_producto.impuestos.iva_percent</th>
      <th>data.payload.transaccion.detalles_producto.impuestos.monto_iva</th>
      <th>data.payload.transaccion.cantidad_comprada</th>
      <th>data.payload.transaccion.metodo_pago</th>
      <th>data.payload.transaccion.tags</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>E-8000</td>
      <td>2023-06-29 00:00:00</td>
      <td>USR_442</td>
      <td>Gold</td>
      <td>Sevilla</td>
      <td>51213</td>
      <td>G6YATHNF</td>
      <td>Monitor 4K</td>
      <td>503</td>
      <td>21</td>
      <td>105.63</td>
      <td>1</td>
      <td>Bizum</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>E-8001</td>
      <td>2023-04-12 00:00:00</td>
      <td>USR_205</td>
      <td>Free</td>
      <td>Sevilla</td>
      <td>14665</td>
      <td>THC8MFC5</td>
      <td>Webcam HD</td>
      <td>1122</td>
      <td>21</td>
      <td>235.62</td>
      <td>1</td>
      <td>Tarjeta Crédito</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>2</th>
      <td>E-8002</td>
      <td>2023-04-20 00:00:00</td>
      <td>USR_214</td>
      <td>Premium</td>
      <td>Sevilla</td>
      <td>59843</td>
      <td>6IFCBHMJ</td>
      <td>Webcam HD</td>
      <td>994</td>
      <td>21</td>
      <td>208.74</td>
      <td>2</td>
      <td>Tarjeta Crédito</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>3</th>
      <td>E-8003</td>
      <td>2023-04-14 00:00:00</td>
      <td>USR_422</td>
      <td>Gold</td>
      <td>Madrid</td>
      <td>56165</td>
      <td>PXC40RUN</td>
      <td>Webcam HD</td>
      <td>1255</td>
      <td>21</td>
      <td>263.55</td>
      <td>2</td>
      <td>Transferencia</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E-8004</td>
      <td>2023-01-03 00:00:00</td>
      <td>USR_329</td>
      <td>Premium</td>
      <td>Sevilla</td>
      <td>78884</td>
      <td>3JI7HLD5</td>
      <td>Monitor 4K</td>
      <td>1458</td>
      <td>21</td>
      <td>306.18</td>
      <td>2</td>
      <td>PayPal</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>115</th>
      <td>E-8115</td>
      <td>2023-04-05 00:00:00</td>
      <td>USR_769</td>
      <td>Free</td>
      <td>Valencia</td>
      <td>31391</td>
      <td>HNQDGL0Q</td>
      <td>Monitor 4K</td>
      <td>829</td>
      <td>21</td>
      <td>174.09</td>
      <td>1</td>
      <td>PayPal</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>116</th>
      <td>E-8116</td>
      <td>2023-04-23 00:00:00</td>
      <td>USR_443</td>
      <td>Gold</td>
      <td>Valencia</td>
      <td>19586</td>
      <td>4PNJTECY</td>
      <td>Laptop Gamer</td>
      <td>858</td>
      <td>21</td>
      <td>180.18</td>
      <td>2</td>
      <td>PayPal</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>117</th>
      <td>E-8117</td>
      <td>2023-06-03 00:00:00</td>
      <td>USR_172</td>
      <td>Premium</td>
      <td>Sevilla</td>
      <td>70707</td>
      <td>W1M7CCSI</td>
      <td>Webcam HD</td>
      <td>637</td>
      <td>21</td>
      <td>133.77</td>
      <td>2</td>
      <td>Tarjeta Crédito</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>118</th>
      <td>E-8118</td>
      <td>2023-02-24 00:00:00</td>
      <td>USR_332</td>
      <td>Premium</td>
      <td>Valencia</td>
      <td>40898</td>
      <td>VXFXQUKX</td>
      <td>Monitor 4K</td>
      <td>502</td>
      <td>21</td>
      <td>105.42</td>
      <td>2</td>
      <td>Transferencia</td>
      <td>[lujo, envio_gratis]</td>
    </tr>
    <tr>
      <th>119</th>
      <td>E-8119</td>
      <td>2023-01-08 00:00:00</td>
      <td>USR_176</td>
      <td>Free</td>
      <td>Madrid</td>
      <td>80962</td>
      <td>3HPQ0U08</td>
      <td>Mouse Ergonómico</td>
      <td>306</td>
      <td>21</td>
      <td>64.26</td>
      <td>1</td>
      <td>Transferencia</td>
      <td>[oferta, digital]</td>
    </tr>
  </tbody>
</table>
<p>120 rows × 14 columns</p>
</div>



### Df Final
El DataFrame final debe tener **exactamente** estas columnas estandarizadas:

- `id_transaccion`
- `fecha`
- `region`
- `producto`
- `cantidad`
- `total_venta`


```python
df_norte.rename(columns={
    "ID_Pedido": "id_transaccion",
    "Fecha_Transaccion": "fecha",
    "Producto": "producto",
    "Unidades": "cantidad",
    "Total_Factura": "total_venta"
}, inplace=True)

df_norte["region"] = "Norte"

df_norte = df_norte[["id_transaccion", "fecha", "region", "producto", "cantidad", "total_venta"]]

```


```python
df_sur.rename(columns={
    "Id": "id_transaccion",
    "Fecha": "fecha",
    "Articulo": "producto",
    "Cantidad": "cantidad",
    "Total": "total_venta"
}, inplace=True)

df_sur["region"] = "Sur"

df_sur = df_sur[["id_transaccion", "fecha", "region", "producto", "cantidad", "total_venta"]]

```


```python
df_este.rename(columns={
    "data.id_registro": "id_transaccion",
    "data.payload.fecha_evento": "fecha",
    "data.payload.transaccion.detalles_producto.nombre_comercial": "producto",
    "data.payload.transaccion.cantidad_comprada": "cantidad"
}, inplace=True)

df_este["total_venta"] = (
    df_este["data.payload.transaccion.detalles_producto.precio_lista"] +
    df_este["data.payload.transaccion.detalles_producto.impuestos.monto_iva"]
)

df_este["region"] = "Este"

df_este = df_este[["id_transaccion", "fecha", "region", "producto", "cantidad", "total_venta"]]

```


```python
df_final = pd.concat([df_norte, df_sur, df_este], ignore_index=True)
df_final
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_transaccion</th>
      <th>fecha</th>
      <th>region</th>
      <th>producto</th>
      <th>cantidad</th>
      <th>total_venta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>N-1000</td>
      <td>2023-05-10 03:00:00</td>
      <td>Norte</td>
      <td>Laptop Gamer</td>
      <td>1</td>
      <td>970.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>N-1001</td>
      <td>2023-06-18 09:00:00</td>
      <td>Norte</td>
      <td>Mouse Ergonómico</td>
      <td>4</td>
      <td>3708.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>N-1002</td>
      <td>2023-03-10 05:00:00</td>
      <td>Norte</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>2820.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>N-1003</td>
      <td>2023-05-10 03:00:00</td>
      <td>Norte</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>2538.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>N-1004</td>
      <td>2023-02-25 17:00:00</td>
      <td>Norte</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>908.00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>425</th>
      <td>E-8115</td>
      <td>2023-04-05 00:00:00</td>
      <td>Este</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>1003.09</td>
    </tr>
    <tr>
      <th>426</th>
      <td>E-8116</td>
      <td>2023-04-23 00:00:00</td>
      <td>Este</td>
      <td>Laptop Gamer</td>
      <td>2</td>
      <td>1038.18</td>
    </tr>
    <tr>
      <th>427</th>
      <td>E-8117</td>
      <td>2023-06-03 00:00:00</td>
      <td>Este</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>770.77</td>
    </tr>
    <tr>
      <th>428</th>
      <td>E-8118</td>
      <td>2023-02-24 00:00:00</td>
      <td>Este</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>607.42</td>
    </tr>
    <tr>
      <th>429</th>
      <td>E-8119</td>
      <td>2023-01-08 00:00:00</td>
      <td>Este</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>370.26</td>
    </tr>
  </tbody>
</table>
<p>430 rows × 6 columns</p>
</div>




```python

```
