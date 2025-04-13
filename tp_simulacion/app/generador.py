import numpy as np

# Funcion para generar variables aleatorias
def generar_numeros(distribucion, n1, n2, cantidad):
    if distribucion == "Normal":
        sigma = np.sqrt(n2)
        return np.random.normal(loc=n1, scale=sigma, size=cantidad)
    elif distribucion == "Poisson":
        lam = n1
        return np.random.poisson(lam=lam, size=cantidad)
    elif distribucion == "Exponencial":
        lam = 1 / n1
        return np.random.exponential(scale=1/lam, size=cantidad)
    elif distribucion == "Uniforme":
        return np.random.uniform(low=n1, high=n2, size=cantidad)
    else:
        raise ValueError("Distribución no soportada.")
