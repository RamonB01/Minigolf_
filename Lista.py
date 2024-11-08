from PyQt6.QtWidgets import QDialog, QSpinBox ,QLineEdit, QPushButton, QVBoxLayout , QMainWindow, QApplication, QTableWidgetItem, QMessageBox, QCheckBox, QFileDialog
from PyQt6.QtGui import  QDoubleValidator, QIntValidator, QIcon
from PyQt6 import uic
from PyQt6.QtCore import Qt
# from inv import InvitadosDialog
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import csv
import os, os.path
import datetime
import sys


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("lista_egresado.ui", self)
        
        self.setWindowIcon(QIcon("img/lista.png"))
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
        self.verInvitados.clicked.connect(self.abrirInvitados)
        validar = QIntValidator(0,100,self)
        self.tarjetas.setValidator(validar)
        self.isEditable = False
        ruta_archivo_csv = None
        nombre_carpeta = ""
        self.tabla_egresados.cellChanged.connect(self.on_table_change)
        # self.guardar.setEnabled(False)
        if self.nombreColegio.text() == "Colegio":
            self.guardar.setEnabled(False)
            self.verInvitados.setEnabled(False)
            self.editarBoton.setEnabled(False)
            self.agregarBoton.setEnabled(False)
        else:
            self.guardar.setEnabled(True)
            self.verInvitados.setEnabled(True)

    def crearCarpetas(self):
        dialogo = CrearCarpetaDialog()
        dialogo.exec()
        self.cargar_csv()
        
    def abrirInvitados(self):
        dialogo = InvitadosDialog(nombre_carpeta=self.nombre_carpeta)
        # dialogo = InvitadosDialog()
        
        # Limpiar y agregar nombres de egresados al comboEgresado
        nombres_egresados = []
        for row in range(self.tabla_egresados.rowCount()):
            nombre_item = self.tabla_egresados.item(row, 0)
            if nombre_item:
                nombres_egresados.append(nombre_item.text())

        dialogo.cargar_egresados(nombres_egresados)  # Llamar al método para cargar nombres en el diálogo
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

        # Crear la estructura de carpetas si no existe
        ruta_escuela = os.path.join("Escuelas", self.nombre_carpeta)
        ruta_invitados = os.path.join(ruta_escuela, "Invitados")
        os.makedirs(ruta_invitados, exist_ok=True)

        # Crear el archivo CSV para el egresado en la carpeta "Invitados"
        ruta_csv = os.path.join(ruta_invitados, f"{nombreEg}.csv")
        with open(ruta_csv, 'w', newline='', encoding='utf-8') as csv_file:
            escritor = csv.writer(csv_file)
            escritor.writerow(["Invitado", "Retirada"])  # Encabezado

        # Agregar el resto de la lógica para insertar el egresado en la tabla (checkboxes, spinbox, etc.)
        spin_box = QSpinBox()
        spin_box.setRange(0, 100)
        tarjetasEg = self.tarjetas.text()
        if tarjetasEg:
            spin_box.setValue(int(tarjetasEg))
        else:
            spin_box.setValue(0)
        checkboxes = [QCheckBox("") for _ in range(12)]
        
        fila = self.tabla_egresados.rowCount()
        self.tabla_egresados.insertRow(fila) 
        self.tabla_egresados.setItem(fila, 0, QTableWidgetItem(nombreEg))
        for col, checkbox in enumerate(checkboxes, start=1):
            self.tabla_egresados.setCellWidget(fila, col, checkbox)
        self.tabla_egresados.setItem(fila, 13, QTableWidgetItem(mypEg))
        self.tabla_egresados.setCellWidget(fila, 14, spin_box)


    def cargar_csv(self):
        self.tabla_egresados.setRowCount(0)
        nombre_archivo = QFileDialog.getOpenFileName(self, 'Abrir archivo', 'Escuelas', 'Archivos CSV (*.csv)')
        if nombre_archivo:
            self.ruta_archivo_csv = nombre_archivo
        if nombre_archivo[0]:
            with open(nombre_archivo[0], 'r', newline='', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                carpeta_seleccionada = os.path.dirname(nombre_archivo[0])
                self.nombre_carpeta = os.path.basename(carpeta_seleccionada)

                self.nombreColegio.setText(self.nombre_carpeta)
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
        self.guardar.setEnabled(True)
        self.verInvitados.setEnabled(True)
        self.agregarBoton.setEnabled(True)
        self.editarBoton.setEnabled(True)
        self.abrirCarpeta.setEnabled(False)
        self.crearCarpeta.setEnabled(False)


    def guardar_csv(self):
        nombre_archivo, _ = QFileDialog.getSaveFileName(self, 'Guardar Archivo',f'Escuelas/{self.nombre_carpeta}/{self.nombre_carpeta}', 'Archivos CSV (*.csv)')
        
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
        self.abrirCarpeta.setEnabled(True)
        self.crearCarpeta.setEnabled(True)

    def on_table_change(self, row, column):
        self.abrirCarpeta.setEnabled(False)
        self.crearCarpeta.setEnabled(False)
        self.guardar.setEnabled(True)

    # if self.tabla_egresados.onChance 



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

        # Definir la ruta completa para la nueva carpeta de la escuela
        ruta_nueva_carpeta = os.path.join(ruta_escuelas, nombre_carpeta)

        # Verificar si la carpeta ya existe
        if nombre_carpeta:  # Asegurarse de que el nombre no esté vacío
            if not os.path.exists(ruta_nueva_carpeta):
                # Crear la nueva carpeta de la escuela
                os.makedirs(ruta_nueva_carpeta)
                
                # Crear la subcarpeta "Invitados" dentro de la carpeta de la escuela
                ruta_invitados = os.path.join(ruta_nueva_carpeta, "Invitados")
                os.makedirs(ruta_invitados)

                # Mensaje de éxito
                QMessageBox.information(self, "Éxito", f"Carpeta '{nombre_carpeta}' y su carpeta 'Invitados' creadas en '{ruta_escuelas}'")

                # Crear un archivo CSV vacío en la carpeta de la escuela
                ruta_csv = os.path.join(ruta_nueva_carpeta, f"{nombre_carpeta}.csv")
                with open(ruta_csv, 'w', newline='', encoding='utf-8') as csv_file:
                    pass  # Crea un archivo CSV vacío

                self.accept()  # Cerrar el diálogo con éxito
            else:
                QMessageBox.warning(self, "Error", f"La carpeta '{nombre_carpeta}' ya existe en '{ruta_escuelas}'")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre válido para la carpeta.")


class InvitadosDialog(QDialog):

    def __init__(self, nombre_carpeta):
        super().__init__()
        uic.loadUi("invitados.ui", self)
        self.nombre_carpeta = nombre_carpeta
        self.setWindowIcon(QIcon("img/lista.png"))
        self.agregarInvitado.clicked.connect(self.agregar_invitado)
        self.guardarCSV.clicked.connect(self.guardar_en_csv)
        self.comboEgresado.currentIndexChanged.connect(self.cargar_invitados)

        # Configuración de la tabla
        self.tabla_invitado.setColumnCount(2)
        self.tabla_invitado.setHorizontalHeaderLabels(["Invitado", "Retirada"])
        self.tabla_invitado.setColumnWidth(0, 300)  
        self.tabla_invitado.setColumnWidth(1, 100)

    def cargar_egresados(self, nombres_egresados):
        self.comboEgresado.clear()
        self.comboEgresado.addItem("Seleccione Egresado")
        self.comboEgresado.addItems(nombres_egresados)

    def cargar_invitados(self):
        # Limpia la tabla
        self.tabla_invitado.setRowCount(0)
        
        nombre_egresado = self.comboEgresado.currentText()
        if nombre_egresado and nombre_egresado != "Seleccione Egresado":
            ruta_archivo = f"Escuelas/{self.nombre_carpeta}/Invitados/{nombre_egresado}.csv"
            
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Salta los encabezados
                    for row_data in reader:
                        self._agregar_fila_invitado(row_data[0], row_data[1] == "True")

    def _agregar_fila_invitado(self, nombre, retirada):
        row = self.tabla_invitado.rowCount()
        self.tabla_invitado.insertRow(row)
        self.tabla_invitado.setItem(row, 0, QTableWidgetItem(nombre))
        
        checkbox = QCheckBox()
        checkbox.setChecked(retirada)
        self.tabla_invitado.setCellWidget(row, 1, checkbox)

    def agregar_invitado(self):
        nombre = self.inputInvitado.text()
        if nombre:
            self._agregar_fila_invitado(nombre, False)
            self.inputInvitado.clear()

    def guardar_en_csv(self):
        nombre_egresado = self.comboEgresado.currentText()
        if nombre_egresado and nombre_egresado != "Seleccione Egresado":
            ruta_escuela = f"Escuelas/{self.nombre_carpeta}/Invitados"
            os.makedirs(ruta_escuela, exist_ok=True)
            filename = os.path.join(ruta_escuela, f"{nombre_egresado}.csv")
            
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Invitado", "Retirada"])
                
                for row in range(self.tabla_invitado.rowCount()):
                    nombre_invitado = self.tabla_invitado.item(row, 0).text() if self.tabla_invitado.item(row, 0) else ""
                    retirada = self.tabla_invitado.cellWidget(row, 1).isChecked() if self.tabla_invitado.cellWidget(row, 1) else False
                    writer.writerow([nombre_invitado, retirada])
            
            print(f"Datos guardados en {filename}")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un egresado válido para guardar los datos.")





app = QApplication([])
win = MiVentana()
win.setWindowTitle("Minigolf Eventos")
win.show()
app.exec()