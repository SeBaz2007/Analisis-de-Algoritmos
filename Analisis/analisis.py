"""
Proyecto 1 - Tercera etapa: programa de analisis de tiempos y espacio.

Mide, para las 7 estructuras del Modelo Conjunto (mas una variante de
referencia de tabla hash con tamano proporcional a N), el tiempo de duracion
y el uso de espacio con distintos tipos y tamanos de conjuntos.

Operaciones medidas: insert, member (presente), member (ausente), delete,
print, union, intersection, difference.

Uso:
    python3 analisis.py                       # corrida completa
    python3 analisis.py --rapido              # corrida corta (prueba)
    python3 analisis.py --tamanos 100 1000    # tamanos propios
    python3 analisis.py --graficar            # solo regenera graficos desde los CSV

Salida (carpeta resultados/): tiempos.csv, espacio.csv y graficos .png
"""
import argparse
import contextlib
import csv
import gc
import io
import os
import random
import statistics
import string
import sys
import time
import tracemalloc

from ConjuntoHash import ConjuntoHash
from ConjuntoListaArreglo import ConjuntoListaArreglo
from ConjuntoListaPunteros import ConjuntoListaPunteros
from ArbolPunteros import ArbolPunteros, _IteradorInorden
from ArbolHeap import ArbolHeap
from TriePunteros import ConjuntoTriePunteros
from TrieArreglos import TrieArreglos

ALFABETO = string.ascii_lowercase + string.digits
SEMILLA = 2026

# ---------------------------------------------------------------- estructuras
# nombre -> fabrica(n). La Hash(m=N) NO es parte del proyecto: es una variante
# de referencia para mostrar el efecto de la redistribucion/tamano de tabla.
ESTRUCTURAS = {
    "Lista punteros": lambda n: ConjuntoListaPunteros(),
    "Lista arreglo": lambda n: ConjuntoListaArreglo(),
    "Hash (m=10)": lambda n: ConjuntoHash(10),
    "Hash (m=N) ref.": lambda n: ConjuntoHash(max(10, n)),
    "ABB punteros": lambda n: ArbolPunteros(),
    "ABB heap": lambda n: ArbolHeap(),
    "Trie punteros": lambda n: ConjuntoTriePunteros(),
    "Trie arreglos": lambda n: TrieArreglos(),
}
# Estructuras que guardan las cadenas completas (los tries las codifican en el camino)
GUARDA_CADENAS = {"Lista punteros", "Lista arreglo", "Hash (m=10)",
                  "Hash (m=N) ref.", "ABB punteros", "ABB heap"}
# Tope de N por estructura (memoria: cada nodo de trie ocupa ~0.5 KB)
MAX_N = {"Trie punteros": 10000, "Trie arreglos": 10000}

OPERACIONES = ["insert", "member_si", "member_no", "delete", "print",
               "union", "intersection", "difference"]
LIMITE_SLOTS_HEAP = 1 << 22  # 4 194 304 posiciones (~33 MB de punteros)


# ------------------------------------------------------------------- datos
def _cadena(rng, largo, prefijo=""):
    return prefijo + "".join(rng.choice(ALFABETO) for _ in range(largo - len(prefijo)))


def generar_universo(tipo, cantidad, rng):
    """Devuelve `cantidad` cadenas unicas segun el tipo de conjunto."""
    vistos, lista = set(), []
    if tipo in ("aleatorio8", "ordenado"):
        gen = lambda: _cadena(rng, 8)
    elif tipo == "max20":
        gen = lambda: _cadena(rng, 20)
    elif tipo == "prefijo":                      # 15 caracteres comunes + 5 propios
        gen = lambda: "prefijocomun123" + _cadena(rng, 5)
    else:
        raise ValueError(tipo)
    while len(lista) < cantidad:
        s = gen()
        if s not in vistos:
            vistos.add(s)
            lista.append(s)
    return lista


