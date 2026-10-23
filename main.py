
    
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

        print("\nEstructuras disponibles:")
        nombres_estructuras = {
            1: "Lista por punteros",
            2: "Lista por arreglos",
            3: "Tabla Hash",
            4: "ABB por punteros",
            5: "ABB por vector heap",
            6: "Trie por punteros",
            7: "Trie por arreglos"
        }

        for numero, nombre in nombres_estructuras.items():
            marca = " <-- ACTUAL" if numero == estructura else ""
            print(f"{numero} = {nombre}{marca}")

        opcion = leer_opcion("\nSeleccione una opcion: ", set(range(10)))

        if opcion == 0:
            print("Programa terminado.")
            return

        try:
            if opcion == 1:

