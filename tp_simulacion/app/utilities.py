from scipy.stats import expon, norm, poisson
import pandas as pd
import numpy as np

def intervalo(numeros, cant_intervalos):
    """Calcula los limites de los intervalos para el histograma."""
    lim_inf = []
    lim_sup = []
    min_val = min(numeros)
    max_val = max(numeros)
    if min_val == max_val: # Validación para q los intervalos no se bugeen xd
        min_val -= 0.5
        max_val += 0.5
    rango = max_val - min_val   
    amplitud = rango / cant_intervalos

    for i in range(cant_intervalos):
        li = min_val + i * amplitud
        ls = li + amplitud
        lim_inf.append(li)
        lim_sup.append(ls)

    return lim_inf, lim_sup, rango


def frec_observadas(numeros, lim_inf, lim_sup):
    contador_fo = []
    for i in range(len(lim_inf)):
        li = lim_inf[i]
        ls = lim_sup[i]
        cuenta = 0
        for n in numeros:
            if (i == 0 and li <= n < ls) or (i > 0 and li < n <= ls):
                cuenta += 1
        contador_fo.append(cuenta)
    return contador_fo


def frec_esp_uniforme(numeros, total, cant_intervalos):
    fe = total / cant_intervalos
    return [fe] * cant_intervalos


def frec_esp_expon(vec_li, vec_ls, lmda, numeros):
    vec_fe = []
    n = len(numeros)
    for i in range(len(vec_li)):
        li = vec_li[i]
        ls = vec_ls[i]
        fe = (expon.cdf(ls, scale=1/lmda) - expon.cdf(li, scale=1/lmda)) * n
        vec_fe.append(fe)
    return vec_fe


def frec_esp_normal(vec_li, vec_ls, mu, sigma, numeros):
    vec_fe = []
    n = len(numeros)
    for i in range(len(vec_li)):
        li = vec_li[i]
        ls = vec_ls[i]
        fe = (norm.cdf(ls, loc=mu, scale=sigma) - norm.cdf(li, loc=mu, scale=sigma)) * n
        vec_fe.append(fe)
    return vec_fe


def frec_esp_poisson(vec_li, vec_ls, mu, numeros):
    vec_fe = []
    n = len(numeros)
    for i in range(len(vec_li)):
        li = vec_li[i]
        ls = vec_ls[i]
        fe = (poisson.cdf(ls, mu) - poisson.cdf(li, mu)) * n
        vec_fe.append(fe)
    return vec_fe


def chi_cuadrado(frec_o, frec_e):
    vec = []
    for i in range(len(frec_o)):
        if frec_e[i] > 0:
            chi_calc = pow(frec_o[i] - frec_e[i], 2) / frec_e[i]
        else:
            chi_calc = 0
        vec.append(chi_calc)
    return sum(vec)

def tabla_frecuencias(lim_inf, lim_sup, fo, fe):
    filas = []
    for i in range(len(fo)):
        filas.append({
            "Intervalo": f"[{lim_inf[i]:.2f} - {lim_sup[i]:.2f}]",
            "Frec. Observada": fo[i],
            "Frec. Esperada": round(fe[i], 2),
            "Contribución Chi²": round(((fo[i] - fe[i])**2 / fe[i]), 4) if fe[i] > 0 else 0
        })
    df = pd.DataFrame(filas)
    df.loc["Totales"] = {
        "Intervalo": "Total",
        "Frec. Observada": sum(fo),
        "Frec. Esperada": round(sum(fe), 2),
        "Contribución Chi²": chi_cuadrado(fo, fe)
    }
    return df