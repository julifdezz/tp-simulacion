import numpy as np

# Funcion para generar variables aleatorias
def generar_numeros(distribucion, media, varianza, cantidad):
    if distribucion == "Normal":
        sigma = np.sqrt(varianza)
        return np.random.normal(loc=media, scale=sigma, size=cantidad)
    elif distribucion == "Poisson":
        lam = media
        return np.random.poisson(lam=lam, size=cantidad)
    elif distribucion == "Exponencial":
        lam = 1 / media
        return np.random.exponential(scale=1/lam, size=cantidad)
    elif distribucion == "Uniforme":
        rango = np.sqrt(12 * varianza)
        a = media - rango / 2
        b = media + rango / 2
        return np.random.uniform(low=a, high=b, size=cantidad)
    else:
        raise ValueError("Distribución no soportada.")
