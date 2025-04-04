import numpy as np


# media = int(input('Ingrese el valor de la media: '))
# desv = float(input('Ingrese el valor de la desviacion estandar: '))
# m = int(input('Ingrese el tamaño de la muestra: '))

# def validar(num):
#     pass


# def generarNormal():
#     pass


def generar_numeros(distribucion, media, varianza, cantidad):
    if distribucion == "normal":
        # En la normal: media = mu, varianza = sigma^2 → sigma = sqrt(varianza)
        sigma = np.sqrt(varianza)
        return np.random.normal(loc=media, scale=sigma, size=cantidad)

    elif distribucion == "poisson":
        # En Poisson, la media = varianza = λ
        # Si se ingresan media y varianza diferentes, se ignora la varianza
        lam = media
        return np.random.poisson(lam=lam, size=cantidad)

    elif distribucion == "exponencial":
        # En exponencial: media = 1/lambda → lambda = 1/media
        # Y varianza = 1/lambda²
        lam = 1 / media
        return np.random.exponential(scale=1/lam, size=cantidad)

    elif distribucion == "uniforme":
        # Para distribución uniforme:
        # media = (a + b)/2
        # varianza = (b - a)^2 / 12
        # Se puede despejar a y b:
        rango = np.sqrt(12 * varianza)
        a = media - rango / 2
        b = media + rango / 2
        return np.random.uniform(low=a, high=b, size=cantidad)

    else:
        raise ValueError("Distribución no soportada.")

def main():
    print("Distribuciones soportadas: normal, poisson, exponencial, uniforme")
    distribucion = input("Ingrese la distribución deseada: ").strip().lower()
    media = float(input("Ingrese la media: "))
    varianza = float(input("Ingrese la varianza: "))
    cantidad = int(input("Cantidad de números a generar: "))

    try:
        numeros = generar_numeros(distribucion, media, varianza, cantidad)
        print(f"\nNúmeros generados ({distribucion}):\n{numeros}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()