dict1 = {
    "naranjas": 1.20,
    "manzanas": 2.50,
    "platanos": 3.10
}

dict2 = {
    "melón": 4.20,
    "naranjas": 1.90
}

out = dict1

for key, value in dict2.items():
    # key=melón     value=4.20
    
    if key in out:
        out[key] += value # Incrementa el valor
    else:
        out[key]= value # Añade el valor