import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit, QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chisquare, norm, expon, poisson, kstest, anderson


# -------------------------- FUNCIONES ESTADÍSTICAS --------------------------
def generar_numeros(distribucion, media, varianza, cantidad):
    if distribucion == "Normal":
        sigma = np.sqrt(varianza)
        return np.random.normal(loc=media, scale=sigma, size=cantidad)
    elif distribucion == "Poisson":
        return np.random.poisson(lam=media, size=cantidad)
    elif distribucion == "Exponencial":
        lam = 1 / media
        return np.random.exponential(scale=1 / lam, size=cantidad)
    elif distribucion == "Uniforme":
        rango = np.sqrt(12 * varianza)
        a = media - rango / 2
        b = media + rango / 2
        return np.random.uniform(low=a, high=b, size=cantidad)
    else:
        raise ValueError("Distribución no soportada.")


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

        suma_obs = sum(frecuencias_observadas)
        suma_exp = sum(frecuencias_esperadas)
        if not np.isclose(suma_obs, suma_exp):
            factor = suma_obs / suma_exp
            frecuencias_esperadas = [f * factor for f in frecuencias_esperadas]

    chi2, p_valor = chisquare(f_obs=frecuencias_observadas, f_exp=frecuencias_esperadas)
    return chi2, p_valor


def prueba_kolmogorov_smirnov(numeros, distribucion):
    if distribucion == "Normal":
        mu, sigma = np.mean(numeros), np.std(numeros)
        return kstest(numeros, 'norm', args=(mu, sigma))
    elif distribucion == "Exponencial":
        scale = np.mean(numeros)
        return kstest(numeros, 'expon', args=(0, scale))
    elif distribucion == "Uniforme":
        a, b = min(numeros), max(numeros)
        return kstest(numeros, 'uniform', args=(a, b - a))
    else:
        raise ValueError("KS no soporta esta distribución.")


def prueba_anderson_darling(numeros, distribucion):
    if distribucion == "Normal":
        return anderson(numeros, dist='norm')
    elif distribucion == "Exponencial":
        return anderson(numeros, dist='expon')
    elif distribucion == "Uniforme":
        return anderson(numeros, dist='uniform')
    else:
        raise ValueError("Anderson-Darling no soporta esta distribución.")


