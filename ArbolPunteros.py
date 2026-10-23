


class NodoArbol:
    def __init__(self, elemento):
        self.elemento = elemento
        self.izquierdo = None
        self.derecho = None


class _IteradorInorden:


    def __init__(self, raiz):
        self.pila = []
        self._empujar_izquierdos(raiz)

    def _empujar_izquierdos(self, nodo):
        while nodo is not None:
            self.pila.append(nodo)
            nodo = nodo.izquierdo

    def empty(self):
        return len(self.pila) > 0

    def actual(self):
        return self.pila[-1].elemento

    def avanzar(self):
        nodo = self.pila.pop()
        self._empujar_izquierdos(nodo.derecho)


def _siguiente_resultado(it_a, it_b, modo):
    """Mezcla ordenada de dos recorridos inorden.
    Retorna el siguiente elemento del resultado según el modo, o None si ya no hay más."""
    while it_a.empty() or it_b.empty():
        a = it_a.actual() if it_a.empty() else None
        b = it_b.actual() if it_b.empty() else None

        if b is None or (a is not None and a < b):       # solo está en A
            it_a.avanzar()
            if modo == "Union" or modo == "Diferencia":
                return a
        elif a is None or b < a:                         # solo está en B
            it_b.avanzar()
            if modo == "Union":
                return b
        else:                                            # está en ambos
            it_a.avanzar()
            it_b.avanzar()
            if modo == "Union" or modo == "Interseccion":
                return a
    return None


def _construir(n, it_a, it_b, modo):
    """Construye un A.B.B. balanceado de n nodos consumiendo la mezcla en orden.
    La profundidad de la recursión es log n"""
    if n == 0:
        return None
    izquierdo = _construir(n // 2, it_a, it_b, modo)
    nodo = NodoArbol(_siguiente_resultado(it_a, it_b, modo))
    nodo.izquierdo = izquierdo
    nodo.derecho = _construir(n - n // 2 - 1, it_a, it_b, modo)
    return nodo


class ArbolPunteros:

    
    def __init__(self):
        self.raiz = None

    #  libera todos los nodos 
    def done(self):
        pila = []
        if self.raiz is not None:
            pila.append(self.raiz)
        while pila:
            nodo = pila.pop()
            if nodo.izquierdo is not None:
                pila.append(nodo.izquierdo)
            if nodo.derecho is not None:
                pila.append(nodo.derecho)
            nodo.izquierdo = None
            nodo.derecho = None
        self.raiz = None

    # Ejecuta y esconde el codigo de done
    def clear(self):
        self.done()

    
    # inserta un elemento al Arbol
    def insert(self, elemento):
        if self.raiz is None:
            self.raiz = NodoArbol(elemento)
            return

        actual = self.raiz
        while True:
            if elemento == actual.elemento:              # ya existe: sin efecto
                return
            if elemento < actual.elemento:
                if actual.izquierdo is None:
                    actual.izquierdo = NodoArbol(elemento)
                    return
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = NodoArbol(elemento)
                    return
                actual = actual.derecho

    # 
    def member(self, elemento):
        actual = self.raiz
        while actual is not None:
            if elemento == actual.elemento:
                return True
            if elemento < actual.elemento:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return False

    # borra un nodo 
    def delete(self, elemento):
        padre = None
        actual = self.raiz
        while actual is not None and actual.elemento != elemento:
            padre = actual
            actual = actual.izquierdo if elemento < actual.elemento else actual.derecho

        if actual is None:                               # no pertenece, no hace efecto
            return

        if actual.izquierdo is not None and actual.derecho is not None:
            # Dos hijos: se reemplaza por el mínimo del subárbol derecho
            padre_min = actual
            minimo = actual.derecho
            while minimo.izquierdo is not None:
                padre_min = minimo
                minimo = minimo.izquierdo
            actual.elemento = minimo.elemento
            padre, actual = padre_min, minimo            # ahora se elimina 'minimo' (tiene a lo sumo un hijo)

        hijo = actual.izquierdo if actual.izquierdo is not None else actual.derecho

        if padre is None:
            self.raiz = hijo
        elif padre.izquierdo is actual:
            padre.izquierdo = hijo
        else:
            padre.derecho = hijo

    # imprime el arbol en inorden salen los elementos ordenados 
    def print(self):
        iterador = _IteradorInorden(self.raiz)
        while iterador.empty():
            print(iterador.actual(), end=" ")
            iterador.avanzar()
        print()

    # Operaciones de conjunto 
    def _combinar(self, otro, modo):
        # en la primeta pasada cuenta cuántos elementos tendra el resultado
        n = 0
        it_a, it_b = _IteradorInorden(self.raiz), _IteradorInorden(otro.raiz)
        while _siguiente_resultado(it_a, it_b, modo) is not None:
            n += 1

        #  construye el resultado balanceado, sin lista auxiliar
        resultado = ArbolPunteros()
        it_a, it_b = _IteradorInorden(self.raiz), _IteradorInorden(otro.raiz)
        resultado.raiz = _construir(n, it_a, it_b, modo)
        return resultado

    def union(self, otro):
        return self._combinar(otro, "Union")

    def intersection(self, otro):
        return self._combinar(otro, "Interseccion")

    def difference(self, otro):
        return self._combinar(otro, "Diferencia")