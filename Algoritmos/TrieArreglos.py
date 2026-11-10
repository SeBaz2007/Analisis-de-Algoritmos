tamAlfanumericos = 36
tamMaximo = 20


def indice(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    return 26 + (ord(c) - ord('0'))


def caracter(i):
    if i < 26:
        return chr(ord('a') + i)
    return chr(ord('0') + (i - 26))


def es_valido(elemento):
    if not isinstance(elemento, str):
        return False
    if not (1 <= len(elemento) <= tamMaximo):
        return False
    for c in elemento:
        if not (('a' <= c <= 'z') or ('0' <= c <= '9')):
            return False
    return True


class Nodo:
    def __init__(self):
        self.hijos = [None] * tamAlfanumericos
        self.es_final = False


def _nodoVacio(nodo):
    if nodo.es_final:
        return False
    for h in nodo.hijos:
        if h is not None:
            return False
    return True


def _copia(nodo):
    if nodo is None:
        return None
    new = Nodo()
    new.es_final = nodo.es_final
    for i in range(tamAlfanumericos):
        new.hijos[i] = _copia(nodo.hijos[i])
    return new


def _union(a, b):
    if a is None:
        return _copia(b)
    if b is None:
        return _copia(a)
    new = Nodo()
    new.es_final = a.es_final or b.es_final
    for i in range(tamAlfanumericos):
        new.hijos[i] = _union(a.hijos[i], b.hijos[i])
    return new


def _interseccion(a, b):
    if a is None or b is None:
        return None
    new = Nodo()
    new.es_final = a.es_final and b.es_final
    for i in range(tamAlfanumericos):
        new.hijos[i] = _interseccion(a.hijos[i], b.hijos[i])
    return None if _nodoVacio(new) else new


def _difference(a, b):
    if a is None:
        return None
    if b is None:
        return _copia(a)
    new = Nodo()
    new.es_final = a.es_final and not b.es_final
    for i in range(tamAlfanumericos):
        new.hijos[i] = _difference(a.hijos[i], b.hijos[i])
    return None if _nodoVacio(new) else new


class TrieArreglos:

    
    def __init__(self):
        self.raiz = Nodo()


    def done(self):
        self.raiz = None


    def clear(self):
        self.raiz = Nodo()


    def insert(self, elemento):
        if not es_valido(elemento):
            raise ValueError(f"elemento invalido: {elemento}")
        actual = self.raiz
        for c in elemento:
            i = indice(c)
            if actual.hijos[i] is None:
                actual.hijos[i] = Nodo()
            actual = actual.hijos[i]
        actual.es_final = True


    def member(self, elemento):
        if not es_valido(elemento):
            return False
        actual = self.raiz
        for c in elemento:
            actual = actual.hijos[indice(c)]
            if actual is None:
                return False
        return actual.es_final 


    def delete(self, elemento):
        if not es_valido(elemento):
            return
        self._delete(self.raiz, elemento, 0)


    def _delete(self, nodo, elemento, pos):
        if pos == len(elemento):
            nodo.es_final = False
            return _nodoVacio(nodo)
        i = indice(elemento[pos])
        hijo = nodo.hijos[i]
        if hijo is None:
            return False
        if self._delete(hijo, elemento, pos + 1):
            nodo.hijos[i] = None
        return _nodoVacio(nodo) and nodo is not self.raiz


    def print(self):
        elementos = []
        self._run(self.raiz, [], elementos)
        print("{" + ", ".join(elementos) + "}")


    def _run(self, nodo, prefijo, salida):
        if nodo.es_final:
            salida.append("".join(prefijo))
        for i in range(tamAlfanumericos):
            if nodo.hijos[i] is not None:
                prefijo.append(caracter(i))
                self._run(nodo.hijos[i], prefijo, salida)
                prefijo.pop()


    def union(A, B):
        R = TrieArreglos()
        resultado = _union(A.raiz, B.raiz)
        if resultado is not None:
            R.raiz = resultado
        return R


    def intersection(A, B):
        R = TrieArreglos()
        resultado = _interseccion(A.raiz, B.raiz)
        if resultado is not None:
            R.raiz = resultado
        return R


    def difference(A, B):
        R = TrieArreglos()
        resultado = _difference(A.raiz, B.raiz)
        if resultado is not None:
            R.raiz = resultado
        return R