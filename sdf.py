import sys
import os

if getattr(sys, 'frozen', False):
    # Si está ejecutándose desde un ejecutable empaquetado
    base_path = sys._MEIPASS
else:
    # Si está ejecutándose desde el código fuente
    base_path = os.path.abspath(".")

# Acceso a los archivos .ui y otros recursos
ui_path = os.path.join(base_path, 'gui', 'lista_egresado.ui')
