dict = {
    "Matemáticas": "Victor",
    "Lengua": "Luis",
    "Historia": "Ana",
}

out = {} # Diccionario vacio

for key, value in dict.items(): # Separo en dos variables los valores
    # Invertir el diccionario
    out[value] = key 
    # Forma normal : out[key] = value
print(out)