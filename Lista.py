from PyQt6.QtWidgets import QDialog, QSpinBox ,QLineEdit, QPushButton, QVBoxLayout , QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QCheckBox, QFileDialog
from PyQt6.QtGui import  QDoubleValidator, QIntValidator
from PyQt6 import uic
from PyQt6.QtCore import Qt
import csv
import os, os.path
import datetime
import sys

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("lista_egresado.ui", self)
        
        self.agregarBoton.clicked.connect(self.agregarBorrar)
        
        self.tabla_egresados.setColumnWidth(0, 300)
        self.tabla_egresados.setColumnWidth(1, 50)
        self.tabla_egresados.setColumnWidth(2, 50)
        self.tabla_egresados.setColumnWidth(3, 50)
        self.tabla_egresados.setColumnWidth(4, 50)
        self.tabla_egresados.setColumnWidth(5, 50)
        self.tabla_egresados.setColumnWidth(6, 50)
        self.tabla_egresados.setColumnWidth(7, 50)
        self.tabla_egresados.setColumnWidth(8, 50)
        self.tabla_egresados.setColumnWidth(9, 50)
        self.tabla_egresados.setColumnWidth(10, 50)
        self.tabla_egresados.setColumnWidth(11, 50)
        self.tabla_egresados.setColumnWidth(12, 50)
        self.tabla_egresados.setColumnWidth(13, 300)
        self.tabla_egresados.setColumnWidth(14, 50)
        self.abrirCarpeta.clicked.connect(self.cargar_csv)
        self.editarBoton.clicked.connect(self.toggleEditMode)
        self.crearCarpeta.clicked.connect(self.crearCarpetas)
        self.guardar.clicked.connect(self.guardar_csv)
        validar = QIntValidator(0,100,self)
        self.tarjetas.setValidator(validar)
        self.isEditable = False

    def crearCarpetas(self):
        dialogo = CrearCarpetaDialog()
        dialogo.exec()

    def toggleEditMode(self):
        self.isEditable = not self.isEditable

        for row in range(self.tabla_egresados.rowCount()):
            for col in range(self.tabla_egresados.columnCount()):
                item = self.tabla_egresados.item(row, col)
                if item:
                    if self.isEditable:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        if self.isEditable:
            self.editarBoton.setText("Guardar Edición")
        else:
            self.editarBoton.setText("Editar")

    def agregarBorrar(self):
        self.addEgresado()
        self.nombre.setText("")
        self.madre.setText("")
        self.padre.setText("")
        self.tarjetas.setText("")

    def addEgresado(self):
        nombreEg = self.nombre.text()
        padresEg = self.padre.text()
        madreEg = self.madre.text()
        mypEg = "dasasdasd"

        if madreEg and padresEg:
            mypEg = f"{padresEg} y {madreEg}"
        elif madreEg: 
            mypEg = madreEg
        elif padresEg: 
            mypEg = padresEg
        spin_box = QSpinBox()
        spin_box.setRange(0, 100)
        tarjetasEg = self.tarjetas.text()
        if tarjetasEg:
            spin_box.setValue(int(tarjetasEg))
        else:
            spin_box.setValue(0)
        checkbox1 = QCheckBox("")
        checkbox2 = QCheckBox("")
        checkbox3 = QCheckBox("")
        checkbox4 = QCheckBox("")
        checkbox5 = QCheckBox("")
        checkbox6 = QCheckBox("")
        checkbox7 = QCheckBox("")
        checkbox8 = QCheckBox("")
        checkbox9 = QCheckBox("")
        checkbox10 = QCheckBox("")
        checkbox11 = QCheckBox("")
        checkbox12 = QCheckBox("")
        fila = self.tabla_egresados.rowCount()
        self.tabla_egresados.insertRow(fila) 
        self.tabla_egresados.setItem(fila, 0, QTableWidgetItem(f"{nombreEg}"))
        # self.tabla_egresados.setItem(fila, 1, QTableWidgetItem(f"{cuotasCant}"))
        # self.tabla_egresados.setItem(fila, 1, QTableWidgetItem(f"{cuotasCant} {checkbox}" ))
        self.tabla_egresados.setCellWidget(fila, 1, checkbox1)
        self.tabla_egresados.setCellWidget(fila, 2, checkbox2)
        self.tabla_egresados.setCellWidget(fila, 3, checkbox3)
        self.tabla_egresados.setCellWidget(fila, 4, checkbox4)
        self.tabla_egresados.setCellWidget(fila, 5, checkbox5)
        self.tabla_egresados.setCellWidget(fila, 6, checkbox6)
        self.tabla_egresados.setCellWidget(fila, 7, checkbox7)
        self.tabla_egresados.setCellWidget(fila, 8, checkbox8)
        self.tabla_egresados.setCellWidget(fila, 9, checkbox9)
        self.tabla_egresados.setCellWidget(fila, 10, checkbox10)
        self.tabla_egresados.setCellWidget(fila, 11, checkbox11)
        self.tabla_egresados.setCellWidget(fila, 12, checkbox12)
        self.tabla_egresados.setItem(fila, 13, QTableWidgetItem(f"{mypEg}"))
        self.tabla_egresados.setCellWidget(fila, 14, spin_box)

    def cargar_csv(self):
        self.tabla_egresados.setRowCount(0)
        nombre_archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', 'Escuelas', 'Archivos CSV (*.csv)')
        if nombre_archivo[0]:
            with open(nombre_archivo[0], 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                carpeta_seleccionada = os.path.dirname(nombre_archivo[0])
                nombre_carpeta = os.path.basename(carpeta_seleccionada)

                self.nombreColegio.setText(nombre_carpeta)
                for fila in lector:

                    self.tabla_egresados.insertRow(self.tabla_egresados.rowCount())

                    self.tabla_egresados.setItem(self.tabla_egresados.rowCount() - 1, 0, QTableWidgetItem(fila[0]))

                    for col in range(1, 13):
                        checkbox = QCheckBox("")
                        checkbox.setChecked(fila[col].lower() == 'true')
                        self.tabla_egresados.setCellWidget(self.tabla_egresados.rowCount() - 1, col, checkbox)

                    self.tabla_egresados.setItem(self.tabla_egresados.rowCount() - 1, 13, QTableWidgetItem(fila[13]))
                    spin_box = QSpinBox()
                    spin_box.setRange(0,100)
                    valor_spinbox = int(fila[14]) if fila[14].isdigit() else 0
                    spin_box.setValue(valor_spinbox)
                    self.tabla_egresados.setCellWidget(self.tabla_egresados.rowCount() - 1, 14, spin_box)
    
    def guardar_csv(self):
        nombre_archivo, _ = QFileDialog.getSaveFileName(self, 'Guardar Archivo', 'Escuelas', 'Archivos CSV (*.csv)')
        
        if nombre_archivo:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                
                # Escribir los datos de la tabla
                for fila in range(self.tabla_egresados.rowCount()):
                    items = []
                    
                    # Columna 0: texto normal
                    item = self.tabla_egresados.item(fila, 0)
                    items.append(item.text() if item else '')

                    # Columnas 1 a 12: checkboxes
                    for col in range(1, 13):
                        widget = self.tabla_egresados.cellWidget(fila, col)
                        if isinstance(widget, QCheckBox):
                            items.append("True" if widget.isChecked() else "False")
                        else:
                            items.append("")

                    # Columna 13: texto normal
                    item = self.tabla_egresados.item(fila, 13)
                    items.append(item.text() if item else '')

                    # Columna 14: QSpinBox
                    spin_box = self.tabla_egresados.cellWidget(fila, 14)
                    if isinstance(spin_box, QSpinBox):
                        items.append(str(spin_box.value()))
                    else:
                        items.append('')

                    # Escribir la fila en el archivo CSV
                    escritor.writerow(items)






    # def abrirColegio(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.ReadOnly  # Solo lectura
    #     file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo CSV", "", "Archivos CSV (*.csv);;Todos los archivos (*)", options=options)
        
    #     if file_path:  
    #         self.tabla_egresados.setRowCount(0)  
    #         print(f"Archivo seleccionado: {file_path}")

    #         with open(file_path, 'r') as file:
    #             reader = csv.reader(file)
    #             next(reader) 
    #             for datosFila in reader:
    #                 fila = self.tabla_egresados.rowCount()
    #                 self.tabla_egresados.insertRow(fila)
    #                 self.tabla_egresados.setColumnCount(len(datosFila))
    #                 for column, data in enumerate(datosFila):
    #                     item = QTableWidgetItem(data)
    #                     self.tabla_egresados.setItem(fila, column, item)


class CrearCarpetaDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Configuración del diálogo
        self.setWindowTitle("Crear Carpeta")
        self.setGeometry(100, 100, 300, 150)

        # Crear un layout vertical
        self.layout = QVBoxLayout(self)

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
        nombre_carpeta = self.nombre_carpeta_input.text().strip()

        # Definir la ruta de la carpeta "Escuelas"
        ruta_escuelas = "Escuelas"
        # Crear la carpeta "Escuelas" si no existe
        os.makedirs(ruta_escuelas, exist_ok=True)

        # Definir la ruta completa para la nueva carpeta
        ruta_nueva_carpeta = os.path.join(ruta_escuelas, nombre_carpeta)

        # Verificar si la carpeta ya existe
        if nombre_carpeta:  # Asegurarse de que el nombre no esté vacío
            if not os.path.exists(ruta_nueva_carpeta):
                # Crear la nueva carpeta
                os.makedirs(ruta_nueva_carpeta)
                QMessageBox.information(self, "Éxito", f"Carpeta '{nombre_carpeta}' creada en '{ruta_escuelas}'")

                # Aquí está el nuevo código agregado para crear el archivo CSV
                ruta_csv = os.path.join(ruta_nueva_carpeta, f"{nombre_carpeta}.csv")
                with open(ruta_csv, 'w', newline='', encoding='utf-8') as csv_file:
                    pass  # Crea un archivo vacío

                self.accept()  # Cerrar el diálogo con éxito
            else:
                QMessageBox.warning(self, "Error", f"La carpeta '{nombre_carpeta}' ya existe en '{ruta_escuelas}'")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre válido para la carpeta.")



app = QApplication([])
win = MiVentana()
win.setWindowTitle("Minigolf Eventos")
win.show()
app.exec()