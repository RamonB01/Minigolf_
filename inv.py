import sys
import csv
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QTableWidgetItem, QCheckBox, QTableWidget, QPushButton

class InvitadosDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("invitados.ui", self)  # Cargar la UI
        self.agregarInvitado.clicked.connect(self.agregar_invitado)  # Conectar botón de agregar
        self.comboEgresado.addItem("Seleccione Egresado")  # Agregar opción inicial al combo box
        self.comboEgresado.addItems(["Egresado 1", "Egresado 2"])  # Ejemplos de nombres de egresados
        self.tabla_invitado.setColumnCount(2)  # Configurar número de columnas
        self.tabla_invitado.setHorizontalHeaderLabels(["Invitado", "Retirada"])  # Encabezados
        self.tabla_invitado.setColumnWidth(0, 300)  # Ajustar ancho de columnas
        self.tabla_invitado.setColumnWidth(1, 100)  # Ancho para el checkbox

        # Botón para guardar en CSV
        self.guardarCSV = self.findChild(QPushButton, "guardarCSV")
        self.guardarCSV.clicked.connect(self.guardar_en_csv)

    def agregar_invitado(self):
        nombre = self.inputInvitado.text()
        if nombre:
            row = self.tabla_invitado.rowCount()
            self.tabla_invitado.insertRow(row)
            
            # Agrega el nombre del invitado
            self.tabla_invitado.setItem(row, 0, QTableWidgetItem(nombre))
            
            # Agrega el checkbox para "Retirada"
            checkbox = QCheckBox()
            self.tabla_invitado.setCellWidget(row, 1, checkbox)
            self.inputInvitado.clear()  # Limpia el campo de texto

    def guardar_en_csv(self):
        nombre_egresado = self.comboEgresado.currentText()
        if nombre_egresado and nombre_egresado != "Seleccione Egresado":
            filename = f"{nombre_egresado}.csv"
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Invitado", "Retirada"])  # Encabezados

                for row in range(self.tabla_invitado.rowCount()):
                    nombre_invitado = self.tabla_invitado.item(row, 0).text()
                    retirada = self.tabla_invitado.cellWidget(row, 1).isChecked()
                    writer.writerow([nombre_invitado, retirada])
            print(f"Datos guardados en {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = InvitadosDialog()
    dialog.setWindowTitle("Gestión de Invitados")
    dialog.show()
    sys.exit(app.exec())

