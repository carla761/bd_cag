cadena = "¿Esto es una-prueba?"
temp = [ letra for letra in cadena if letra.isalnum()]
res = "".join(temp)
print(res)