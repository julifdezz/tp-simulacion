import numpy as np
from utilities import *

# PRUEBA DE CHI-CUADRADO
def prueba_chi_cuadrado(numeros, distribucion, cant_intervalos):
    # Calculamos los limites inferior y superior y las frecuencias observadas
    lim_inf, lim_sup, _ = intervalo(numeros, cant_intervalos) # (utilities.py)
    vec_fo = frec_observadas(numeros, lim_inf, lim_sup) # (utilities.py)
    
    # Segun la distribucion seleccionada, calculamos la frecuencia esperada y realizamos la prueba de chi-cuadrado
    if distribucion == "Uniforme":
        vec_fe = frec_esp_uniforme(len(numeros), cant_intervalos) # (utilities.py)

    elif distribucion == "Exponencial":
        lmda = 1 / np.mean(numeros) # lambda = 1 / media
        vec_fe = frec_esp_expon(lim_inf, lim_sup, lmda, numeros)

    elif distribucion == "Normal":
        mu, sigma = np.mean(numeros), np.std(numeros) # media y desviacion estandar
        vec_fe = frec_esp_normal(lim_inf, lim_sup, mu, sigma, numeros)

    elif distribucion == "Poisson":
        mu = np.mean(numeros) # media (seria lambda)
        vec_fe = frec_esp_poisson(lim_inf, lim_sup, mu, numeros)

    else:
        raise ValueError("Distribución no soportada.")

    chi = chi_cuadrado(vec_fo, vec_fe)
    return chi, lim_inf, lim_sup, vec_fo, vec_fe