import numpy as np
from scipy.stats import chisquare, norm, expon, poisson, kstest, uniform
import pandas as pd
from utilities import *



# Funcion para prueba Chi-Cuadrado
# def prueba_chi_cuadrado(numeros, distribucion, bins):
#     frecuencias_observadas, limites = np.histogram(numeros, bins=bins)
#     total = len(numeros)

#     if distribucion == "Uniforme":
#         frecuencias_esperadas = [total / bins] * bins
#     else:
#         cdf = None
#         if distribucion == "Normal":
#             mu, sigma = np.mean(numeros), np.std(numeros)
#             cdf = lambda x: norm.cdf(x, loc=mu, scale=sigma)
#         elif distribucion == "Exponencial":
#             scale = np.mean(numeros)
#             cdf = lambda x: expon.cdf(x, scale=scale)
#         elif distribucion == "Poisson":
#             mu = int(np.mean(numeros))
#             cdf = lambda x: poisson.cdf(x, mu=mu)

#         frecuencias_esperadas = []
#         for i in range(len(limites) - 1):
#             prob = cdf(limites[i + 1]) - cdf(limites[i])
#             frecuencias_esperadas.append(prob * total)

#         # Ajustar suma esperada a la suma observada
#         suma_obs = sum(frecuencias_observadas)
#         suma_exp = sum(frecuencias_esperadas)
#         if not np.isclose(suma_obs, suma_exp):
#             factor = suma_obs / suma_exp
#             frecuencias_esperadas = [f * factor for f in frecuencias_esperadas]
        
#     chi2, p_valor = chisquare(f_obs=frecuencias_observadas, f_exp=frecuencias_esperadas)    
#     return chi2, p_valor

def prueba_chi_cuadrado(numeros, distribucion, cant_intervalos):
    lim_inf, lim_sup, _ = intervalo(numeros, cant_intervalos)
    vec_fo = frec_observadas(numeros, lim_inf, lim_sup)
    if distribucion == "Uniforme":
        vec_fe = frec_esp_uniforme(numeros, len(numeros), cant_intervalos)

    elif distribucion == "Exponencial":
        lmda = 1 / np.mean(numeros)
        vec_fe = frec_esp_expon(lim_inf, lim_sup, lmda, numeros)

    elif distribucion == "Normal":
        mu, sigma = np.mean(numeros), np.std(numeros)
        vec_fe = frec_esp_normal(lim_inf, lim_sup, mu, sigma, numeros)

    elif distribucion == "Poisson":
        mu = np.mean(numeros)
        vec_fe = frec_esp_poisson(lim_inf, lim_sup, mu, numeros)

    else:
        raise ValueError("Distribución no soportada.")

    chi = chi_cuadrado(vec_fo, vec_fe)
    return chi, lim_inf, lim_sup, vec_fo, vec_fe