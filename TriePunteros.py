def _indice(c):
    if '0' <= c <= '9':
        return ord(c) - 48
    if 'a' <= c <= 'z':
        return ord(c) - 87
    return -1


def _simbolo(i):
    if i < 10:
        return chr(i + 48)
    return chr(i + 87)


def _validar(elemento):
    if not isinstance(elemento, str) or not 1 <= len(elemento) <= 20:
        raise ValueError("el elemento debe ser un string de longitud 1..20")
    for c in elemento:
        if _indice(c) == -1:
            raise ValueError("el elemento solo admite 'a'..'z' y '0'..'9'")


class _Nodo:
    __slots__ = ("hijos", "es_fin")

    def __init__(self):
        self.hijos = [None] * 36
        self.es_fin = False


class ConjuntoTriePunteros:

    def __init__(self):
        self.init()

    def init(self):
        self._raiz = _Nodo()

    def done(self):
        if self._raiz is None:
            return
        pila = [self._raiz]
        while pila:
            nodo = pila.pop()
            for i in range(36):
                hijo = nodo.hijos[i]
                if hijo is not None:
                    pila.append(hijo)
                    nodo.hijos[i] = None
        self._raiz = None

    def clear(self):
        self.done()
        self.init()

    def insert(self, elemento):
        _validar(elemento)
        nodo = self._raiz
        for c in elemento:
            i = _indice(c)
            if nodo.hijos[i] is None:
                nodo.hijos[i] = _Nodo()
            nodo = nodo.hijos[i]
        nodo.es_fin = True

    def delete(self, elemento):
        _validar(elemento)
        camino = []
        nodo = self._raiz
        for c in elemento:
            i = _indice(c)
            hijo = nodo.hijos[i]
            if hijo is None:
                return
            camino.append((nodo, i))
            nodo = hijo
        if not nodo.es_fin:
            return
        nodo.es_fin = False
        for padre, i in reversed(camino):
            actual = padre.hijos[i]
            if actual.es_fin or any(h is not None for h in actual.hijos):
                break
            padre.hijos[i] = None

    def member(self, elemento):
        _validar(elemento)
        nodo = self._raiz
        for c in elemento:
            nodo = nodo.hijos[_indice(c)]
            if nodo is None:
                return False
        return nodo.es_fin

    def _recorrer(self):
        pila = [(self._raiz, "")]
        while pila:
            nodo, prefijo = pila.pop()
            if nodo.es_fin:
                yield prefijo
            for i in range(35, -1, -1):
                hijo = nodo.hijos[i]
                if hijo is not None:
                    pila.append((hijo, prefijo + _simbolo(i)))

    def print(self):
        for elemento in self._recorrer():
            print(elemento)


def union(a, b):
    c = ConjuntoTriePunteros()
    for e in a._recorrer():
        c.insert(e)
    for e in b._recorrer():
        c.insert(e)
    return c


def intersection(a, b):
    c = ConjuntoTriePunteros()
    for e in a._recorrer():
        if b.member(e):
            c.insert(e)
    return c


def difference(a, b):
    c = ConjuntoTriePunteros()
    for e in a._recorrer():
        if not b.member(e):
            c.insert(e)
    return c


