from PyQt6.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
import os

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Crear Carpeta")
        self.setGeometry(100, 100, 300, 150)

        # Crear un widget central y layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear un campo de entrada para el nombre de la carpeta
        self.nombre_carpeta_input = QLineEdit(self)
        self.nombre_carpeta_input.setPlaceholderText("Ingrese el nombre de la carpeta")
        self.layout.addWidget(self.nombre_carpeta_input)

        # Crear un botón para crear la carpeta
        self.crear_boton = QPushButton("Crear Carpeta", self)
        self.crear_boton.clicked.connect(self.crear_carpeta)
        self.layout.addWidget(self.crear_boton)

    def crear_carpeta(self):
        # Obtener el nombre de la carpeta del campo de entrada
        nombre_carpeta = self.nombre_carpeta_input.text()

        # Definir la ruta de la carpeta "Escuelas"
        ruta_escuelas = "Escuelas"
        # Crear la carpeta "Escuelas" si no existe
        os.makedirs(ruta_escuelas, exist_ok=True)

        # Definir la ruta completa para la nueva carpeta
        ruta_nueva_carpeta = os.path.join(ruta_escuelas, nombre_carpeta)

        # Verificar si la carpeta ya existe
        if not os.path.exists(ruta_nueva_carpeta):
            # Crear la nueva carpeta
            os.makedirs(ruta_nueva_carpeta)
            QMessageBox.information(self, "Éxito", f"Carpeta '{nombre_carpeta}' creada en '{ruta_escuelas}'")
            self.close()  # Cerrar la ventana después de crear la carpeta
        else:
            QMessageBox.warning(self, "Error", f"La carpeta '{nombre_carpeta}' ya existe en '{ruta_escuelas}'")

app = QApplication([])
ventana = MiVentana()
ventana.show()
app.exec()
