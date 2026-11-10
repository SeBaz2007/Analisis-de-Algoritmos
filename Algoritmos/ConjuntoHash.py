class ConjuntoHash:

    def __init__(self, tamaño=10):
        self.tamaño = tamaño
        self.tabla = [[] for i in range(tamaño)]



    def hash(self, elemento):
        suma = 0

        for caracter in elemento:
            suma = suma * 31 + ord(caracter)

        return suma % self.tamaño


    def insert(self, elemento):
        posicion = self.hash(elemento)

        if elemento not in self.tabla[posicion]:
            self.tabla[posicion].append(elemento)


    def member(self, elemento):
        posicion = self.hash(elemento)

        if elemento in self.tabla[posicion]:
            return True

        return False

    def delete(self, elemento):
        posicion = self.hash(elemento)

        if elemento in self.tabla[posicion]:
            self.tabla[posicion].remove(elemento)

    def print(self):
        for i in range(self.tamaño):

            print(i, end=": ")

            for elemento in self.tabla[i]:
                print(elemento, end=" -> ")

            print("None")

    def clear(self):
        for i in range(self.tamaño):
            self.tabla[i] = []

    def union(self, otro):
        resultado = ConjuntoHash(self.tamaño)

        for lista in self.tabla:
            for elemento in lista:
                resultado.insert(elemento)

        for lista in otro.tabla:
            for elemento in lista:
                resultado.insert(elemento)

        return resultado


    def intersection(self, otro):
        resultado = ConjuntoHash(self.tamaño)

        for lista in self.tabla:
            for elemento in lista:

                if otro.member(elemento):
                    resultado.insert(elemento)

        return resultado


    def difference(self, otro):
        resultado = ConjuntoHash(self.tamaño)

        for lista in self.tabla:
            for elemento in lista:

                if not otro.member(elemento):
                    resultado.insert(elemento)

        return resultado