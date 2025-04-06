import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit
)
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Función para generar valores de variables aleatorias según la distribución seleccionada
def generar_numeros(distribucion, media, varianza, cantidad):
    if distribucion == "Normal":
        # En la normal: media = mu, varianza = sigma^2 → sigma = sqrt(varianza)
        sigma = np.sqrt(varianza)
        return np.random.normal(loc=media, scale=sigma, size=cantidad)

    elif distribucion == "Poisson":
        # En Poisson, la media = varianza = λ
        # Si se ingresan media y varianza diferentes, se ignora la varianza
        lam = media
        return np.random.poisson(lam=lam, size=cantidad)

    elif distribucion == "Exponencial":
        # En exponencial: media = 1/lambda → lambda = 1/media
        # Y varianza = 1/lambda²
        lam = 1 / media
        return np.random.exponential(scale=1/lam, size=cantidad)

    elif distribucion == "Uniforme":
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


class GeneradorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Números Aleatorios")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Distribución
        self.distribucion_label = QLabel("Distribución:")
        self.distribucion_combo = QComboBox()
        self.distribucion_combo.addItems(["Normal", "Poisson", "Exponencial", "Uniforme"])
        self.distribucion_combo.currentTextChanged.connect(self.actualizar_campos)

        # Media / Lambda
        self.media_label = QLabel("Media:")
        self.media_input = QLineEdit()

        # Varianza
        self.varianza_label = QLabel("Varianza:")
        self.varianza_input = QLineEdit()

        # Cantidad
        self.cantidad_label = QLabel("Cantidad de valores:")
        self.cantidad_input = QLineEdit()

        # Intervalos
        self.intervalos_label = QLabel("Nº de intervalos (histograma):")
        self.intervalos_input = QComboBox()
        self.intervalos_input.addItems(["10", "15", "20", "25"])
        self.intervalos_input.setCurrentIndex(0)

        # Botón
        self.generar_btn = QPushButton("Generar")
        self.generar_btn.clicked.connect(self.generar)

        # Resultado
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)

        # Agregar campos a la ventana
        layout.addWidget(self.distribucion_label)
        layout.addWidget(self.distribucion_combo)

        layout.addWidget(self.media_label)
        layout.addWidget(self.media_input)

        layout.addWidget(self.varianza_label)
        layout.addWidget(self.varianza_input)

        layout.addWidget(self.cantidad_label)
        layout.addWidget(self.cantidad_input)

        layout.addWidget(self.intervalos_label)
        layout.addWidget(self.intervalos_input)

        layout.addWidget(self.generar_btn)
        layout.addWidget(self.resultado_text)

        self.setLayout(layout)

    def actualizar_campos(self, texto_distribucion):
        if texto_distribucion in ["Poisson", "Exponencial"]:
            self.varianza_label.hide()
            self.varianza_input.hide()
            self.media_label.setText("Lambda:")
        else:
            self.varianza_label.show()
            self.varianza_input.show()
            self.media_label.setText("Media:")

    def generar(self):
        try:
            distribucion = self.distribucion_combo.currentText()
            media = float(self.media_input.text())
            varianza = float(self.varianza_input.text())
            cantidad = int(self.cantidad_input.text())
            intervalos = int(self.intervalos_input.currentText())

            if varianza < 0:
                raise ValueError("La varianza debe ser mayor a cero.")
                
            if 0 < cantidad <= 50000:
                # Generar números según la distribución seleccionada
                numeros = generar_numeros(distribucion, media, varianza, cantidad)
                
                # Guardar los números en un archivo CSV
                archivo_csv = "datos.csv"
                with open(archivo_csv, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for numero in numeros:
                        writer.writerow([numero])  # Escribir cada número en una fila
                
                #Variable para leer el archivo CSV 
                df = pd.read_csv('datos.csv', header = None) 
                plt.close()

                #Crear el histograma
                plt.hist(df[0], bins=intervalos, edgecolor='black')  # Ajusta 'bins' si quieres más o menos intervalos
                plt.title('Histograma de los Números Generados')
                plt.xlabel('Valor')
                plt.ylabel('Frecuencia')
                plt.show()
                
                self.resultado_text.setText(f"Números generados ({distribucion}):\n{numeros}")
            
            else: 
                raise ValueError("La cantidad debe ser entre [1, 50000].")
        except Exception as e:
            self.resultado_text.setText(f"Error: {e}")       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorApp()
    ventana.show()
    sys.exit(app.exec_())