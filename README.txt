Proyecto 1 — Modelo Conjunto

1. Descripción

Este programa permite trabajar con dos conjuntos, A y B, mediante un menú de opciones. Se pueden insertar, eliminar
y buscar elementos, mostrar los conjuntos y calcular su unión, intersección y diferencia.

Los elementos son cadenas alfanuméricas (letras minúsculas a-z y dígitos 0-9) de hasta 20 caracteres.

También permite cambiar la estructura de datos utilizada para representar los conjuntos. La numeración coincide
con la del menú de main.py:

1. Lista por punteros: Lista ordenada simplemente enlazada.
2. Lista por arreglos: Lista ordenada almacenada en un arreglo.
3. Tabla hash: Estructura que permite organizar y buscar elementos mediante una función hash, con
   encadenamiento separado para resolver colisiones (estructura por defecto, tamaño 10).
4. ABB por punteros: Árbol binario de búsqueda cuyos nodos dinámicos contienen un valor y referencias a sus
   subárboles izquierdo y derecho.
5. ABB por vector heap: Árbol binario de búsqueda representado de forma contigua en un arreglo mediante mapeo
   de índices (hijo izquierdo en 2i+1, hijo derecho en 2i+2).
6. Trie por punteros: Árbol de prefijos donde cada nodo contiene enlaces explícitos a sus nodos hijos mediante
   punteros.
7. Trie por arreglos: Árbol de prefijos donde cada nodo almacena un vector estático de tamaño fijo para mapear
   las entradas del alfabeto a los subárboles correspondientes.


2. Requisitos

- Tener instalado Python 3 (probado con Python 3.12).
- Mantener todos los archivos en la misma carpeta:
  - main.py
  - ConjuntoListaPunteros.py
  - ConjuntoListaArreglo.py
  - ConjuntoHash.py
  - ArbolPunteros.py
  - ArbolHeap.py
  - TriePunteros.py
  - TrieArreglos.py
  - analisis.py
- Solo para generar los gráficos de analisis.py: instalar pandas y matplotlib
  (pip install pandas matplotlib). main.py no los necesita.


3. Cómo ejecutar el programa

Abra una terminal en la carpeta del proyecto y ejecute:

Win/Linux
python3 main.py

(En Windows también puede usarse: python main.py)


4. Programa de análisis (tercera etapa)

analisis.py mide el tiempo de duración y el uso de espacio de las siete estructuras (más una variante de
referencia de tabla hash con tamaño proporcional a N) con distintos tipos y tamaños de conjuntos. Importa las
clases de las etapas anteriores sin modificarlas.

Uso, desde la carpeta del proyecto:

python3 analisis.py                       Corrida completa (puede tardar bastante)
python3 analisis.py --rapido              Corrida corta, útil para probar
python3 analisis.py --tamanos 100 1000    Tamaños de N propios
python3 analisis.py --conjuntos max20     Solo un tipo de conjunto (aleatorio8, max20, prefijo, ordenado)
python3 analisis.py --graficar            Solo regenera los gráficos a partir de los CSV existentes

Salida (carpeta resultados/, se crea automáticamente):
- tiempos.csv: tiempos por operación, estructura, tipo de conjunto y tamaño N.
- espacio.csv: uso de memoria por estructura, tipo de conjunto y tamaño N.
- Gráficos en formato .png (tiempos por tipo de conjunto y uso de espacio).