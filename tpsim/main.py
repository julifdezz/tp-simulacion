import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QComboBox, QTextEdit)
import sys 
# To do List
# Faltan los intervalos (agregar en el layout de la app, y a su vez agregar la libreria para el histograma B))
# Alan G. slds


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

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Números Aleatorios")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()

        # Selección de Distribución
        self.distribucion_label = QLabel("Distribución:")
        self.distribucion_combo = QComboBox()
        self.distribucion_combo.addItems(["normal", "poisson", "exponencial", "uniforme"])

        # Media
        self.media_label = QLabel("Media:")
        self.media_input = QLineEdit()

        # Varianza
        self.varianza_label = QLabel("Varianza:")
        self.varianza_input = QLineEdit()

        # Cantidad
        self.cantidad_label = QLabel("Cantidad:")
        self.cantidad_input = QLineEdit()

        # Botón para Generar los números
        self.boton = QPushButton("Generar")
        self.boton.clicked.connect(self.generar)

        # Resultado
        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)

        # Añadir widgets al layout
        layout.addWidget(self.distribucion_label)
        layout.addWidget(self.distribucion_combo)

        layout.addWidget(self.media_label)
        layout.addWidget(self.media_input)

        layout.addWidget(self.varianza_label)
        layout.addWidget(self.varianza_input)

        layout.addWidget(self.cantidad_label)
        layout.addWidget(self.cantidad_input)

        layout.addWidget(self.boton)
        layout.addWidget(self.resultado_text)

        self.setLayout(layout)

    def generar(self):
        try:
            distribucion = self.distribucion_combo.currentText()
            media = float(self.media_input.text())
            varianza = float(self.varianza_input.text())
            cantidad = int(self.cantidad_input.text())

            numeros = generar_numeros(distribucion, media, varianza, cantidad)
            self.resultado_text.setText(f"Números generados ({distribucion}):\n{numeros}")
        except Exception as e:
            self.resultado_text.setText(f"Error: {e}")                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GUI()
    ventana.show()
    sys.exit(app.exec_())