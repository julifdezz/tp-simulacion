from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QCheckBox
from PyQt5 import  QtGui
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from generador import generar_numeros
from pruebas import prueba_chi_cuadrado, prueba_kolmogorov_smirnov
from styles.styles import style

RUTA = "tp_simulacion/app/data/datos.csv"

# Interfaz con PyQt5
class GeneradorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador Numérico")
        self.setup_ui()
        self.setWindowIcon(QtGui.QIcon("tp_simulacion/assets/imgs/calculator.png"))
        
    def setup_ui(self):
        self.setStyleSheet(style)

        layout = QVBoxLayout()

        self.distribucion_label = QLabel("Distribución:")
        self.distribucion_combo = QComboBox()
        self.distribucion_combo.addItems(["Normal", "Poisson", "Exponencial", "Uniforme"])
        self.distribucion_combo.currentTextChanged.connect(self.actualizar_campos)

        self.param1_label = QLabel("Media:")
        self.param1_input = QLineEdit()

        self.param2_label = QLabel("Varianza:")
        self.param2_input = QLineEdit()

        self.cantidad_label = QLabel("Cantidad de valores:")
        self.cantidad_input = QLineEdit()

        self.intervalos_label = QLabel("Nº de intervalos (histograma):")
        self.intervalos_input = QComboBox()
        self.intervalos_input.addItems(["10", "15", "20", "25"])
        self.intervalos_input.setCurrentIndex(0)

        self.prueba_label = QLabel("Prueba estadística:")
        self.prueba_combo = QComboBox()
        self.prueba_combo.addItems(["Ninguna", "Chi-Cuadrado", "Kolmogorov-Smirnov"])

        self.usar_existente_checkbox = QCheckBox("Usar datos anteriores")
        
        self.generar_btn = QPushButton("GENERAR")
        self.generar_btn.clicked.connect(self.generar)

        self.resultado_text = QTextEdit()
        self.resultado_text.setReadOnly(True)

        layout.addWidget(self.distribucion_label)
        layout.addWidget(self.distribucion_combo)
        layout.addWidget(self.param1_label)
        layout.addWidget(self.param1_input)
        layout.addWidget(self.param2_label)
        layout.addWidget(self.param2_input)
        layout.addWidget(self.cantidad_label)
        layout.addWidget(self.cantidad_input)
        layout.addWidget(self.intervalos_label)
        layout.addWidget(self.intervalos_input)
        layout.addWidget(self.prueba_label)
        layout.addWidget(self.prueba_combo)
        layout.addWidget(self.usar_existente_checkbox)
        layout.addWidget(self.generar_btn)
        layout.addWidget(self.resultado_text)

        self.setLayout(layout)

    def actualizar_campos(self, texto_distribucion):   
        if texto_distribucion == "Normal":
            self.param2_label.setText("Varianza:")
            self.param2_label.show()
            self.param2_input.show()
         
        if texto_distribucion in ["Poisson", "Exponencial"]:
            self.param2_label.hide()
            self.param2_input.hide()
            self.param1_label.setText("Lambda:")
        else:
            self.param2_label.show()
            self.param2_input.show()
            self.param1_label.setText("Media:")

        if texto_distribucion == "Uniforme":
            self.param1_label.setText("Límite inferior (a):")
            self.param2_label.setText("Límite superior (b):")
            self.param2_label.show()
            self.param2_input.show()
            self.param1_input.setStyleSheet("")
            self.param2_input.setStyleSheet("")
        
        self.prueba_combo.clear()
        self.prueba_combo.addItem("Ninguna")
        if texto_distribucion != "Poisson":
            self.prueba_combo.addItem("Kolmogorov-Smirnov")
        self.prueba_combo.addItem("Chi-Cuadrado")

    def generar(self):
        try:
            distribucion = self.distribucion_combo.currentText()
            prueba = self.prueba_combo.currentText()
            intervalos = int(self.intervalos_input.currentText())
            usar_existente = self.usar_existente_checkbox.isChecked()

            if usar_existente:
                try:
                    df = pd.read_csv(RUTA, header=None)
                    numeros = df[0].to_numpy()
                    mensaje = f"🟦 Usando datos existentes de 'datos.csv' ({len(numeros)} valores)\n\n"
                except FileNotFoundError:
                    self.resultado_text.setText("⚠️ Archivo 'datos.csv' no encontrado. No se puede hacer la prueba.")
                    return
            else:
                
                if distribucion not in ["Normal", "Uniforme"]:
                    # varianza = None
                    if self.param1_input.text() == "":
                            raise ValueError("Lambda no puede estar vacía.")
                    else: 
                        n1 = float(self.param1_input.text())
                        if n1 < 0:
                            raise ValueError("Lambda debe ser mayor a cero.")
                
                else: 
                    if self.param1_input.text() == "":
                            raise ValueError("El primer parametro no puede estar vacio.")
                    elif self.param2_input.text() == "":
                         raise ValueError("El segundo parametro no puede estar vacio.")
                    else: 
                        n1 = float(self.param1_input.text())
                
                if distribucion == "Uniforme":
                    n1 = float(self.param1_input.text()) # Media seria nuestro Limite Inferior
                    n2 = float(self.param2_input.text())  # Varianza seria nuestro Limite Superior.
                    if n1 >= n2:
                        raise ValueError("El límite inferior debe ser menor que el superior.")

                if distribucion not in ["Normal", "Uniforme"]:  
                    n2 = None
                else: 
                    if self.param2_input.text() == "":
                            raise ValueError("La Varianza no puede estar vacía.")
                    else: 
                        n2 = float(self.param2_input.text())
                        if (n2 < 0 and distribucion == "Normal"):
                            raise ValueError("La Varianza debe ser mayor a cero.")
                    
                if self.cantidad_input.text() == "":
                    raise ValueError("La Cantidad no puede estar vacía.")
                else: 
                    cantidad = int(self.cantidad_input.text())

                if not (0 < cantidad <= 50000):
                    raise ValueError("La Cantidad debe estar entre 1 y 50000.")

                numeros = generar_numeros(distribucion, n1, n2, cantidad)
                
                with open(RUTA, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    for numero in numeros:
                        writer.writerow([numero])

                mensaje = f"🟦 Números generados ({distribucion}):\n{numeros}\n\n"

            # Mostrar histograma
            plt.close()
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.canvas.manager.set_window_title(f"Histograma para la distribucion {distribucion}")
            ax.hist(numeros, bins=intervalos, edgecolor='black', color='#5c9ded', alpha=0.85)
            ax.set_title(f'Histograma ({distribucion})', fontsize=20, fontweight='bold', color='#333')
            ax.set_xlabel('Valor', fontsize=16, color='#444')
            ax.set_ylabel('Frecuencia', fontsize=16, color='#444')
            ax.tick_params(axis='both', labelsize=13)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.6)
            plt.tight_layout()
            plt.show()

            # Prueba estadística
            mensaje += f"\n🟦 Resultado de la prueba estadística seleccionada ({prueba}):\n"

            if prueba == "Chi-Cuadrado":
                chi2, p_valor = prueba_chi_cuadrado(numeros, distribucion, intervalos)
                mensaje += f"Chi² = {chi2:.4f}, p-valor = {p_valor:.4f}\n"
                mensaje += "✅ Distribución aceptada (p > 0.05).\n" if p_valor > 0.05 else "❌ Distribución rechazada (p <= 0.05).\n"

            elif prueba == "Kolmogorov-Smirnov":
                if distribucion == "Poisson":
                    mensaje += "❌ KS no soporta distribuciones discretas como Poisson.\n"
                else:
                    stat, p_valor = prueba_kolmogorov_smirnov(numeros, distribucion)
                    mensaje += f"Estadístico D = {stat:.4f}, p-valor = {p_valor:.4f}\n"
                    mensaje += "✅ Distribución aceptada (p > 0.05).\n" if p_valor > 0.05 else "❌ Distribución rechazada (p <= 0.05).\n"

            self.resultado_text.setText(mensaje)

        except Exception as e:
            self.resultado_text.setText(f"⚠️ {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeneradorApp()
    ventana.setMinimumWidth(500)
    ventana.setMaximumWidth(500)
    ventana.setMinimumHeight(900)
    ventana.setMaximumHeight(900)
    ventana.show()
    sys.exit(app.exec_())
