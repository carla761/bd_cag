cadena = "Esto es una-prueba"
cadena = cadena.title()
cadena = cadena.replace(" ","").replace("-","")
cadena = cadena[0].lower() + cadena[1:]
print(cadena)
