
class ArbolHeap:

    def __init__(self):
        self.vector = []


    def done(self):
        self.vector.clear()


    def clear(self):
        self.vector.clear()


    def validar(self, elemento):
        if not isinstance(elemento, str): #comprueba que el elemento sea un string
            raise TypeError("El elemento debe ser un string")

        if len(elemento) > 20:
            raise ValueError("Maximo 20 caracteres")

        if any(not ('a' <= c <= 'z' or '0' <= c <= '9')
            for c in elemento):
            raise ValueError("Solo se permiten letras minusculas y digitos")


    def member(self, elemento):
        self.validar(elemento)
        return self._buscar(0, elemento)


    def _buscar(self, i, elemento):
        if i >= len(self.vector) or self.vector[i] is None:
            return False

        actual = self.vector[i]

        if elemento == actual:
            return True

        if elemento < actual:
            return self._buscar(2 * i + 1, elemento)

        return self._buscar(2 * i + 2, elemento)


    def insert(self, elemento):
        self.validar(elemento)
        self._insertar(0, elemento)


    def _insertar(self, i, elemento):
        if i >= len(self.vector):
            self.vector.extend(
                [None] * (i + 1 - len(self.vector))
            )

        if self.vector[i] is None:
            self.vector[i] = elemento
            return

        if elemento == self.vector[i]:
            return

        if elemento < self.vector[i]:
            self._insertar(2 * i + 1, elemento)
        else:
            self._insertar(2 * i + 2, elemento)


    def delete(self, elemento):
        self.validar(elemento)
        self._eliminar(0, elemento)

        while self.vector and self.vector[-1] is None:
            self.vector.pop()


    def _eliminar(self, i, elemento):
        if i >= len(self.vector) or self.vector[i] is None:
            return

        actual = self.vector[i]

        if elemento < actual:
            self._eliminar(2 * i + 1, elemento)

        elif elemento > actual:
            self._eliminar(2 * i + 2, elemento)

        else:
            izq = 2 * i + 1
            der = 2 * i + 2

            tiene_izq = (
                izq < len(self.vector)
                and self.vector[izq] is not None
            )
            tiene_der = (
                der < len(self.vector)
                and self.vector[der] is not None
            )

            # Caso 1: no tiene hijos
            if not tiene_izq and not tiene_der:
                self.vector[i] = None

            # Caso 2: solo tiene hijo derecho
            elif not tiene_izq:
                sucesor = self._minimo(der)
                self.vector[i] = sucesor
                self._eliminar(der, sucesor)

            # Caso 3: solo tiene hijo izquierdo
            elif not tiene_der:
                sucesor = self._maximo(izq)
                self.vector[i] = sucesor
                self._eliminar(izq, sucesor)

            # Caso 4: tiene ambos hijos
            else:
                sucesor = self._minimo(der)
                self.vector[i] = sucesor
                self._eliminar(der, sucesor)


    def _minimo(self, i):
        while True:
            izq = 2 * i + 1

            if (izq >= len(self.vector)
                    or self.vector[izq] is None):
                return self.vector[i]

            i = izq


    def _maximo(self, i):
        while True:
            der = 2 * i + 2

            if (der >= len(self.vector)
                    or self.vector[der] is None):
                return self.vector[i]

            i = der


    def print(self):
        elementos = []
        self._recorrer(0, elementos)
        print("{" + ", ".join(elementos) + "}")


    def _recorrer(self, i, elementos):
        if i >= len(self.vector) or self.vector[i] is None:
            return

        self._recorrer(2 * i + 1, elementos)
        elementos.append(self.vector[i])
        self._recorrer(2 * i + 2, elementos)


    def union(A, B):
        resultado = ArbolHeap()

        for elemento in A._elementos():
            resultado.insert(elemento)

        for elemento in B._elementos():
            resultado.insert(elemento)

        return resultado


    def intersection(A, B):
        resultado = ArbolHeap()

        for elemento in A._elementos():
            if B.member(elemento):
                resultado.insert(elemento)

        return resultado


    def difference(A, B):
        resultado = ArbolHeap()

        for elemento in A._elementos():
            if not B.member(elemento):
                resultado.insert(elemento)

        return resultado


    def _elementos(self):
        elementos = []
        self._recorrer(0, elementos)
        return elementos
