class Nodo:
    def __init__(self, elemento):
        self.elemento = elemento
        self.siguiente = None
        
class ConjuntoListaPunteros:
    def __init__(self):
        self.primero = None

    def clear(self):
        self.primero = None

    def done(self):
        self.clear()

    def insert(self, elemento):
        nuevo = Nodo(elemento)
        
        #Lista vacia
        if self.primero is None:
            self.primero = nuevo
            return
        #meter al inicio
        if elemento < self.primero.elemento:
            nuevo.siguiente= self.primero  
            self.primero = nuevo
            return
        anterior = None
        actual = self.primero
            
        while actual is not None and actual.elemento < elemento:
            anterior = actual
            actual = actual.siguiente
                
        # Ya existe
        if actual is not None and actual.elemento == elemento:
            return
        
        nuevo.siguiente = actual
        anterior.siguiente = nuevo
        
    def member(self, elemento):
        actual = self.primero

        while actual is not None:
            if actual.elemento == elemento:
                return True

            if actual.elemento > elemento:
                return False

            actual = actual.siguiente

        return False
    
    
    def print(self):
        actual = self.primero

        while actual is not None:
            print(actual.elemento, end=" ")
            actual = actual.siguiente

        print()
        
    def delete(self, elemento):
        anterior = None
        actual = self.primero

        while actual is not None and actual.elemento < elemento:
            anterior = actual
            actual = actual.siguiente

        if actual is None or actual.elemento != elemento:
            return

        if anterior is None:
            self.primero = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
            
    
    
    def union(self, otro):
        resultado = ConjuntoListaPunteros()

        actual = self.primero
        while actual is not None:
            resultado.insert(actual.elemento)
            actual = actual.siguiente

        actual = otro.primero
        while actual is not None:
            resultado.insert(actual.elemento)
            actual = actual.siguiente

        return resultado
    
    def intersection(self, otro):
        resultado = ConjuntoListaPunteros()

        actual = self.primero

        while actual is not None:
            if otro.member(actual.elemento):
                resultado.insert(actual.elemento)

            actual = actual.siguiente

        return resultado
    
    def difference(self, otro):
        resultado = ConjuntoListaPunteros()

        actual = self.primero

        while actual is not None:
            if not otro.member(actual.elemento):
                resultado.insert(actual.elemento)

            actual = actual.siguiente

        return resultado