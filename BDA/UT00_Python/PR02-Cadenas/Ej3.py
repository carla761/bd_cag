a=input("Dime una cadena:")
b="".join(a.split())

if (b==b[::-1]):
    print("Es un palíndromo") 
else:
    print("No es un palindromo")