asignaturas = {
    "Matemáticas": ["Ana", "Carlos", "Luis", "María", "Jorge"],
    "Física": ["Elena", "Luis", "Juan", "Sofía"],
    "Programación": ["Ana", "Carlos", "Sofía", "Jorge", "Pedro"],
    "Historia": ["María", "Juan", "Elena", "Ana"],
    "Inglés": ["Carlos", "Sofía", "Jorge", "María"],
}

while True:
    print("1.- Listar estudiantes")
    print("2.- Matricular estudiante")
    print("3.- Dar de baja estudiante")
    print("4.- Salir")
    op = input ("Elige una opción:")

    match op:
        case "1":
            # Listar estudiantes matriculados en una asignatura
            asig = input("Dime el nombre de una asignatura:")
            # Opcion 1: print(asignaturas[asig]) 
            # Opcion 2: print(asignaturas.get(asig))
            alumnos =asignaturas.get(asig) # Opción 3
            print(f"Alumnos matriculados en {asig}")
            for a in alumnos:
                print(f" {a}")
        case "2":
            # Matricular estudiante en una asignatura
            alumno = input("Dime el nombre del alumno a matricular:")
            asig = input("Dime el nombre de la asignatura")
            if asig in asignaturas:
                asignaturas[asig].append(alumno) # Se añade el alumno a la asignatura creada
            else:
                asignaturas[asig] = [alumno] # Se crea la asignatura y se añade al alumno
        case "3":
            # Dar de baja a un estudiante en una asignatura
            alumno = input("Dime el alumno a dar de baja:")
            asig = input("Dime  la asignatura de la que vamos a darle de baja")
            asignaturas[asig].remove(alumno) # Se elimina al alumno de la asignatura
        case _:
            salir = True
