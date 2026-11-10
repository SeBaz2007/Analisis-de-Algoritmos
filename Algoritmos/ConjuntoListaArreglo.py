class ConjuntoListaArreglo:
    def __init__(self):
        self.elementos = []

    def clear(self):
        self.elementos = []

    def done(self):
        self.clear()

    def insert(self, elemento):
        if len(self.elementos) == 0:
            self.elementos.append(elemento)
            return

        i = 0

        while i < len(self.elementos) and self.elementos[i] < elemento:
            i += 1

        if i < len(self.elementos) and self.elementos[i] == elemento:
            return

        self.elementos.insert(i, elemento)

    def member(self, elemento):
        for actual in self.elementos:
            if actual == elemento:
                return True

            if actual > elemento:
                return False

        return False

    def delete(self, elemento):
        if self.member(elemento):
            self.elementos.remove(elemento)

    def print(self):
        for elemento in self.elementos:
            print(elemento, end=" ")

        print()
        
    def union(self, otro):
        resultado = ConjuntoListaArreglo()

        for elemento in self.elementos:
            resultado.insert(elemento)

        for elemento in otro.elementos:
            resultado.insert(elemento)

        return resultado

    def intersection(self, otro):
        resultado = ConjuntoListaArreglo()

        for elemento in self.elementos:
            if otro.member(elemento):
                resultado.insert(elemento)

        return resultado

    def difference(self, otro):
        resultado = ConjuntoListaArreglo()

        for elemento in self.elementos:
            if not otro.member(elemento):
                resultado.insert(elemento)

        return resultado