def generar_AB(tipo, n, rng):
    """A y B de tamano n con 50 % de solapamiento. Retorna listas en orden de insercion."""
    universo = generar_universo(tipo, n + n // 2, rng)
    A = universo[: n]
    B = universo[n // 2:]
    if tipo == "ordenado":
        A, B = sorted(A), sorted(B)
    else:
        rng.shuffle(A)
        rng.shuffle(B)
    return A, B


# --------------------------------------------------- utilidades de estructura
def extraer(nombre, s):
    """Lista (ordenada) de elementos de una estructura, para verificar resultados."""
    if nombre == "Lista punteros":
        out, a = [], s.primero
        while a is not None:
            out.append(a.elemento)
            a = a.siguiente
        return sorted(out)
    if nombre == "Lista arreglo":
        return sorted(s.elementos)
    if nombre.startswith("Hash"):
        return sorted(e for lista in s.tabla for e in lista)
    if nombre == "ABB punteros":
        out, it = [], _IteradorInorden(s.raiz)
        while it.empty():          # (en ese codigo empty() es True si QUEDAN nodos)
            out.append(it.actual())
            it.avanzar()
        return sorted(out)
    if nombre == "ABB heap":
        return sorted(s._elementos())
    if nombre == "Trie punteros":
        return sorted(s._recorrer())
    if nombre == "Trie arreglos":
        out = []
        s._run(s.raiz, [], out)
        return sorted(out)
    raise ValueError(nombre)


def heap_viable(secuencia, limite=LIMITE_SLOTS_HEAP):
    """Simula insertar `secuencia` en el vector heap sin reservarlo.
    Retorna (viable, posicion_maxima_necesaria_o_primera_que_excede_limite)."""
    nodos, maximo = {}, 0
    for e in secuencia:
        i = 0
        while True:
            if i >= limite:
                return False, i
            actual = nodos.get(i)
            if actual is None:
                nodos[i] = e
                maximo = max(maximo, i)
                break
            if e == actual:
                break
            i = 2 * i + 1 if e < actual else 2 * i + 2
    return True, maximo


def tamano_cadenas(elementos):
    return sum(sys.getsizeof(e) for e in elementos)


class Cronometro:
    def __enter__(self):
        gc.collect()
        gc.disable()
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *a):
        self.dt = time.perf_counter() - self.t0
        gc.enable()


# -------------------------------------------------------------- una medicion
def medir_una_vez(nombre, n, A_el, B_el, rng, operaciones_activas, verificar):
    """Ejecuta todas las operaciones activas una vez. Retorna dict op -> segundos
    (tiempo total de la operacion; ver K para las muestreadas) y bandera de correccion."""
    fab = ESTRUCTURAS[nombre]
    res, ok = {}, True
    setA, setB = set(A_el), set(B_el)

    A = fab(n)
    with Cronometro() as c:
        for e in A_el:
            A.insert(e)
    res["insert"] = c.dt
    B = fab(n)
    for e in B_el:
        B.insert(e)

    k = min(n, 1000)
    muestra_si = rng.sample(A_el, k)
    solo_B = [e for e in B_el if e not in setA]
    muestra_no = rng.sample(solo_B, min(k, len(solo_B))) if solo_B else []

    if "member_si" in operaciones_activas:
        with Cronometro() as c:
            for e in muestra_si:
                A.member(e)
        res["member_si"] = (c.dt, len(muestra_si))
        if verificar:
            ok &= all(A.member(e) for e in muestra_si[:50])
    if "member_no" in operaciones_activas and muestra_no:
        with Cronometro() as c:
            for e in muestra_no:
                A.member(e)
        res["member_no"] = (c.dt, len(muestra_no))
        if verificar:
            ok &= not any(A.member(e) for e in muestra_no[:50])

    if "print" in operaciones_activas:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            with Cronometro() as c:
                A.print()
        res["print"] = c.dt

    esperado = {"union": setA | setB, "intersection": setA & setB,
                "difference": setA - setB}
    for op in ("union", "intersection", "difference"):
        if op not in operaciones_activas:
            continue
        with Cronometro() as c:
            R = getattr(A, op)(B)
        res[op] = c.dt
        if verificar:
            ok &= (extraer(nombre, R) == sorted(esperado[op]))
        del R

    if "delete" in operaciones_activas:
        kd = min(n, 300)
        muestra_del = rng.sample(A_el, kd)
        with Cronometro() as c:
            for e in muestra_del:
                A.delete(e)
        res["delete"] = (c.dt, kd)
        if verificar:
            ok &= not any(A.member(e) for e in muestra_del[:50])
    return res, ok


def medir_espacio(nombre, n, A_el):
    """Bytes de la estructura (tracemalloc), sin contar las cadenas ya existentes."""
    gc.collect()
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    S = ESTRUCTURAS[nombre](n)
    for e in A_el:
        S.insert(e)
    actual = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    estructura = actual - base
    total = estructura + (tamano_cadenas(A_el) if nombre in GUARDA_CADENAS else 0)
    slots = len(S.vector) if nombre == "ABB heap" else ""
    del S
    gc.collect()
    return estructura, total, slots


# ----------------------------------------------------------------- principal
def correr(args):
    os.makedirs(args.salida, exist_ok=True)
    f_t = open(os.path.join(args.salida, "tiempos.csv"), "w", newline="")
    f_e = open(os.path.join(args.salida, "espacio.csv"), "w", newline="")
    w_t, w_e = csv.writer(f_t), csv.writer(f_e)
    w_t.writerow(["estructura", "conjunto", "N", "operacion", "tiempo_total_s",
                  "n_ops", "tiempo_por_op_us", "reps", "correcto", "estado"])
    w_e.writerow(["estructura", "conjunto", "N", "bytes_estructura",
                  "bytes_con_cadenas", "bytes_por_elemento", "slots_heap", "estado"])

    def fila_t(*v):
        w_t.writerow(v)
        f_t.flush()

    for tipo in args.conjuntos:
        for nombre in ESTRUCTURAS:
            ultimo = {}          # op -> (n, tiempo) para predecir el siguiente tamano
            bloqueadas = set()
            for n in args.tamanos:
                if n > MAX_N.get(nombre, 10 ** 9):
                    continue
                rng = random.Random(f"{SEMILLA}-{tipo}-{n}")
                A_el, B_el = generar_AB(tipo, n, rng)
                setA, setB = set(A_el), set(B_el)
                activas = set(OPERACIONES) - bloqueadas
                if "insert" in bloqueadas:
                    break

                # --- viabilidad del ABB por vector heap
                if nombre == "ABB heap":
                    vA, sa = heap_viable(A_el)
                    vB, sb = heap_viable(B_el)
                    if not (vA and vB):
                        msg = (f"inviable: el vector necesitaria mas de {LIMITE_SLOTS_HEAP} "
                               f"posiciones (arbol degenerado)")
                        fila_t(nombre, tipo, n, "insert", "", n, "", 0, "", msg)
                        w_e.writerow([nombre, tipo, n, "", "", "", sa, msg])
                        break
                    for op, res_set in (("union", setA | setB),
                                        ("intersection", setA & setB),
                                        ("difference", setA - setB)):
                        v, s = heap_viable(sorted(res_set))
                        if not v:
                            activas.discard(op)
                            if ("setops_heap", n) not in ultimo:
                                ultimo[("setops_heap", n)] = 1
                            fila_t(nombre, tipo, n, op, "", n, "", 0, "",
                                   f"inviable: insertar el resultado ordenado crea un arbol "
                                   f"en cadena (>{LIMITE_SLOTS_HEAP} posiciones)")

                # --- prediccion de tiempo (peor caso cuadratico)
                for op in list(activas):
                    if op in ultimo:
                        n0, t0 = ultimo[op]
                        pred = t0 * (n / n0) ** 2
                        if pred > args.presupuesto:
                            activas.discard(op)
                            bloqueadas.add(op)
                            fila_t(nombre, tipo, n, op, "", "", "", 0, "",
                                   f"omitido: tiempo estimado {pred:.0f}s > {args.presupuesto}s")
                if "insert" not in activas:
                    break

                # --- repeticiones
                reps_max = 5 if n <= 1000 else 3 if n <= 10000 else 1
                acum = {op: [] for op in OPERACIONES}
                correcto, reps = True, 0
                t_ini = time.perf_counter()
                for r in range(reps_max):
                    res, ok = medir_una_vez(nombre, n, A_el, B_el, rng, activas,
                                            verificar=(r == 0))
                    if r == 0:
                        correcto = ok
                    for op, v in res.items():
                        acum[op].append(v)
                    reps += 1
                    if time.perf_counter() - t_ini > args.presupuesto:
                        break

                for op in OPERACIONES:
                    if not acum[op]:
                        continue
                    if isinstance(acum[op][0], tuple):
                        t = statistics.median(v[0] for v in acum[op])
                        nops = acum[op][0][1]
                    else:
                        t = statistics.median(acum[op])
                        nops = n if op == "insert" else 1
                    ultimo[op] = (n, t)
                    fila_t(nombre, tipo, n, op, f"{t:.6f}", nops,
                           f"{t / nops * 1e6:.3f}", reps, int(correcto), "ok")

                # --- espacio
                est, tot, slots = medir_espacio(nombre, n, A_el)
                w_e.writerow([nombre, tipo, n, est, tot, f"{tot / n:.1f}", slots, "ok"])
                f_e.flush()
                print(f"[{tipo:10s}] {nombre:16s} N={n:<7d} insert={ultimo['insert'][1]:.3f}s "
                      f"correcto={correcto}", flush=True)
    f_t.close()
    f_e.close()


# ------------------------------------------------------------------ graficos
def graficar(carpeta):
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t = pd.read_csv(os.path.join(carpeta, "tiempos.csv"))
    e = pd.read_csv(os.path.join(carpeta, "espacio.csv"))
    t = t[t.estado == "ok"].copy()
    t["tiempo_por_op_us"] = t["tiempo_por_op_us"].astype(float)
    e = e[e.estado == "ok"].copy()

    estilos = {
        "Lista punteros": ("tab:blue", "o", "-"), "Lista arreglo": ("tab:cyan", "s", "-"),
        "Hash (m=10)": ("tab:orange", "^", "-"), "Hash (m=N) ref.": ("tab:orange", "x", ":"),
        "ABB punteros": ("tab:green", "v", "-"), "ABB heap": ("tab:olive", "D", "-"),
        "Trie punteros": ("tab:red", "P", "-"), "Trie arreglos": ("tab:purple", "*", "-"),
    }
    titulos = {"insert": "Insert (por elemento)", "member_si": "Member (presente)",
               "member_no": "Member (ausente)", "delete": "Delete (por elemento)",
               "print": "Print (total)", "union": "Union (total)",
               "intersection": "Intersection (total)", "difference": "Difference (total)"}
    nombres_conj = {"aleatorio8": "Aleatorio, 8 caracteres", "max20": "Aleatorio, 20 caracteres",
                    "prefijo": "Prefijo comun de 15 caracteres",
                    "ordenado": "Insercion en orden ascendente"}

    for tipo in t.conjunto.unique():
        fig, axs = plt.subplots(2, 4, figsize=(20, 9))
        for ax, op in zip(axs.ravel(), OPERACIONES):
            d = t[(t.conjunto == tipo) & (t.operacion == op)]
            col = "tiempo_por_op_us" if op in ("insert", "member_si", "member_no", "delete") else "tiempo_total_s"
            for nombre, g in d.groupby("estructura"):
                g = g.sort_values("N")
                y = g[col].astype(float)
                c, m, ls = estilos[nombre]
                ax.plot(g.N, y, color=c, marker=m, linestyle=ls, label=nombre, markersize=5)
            ax.set_xscale("log"); ax.set_yscale("log")
            ax.set_title(titulos[op]); ax.set_xlabel("N (elementos por conjunto)")
            ax.set_ylabel("microsegundos" if col == "tiempo_por_op_us" else "segundos")
            ax.grid(True, which="both", alpha=0.3)
        axs[0, 0].legend(fontsize=8)
        fig.suptitle(f"Tiempos - {nombres_conj.get(tipo, tipo)}", fontsize=15)
        fig.tight_layout()
        fig.savefig(os.path.join(carpeta, f"tiempos_{tipo}.png"), dpi=110)
        plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(15, 5.5))
    for ax, col, tit in zip(axs, ["bytes_por_elemento", "bytes_con_cadenas"],
                            ["Bytes por elemento", "Bytes totales"]):
        d = e[e.conjunto == "aleatorio8"]
        for nombre, g in d.groupby("estructura"):
            g = g.sort_values("N")
            c, m, ls = estilos[nombre]
            ax.plot(g.N, g[col], color=c, marker=m, linestyle=ls, label=nombre, markersize=5)
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title(tit + " (aleatorio, 8 car.)")
        ax.set_xlabel("N"); ax.grid(True, which="both", alpha=0.3)
    axs[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(carpeta, "espacio_aleatorio8.png"), dpi=110)
    plt.close(fig)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5.5))
    for ax, tipo in zip(axs, ["max20", "prefijo", "ordenado"]):
        d = e[e.conjunto == tipo]
        for nombre, g in d.groupby("estructura"):
            g = g.sort_values("N")
            c, m, ls = estilos[nombre]
            ax.plot(g.N, g.bytes_por_elemento, color=c, marker=m, linestyle=ls, label=nombre, markersize=5)
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title(nombres_conj[tipo])
        ax.set_xlabel("N"); ax.set_ylabel("bytes por elemento"); ax.grid(True, which="both", alpha=0.3)
    axs[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(carpeta, "espacio_otros_conjuntos.png"), dpi=110)
    plt.close(fig)
    print("Graficos generados en", carpeta)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tamanos", type=int, nargs="+",
                    default=[10, 20, 30, 50, 100, 200, 500, 1000, 5000, 10000, 50000])
    ap.add_argument("--conjuntos", nargs="+",
                    default=["aleatorio8", "max20", "prefijo", "ordenado"])
    ap.add_argument("--presupuesto", type=float, default=15.0,
                    help="segundos maximos estimados por medicion")
    ap.add_argument("--salida", default="resultados")
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--graficar", action="store_true", help="solo graficar desde los CSV")
    args = ap.parse_args()
    if args.rapido:
        args.tamanos, args.presupuesto = [10, 100, 1000], 3.0
    if not args.graficar:
        correr(args)
    graficar(args.salida)
