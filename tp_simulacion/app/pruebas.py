import numpy as np
from scipy.stats import chisquare, norm, expon, poisson, kstest

# Funciones para pruebas estadisticas 


# Funcion para prueba Chi-Cuadrado
def prueba_chi_cuadrado(numeros, distribucion, bins):
    frecuencias_observadas, limites = np.histogram(numeros, bins=bins)
    total = len(numeros)

    if distribucion == "Uniforme":
        frecuencias_esperadas = [total / bins] * bins
    else:
        cdf = None
        if distribucion == "Normal":
            mu, sigma = np.mean(numeros), np.std(numeros)
            cdf = lambda x: norm.cdf(x, loc=mu, scale=sigma)
        elif distribucion == "Exponencial":
            scale = np.mean(numeros)
            cdf = lambda x: expon.cdf(x, scale=scale)
        elif distribucion == "Poisson":
            mu = int(np.mean(numeros))
            cdf = lambda x: poisson.cdf(x, mu=mu)

        frecuencias_esperadas = []
        for i in range(len(limites) - 1):
            prob = cdf(limites[i + 1]) - cdf(limites[i])
            frecuencias_esperadas.append(prob * total)

        # Ajustar suma esperada a la suma observada
        suma_obs = sum(frecuencias_observadas)
        suma_exp = sum(frecuencias_esperadas)
        if not np.isclose(suma_obs, suma_exp):
            factor = suma_obs / suma_exp
            frecuencias_esperadas = [f * factor for f in frecuencias_esperadas]

    chi2, p_valor = chisquare(f_obs=frecuencias_observadas, f_exp=frecuencias_esperadas)
    return chi2, p_valor


# Funcion para prueba Kolmogorov–Smirnov
def prueba_kolmogorov_smirnov(numeros, distribucion):
    if distribucion == "Normal":
        mu, sigma = np.mean(numeros), np.std(numeros)
        stat, p_valor = kstest(numeros, 'norm', args=(mu, sigma))
    elif distribucion == "Exponencial":
        scale = np.mean(numeros)
        stat, p_valor = kstest(numeros, 'expon', args=(0, scale))
    elif distribucion == "Uniforme":
        a, b = min(numeros), max(numeros)
        stat, p_valor = kstest(numeros, 'uniform', args=(a, b - a))
    else:
        raise ValueError("KS no soporta esta distribución.")
    return stat, p_valor

