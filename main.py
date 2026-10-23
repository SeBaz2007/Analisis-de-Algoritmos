from ConjuntoHash import ConjuntoHash
from ConjuntoListaArreglo import ConjuntoListaArreglo
from ConjuntoListaPunteros import ConjuntoListaPunteros
from ArbolPunteros import ArbolPunteros
from ArbolHeap import ArbolHeap
from TriePunteros import ConjuntoTriePunteros
from TrieArreglos import TrieArreglos


def mostrar_menu():
    print("\n========== MENU ==========")
    print("1. Insertar")
    print("2. Eliminar")
    print("3. Buscar")
    print("4. Imprimir")
    print("5. Union")
    print("6. Intersection")
    print("7. Difference")
    print("8. Limpiar")
    print("9. Cambiar estructura")
    print("0. Salir")
    print("==========================")


def leer_opcion(mensaje, opciones_validas):
    #Lee una opcion y vuelve a preguntar hasta recibir una valida
    while True:
        entrada = input(mensaje).strip()

        try:
            opcion = int(entrada)
        except ValueError:
            print("Error: debe ingresar un numero entero. Intente nuevamente.")
            continue

        if opcion not in opciones_validas:
            opciones = ", ".join(str(x) for x in sorted(opciones_validas))
            print(f"Error: opcion invalida. Ingrese una de estas opciones: {opciones}.")
            continue

        return opcion


def leer_conjunto(mensaje):
    #Solo acepta A o B
    while True:
        conjunto = input(mensaje).strip().upper()

        if conjunto in ("A", "B"):
            return conjunto

        print("Error: debe escribir A o B. Intente nuevamente.")


def leer_elemento():
    #Evita aceptar una entrada vacia como elemento
    while True:
        elemento = input("Elemento: ").strip()

        if elemento:
            return elemento

        print("Error: el elemento no puede estar vacio. Intente nuevamente.")


def main():
    A = ConjuntoHash(10)
    B = ConjuntoHash(10)
    estructura = 3

    while True:
        mostrar_menu()

        print("\nEstructura actual:", estructura)
        print("1 = Lista por punteros")
        print("2 = Lista por arreglos")
        print("3 = Tabla Hash")

        opcion = leer_opcion("\nSeleccione una opcion: ", set(range(10)))

        if opcion == 0:
            print("Programa terminado.")
            return

        try:
            if opcion == 1:
                conjunto = leer_conjunto("¿Conjunto A o B? ")
                elemento = leer_elemento()

                if conjunto == "A":
                    A.insert(elemento)
                else:
                    B.insert(elemento)

                print("Operacion de insercion completada.")

            elif opcion == 2:
                conjunto = leer_conjunto("¿Conjunto A o B? ")
                elemento = leer_elemento()

                if conjunto == "A":
                    A.delete(elemento)
                else:
                    B.delete(elemento)

                print("Operacion de eliminacion completada.")

            elif opcion == 3:
                conjunto = leer_conjunto("¿Conjunto A o B? ")
                elemento = leer_elemento()

                if conjunto == "A":
                    print(A.member(elemento))
                else:
                    print(B.member(elemento))

            elif opcion == 4:
                print("\nConjunto A:")
                A.print()
                print("Conjunto B:")
                B.print()

            elif opcion == 5:
                resultado = A.union(B)
                print("\nA UNION B:")
                resultado.print()

            elif opcion == 6:
                resultado = A.intersection(B)
                print("\nA INTERSECTION B:")
                resultado.print()

            elif opcion == 7:
                resultado = A.difference(B)
                print("\nA DIFFERENCE B:")
                resultado.print()

            elif opcion == 8:
                conjunto = leer_conjunto("¿Limpiar A o B? ")

                if conjunto == "A":
                    A.clear()
                else:
                    B.clear()

                print(f"Conjunto {conjunto} limpiado.")

            elif opcion == 9:
                nueva_estructura = leer_opcion(
                    "1. Lista por punteros\n"
                    "2. Lista por arreglos\n"
                    "3. Tabla Hash\n"
                    "4. ABB por punteros\n"
                    "5. ABB por vector heap\n"
                    "6. Trie por punteros\n"
                    "7. Trie por arreglos\n"
                    "Seleccione: ",
                    {1, 2, 3, 4, 5, 6, 7},
                )

                # Se crean los conjuntos nuevos solo despues de validar la opcion.
                if nueva_estructura == 1:
                    nuevo_A = ConjuntoListaPunteros()
                    nuevo_B = ConjuntoListaPunteros()
                elif nueva_estructura == 2:
                    nuevo_A = ConjuntoListaArreglo()
                    nuevo_B = ConjuntoListaArreglo()
                elif nueva_estructura == 3:
                    nuevo_A = ConjuntoHash(10)
                    nuevo_B = ConjuntoHash(10)
                elif nueva_estructura == 4:
                    nuevo_A = ArbolPunteros()
                    nuevo_B = ArbolPunteros()
                elif nueva_estructura == 5:
                    nuevo_A = ArbolHeap()
                    nuevo_B = ArbolHeap()
                elif nueva_estructura == 6:
                    nuevo_A = ConjuntoTriePunteros()
                    nuevo_B = ConjuntoTriePunteros()
                elif nueva_estructura == 7:
                    nuevo_A = TrieArreglos()
                    nuevo_B = TrieArreglos()
                else:
                    print("Opcion invalida. No se cambio la estructura.")
                    continue

                A = nuevo_A
                B = nuevo_B
                estructura = nueva_estructura
                print("Estructura cambiada. Los conjuntos empiezan vacios.")

        except Exception as error:
            # Evita que un error inesperado durante una operacion y se cierre el programa.
            print(f"Error al realizar la operacion: {error}")
            print("Puede intentarlo nuevamente desde el menu.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada cancelada. Programa terminado.")
