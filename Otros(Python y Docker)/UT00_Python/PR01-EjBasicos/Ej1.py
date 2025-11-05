while True:
    a = input("Dime un número:")
    if ( a.isdigit() ):
        print("El número es válido")
        break
    else:
        print("El número no es válido")
