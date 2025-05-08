import numpy as np

# Funcion para generar variables aleatorias (llamada desde el main.py)
def generar_numeros(distribucion, n1, n2, cantidad):
    if distribucion == "Normal":
        sigma = np.sqrt(n2)
        return np.random.normal(loc=n1, scale=sigma, size=cantidad) # loc: media, scale: desviacion estandar
    elif distribucion == "Poisson":
        lam = n1
        return np.random.poisson(lam=lam, size=cantidad) # lam: lambda
    elif distribucion == "Exponencial":
        lam = 1 / n1
        return np.random.exponential(scale=1/lam, size=cantidad) # (cambio opcional: scale = 1 / n1)
    elif distribucion == "Uniforme":
        return np.random.uniform(low=n1, high=n2, size=cantidad) # low/high: limites superior e inferior
    else:
        raise ValueError("Distribución no soportada.")