# -------------------------- INTERFAZ --------------------------
class GeneradorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Números Aleatorios")
        self.modo_oscuro = False
        self.setup_ui()
        self.aplicar_tema()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Header con botón de modo oscuro alineado a la derecha
        header_layout = QHBoxLayout()
        header_layout.addStretch()  # Esto empuja el botón a la derecha

        self.modo_btn = QPushButton()
        self.modo_btn.setIcon(QIcon("modo_oscuro.png"))  # Usa tu propio ícono aquí
        self.modo_btn.setIconSize(QSize(24, 24))
        self.modo_btn.setFixedSize(32, 32)
        self.modo_btn.setStyleSheet("border: none;")  # Sin bordes ni fondo
        self.modo_btn.setToolTip("Cambiar modo claro/oscuro")
        self.modo_btn.clicked.connect(self.cambiar_modo)

        header_layout.addWidget(self.modo_btn, alignment=Qt.AlignRight)
        main_layout.addLayout(header_layout)

        # Resto de los widgets como antes
        self.distribucion_combo = QComboBox()
        self.distribucion_combo.addItems(["Normal", "Poisson", "Exponencial", "Uniforme"])
        self.distribucion_combo.currentTextChanged.connect(self.actualizar_campos)

        self.media_input = QLineEdit()
        self.varianza_input = QLineEdit()
        self.cantidad_input = QLineEdit()

        self.intervalos_input = QComboBox()
        self.intervalos_input.addItems(["10", "15", "20", "25"])

        self.prueba_combo = QComboBox()
        self.prueba_combo.addItems(["Ninguna", "Chi-Cuadrado", "Kolmogorov-Smirnov", "Anderson-Darling"])

        self.usar_existente_checkbox = QCheckBox("Usar datos existentes del archivo CSV (sin generar nuevos)")

        self.generar_btn = QPushButton("Generar")
        self.generar_btn.clicked.connect(self.generar)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)

        # Agregar widgets al layout
        for etiqueta, widget in [
            ("Distribución:", self.distribucion_combo),
            ("Media:", self.media_input),
            ("Varianza:", self.varianza_input),
            ("Cantidad de valores:", self.cantidad_input),
            ("Nº de intervalos (histograma):", self.intervalos_input),
            ("Prueba estadística:", self.prueba_combo)
        ]:
            main_layout.addWidget(QLabel(etiqueta))
            main_layout.addWidget(widget)

        main_layout.addWidget(self.usar_existente_checkbox)
        main_layout.addWidget(self.generar_btn)
        main_layout.addWidget(self.resultado_text)
        self.setLayout(main_layout)


    def aplicar_tema(self):
        claro = """
            QWidget { background-color: #f0f2f5; font-family: 'Segoe UI'; font-size: 14px; }
            QLabel { color: #333; }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #fff; border: 1px solid #ccc; border-radius: 6px; padding: 5px;
            }
            QPushButton {
                background-color: #0078d7; color: white; border-radius: 6px; padding: 8px;
            }
            QPushButton:hover { background-color: #005fa1; }
        """
        oscuro = """
            QWidget { background-color: #1e1e1e; color: #ccc; font-family: 'Segoe UI'; font-size: 14px; }
            QLabel { color: #fff; }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #2b2b2b; color: #fff; border: 1px solid #555; border-radius: 6px; padding: 5px;
            }
            QPushButton {
                background-color: #0078d7; color: white; border-radius: 6px; padding: 8px;
            }
            QPushButton:hover { background-color: #005fa1; }
        """
        self.setStyleSheet(oscuro if self.modo_oscuro else claro)

    def cambiar_modo(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()

    def actualizar_campos(self, texto_distribucion):
        if texto_distribucion in ["Poisson", "Exponencial"]:
            self.varianza_input.hide()
        else:
            self.varianza_input.show()

        self.prueba_combo.clear()
        self.prueba_combo.addItem("Ninguna")
        if texto_distribucion != "Poisson":
            self.prueba_combo.addItem("Kolmogorov-Smirnov")
            self.prueba_combo.addItem("Anderson-Darling")
        self.prueba_combo.addItem("Chi-Cuadrado")

    def generar(self):
        try:
            distribucion = self.distribucion_combo.currentText()
            prueba = self.prueba_combo.currentText()
            intervalos = int(self.intervalos_input.currentText())
            usar_existente = self.usar_existente_checkbox.isChecked()

            if usar_existente:
                try:
                    df = pd.read_csv("datos.csv", header=None)
                    numeros = df[0].to_numpy()
                    mensaje = f"Usando datos existentes de 'datos.csv' ({len(numeros)} valores)\n\n"
                except FileNotFoundError:
                    self.resultado_text.setText("⚠️ Archivo 'datos.csv' no encontrado.")
                    return
            else:
                media = float(self.media_input.text())
                cantidad = int(self.cantidad_input.text())
                varianza = float(self.varianza_input.text()) if distribucion in ["Normal", "Uniforme"] else None

                if not (0 < cantidad <= 50000):
                    raise ValueError("La cantidad debe estar entre 1 y 50000.")

                numeros = generar_numeros(distribucion, media, varianza, cantidad)

                with open("datos.csv", mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for numero in numeros:
                        writer.writerow([numero])
                mensaje = f"Números generados ({distribucion}):\n{numeros[:10]} ...\n\n"

            plt.close()
            plt.hist(numeros, bins=intervalos, edgecolor='black')
            plt.title('Histograma de los Números')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            plt.show()

            mensaje += f"\nResultado de la prueba estadística seleccionada ({prueba}):\n"

            if prueba == "Chi-Cuadrado":
                chi2, p_valor = prueba_chi_cuadrado(numeros, distribucion, intervalos)
                mensaje += f"Chi² = {chi2:.4f}, p-valor = {p_valor:.4f}\n"
                mensaje += "✅ Distribución aceptada.\n" if p_valor > 0.05 else "❌ Distribución rechazada.\n"

            elif prueba == "Kolmogorov-Smirnov":
                if distribucion == "Poisson":
                    mensaje += "❌ KS no soporta distribuciones discretas como Poisson.\n"
                else:
                    stat, p_valor = prueba_kolmogorov_smirnov(numeros, distribucion)
                    mensaje += f"Estadístico D = {stat:.4f}, p-valor = {p_valor:.4f}\n"
                    mensaje += "✅ Distribución aceptada.\n" if p_valor > 0.05 else "❌ Distribución rechazada.\n"

            elif prueba == "Anderson-Darling":
                if distribucion == "Poisson":
                    mensaje += "❌ Anderson-Darling no soporta distribuciones discretas como Poisson.\n"
                else:
                    resultado = prueba_anderson_darling(numeros, distribucion)
                    mensaje += f"Estadístico A² = {resultado.statistic:.4f}\n"
                    for sig, crit in zip(resultado.significance_level, resultado.critical_values):
                        mensaje += f"  Nivel {sig:.1f}% → valor crítico: {crit:.4f}\n"
                    mensaje += "✅ Distribución aceptada al 5%.\n" if resultado.statistic < resultado.critical_values[2] else "❌ Distribución rechazada al 5%.\n"

            self.resultado_text.setText(mensaje)

        except Exception as e:
            self.resultado_text.setText(f"Error: {e}")


# -------------------------- MAIN --------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorApp()
    ventana.setMaximumWidth(600)
    ventana.setMaximumHeight(1000)
    ventana.show()
    sys.exit(app.exec_())
