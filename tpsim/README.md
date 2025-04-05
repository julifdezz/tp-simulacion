## DOCUMENTATION

https://doc.qt.io/qtforpython-6/



import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QComboBox, QTextEdit
)
import sys

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

        # Resultado
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)

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
        layout.addWidget(self.resultado)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorApp()
    ventana.show()
    sys.exit(app.exec_())
