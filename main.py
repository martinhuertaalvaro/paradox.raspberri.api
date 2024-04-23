import sys
import random
import numpy as np
import os
import subprocess

import pandas as pd

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QVBoxLayout,QAction, QMenu, QSpacerItem, QHBoxLayout, QPushButton, QComboBox, QScrollArea, QTableWidget, QTableWidgetItem, QSizePolicy, QFileDialog
from PyQt5.QtGui import QImage, QColor, QPalette, QPixmap, QFontDatabase, QFont, QIcon,QPainter
from PyQt5.QtCore import Qt, QTimer, QSize

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from datetime import datetime


class FullScreenWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.BtimerMedidas = False

        self.historialMedidas = []

        self.x_graph_act = []
        self.y_graph_act = []

        self.figure_act = None
        self.canvas_act = None
        self.line_act = None

        self.y_min = 0
        self.y_max = 1

        self.cont_graph_act = 0
        
        # Ubicacion de carpetas -------------------------------------------------------

        carpeta_raiz = os.getcwd()
        ruta_setup = os.path.join(carpeta_raiz, 'setup')
        self.ruta_images = os.path.join(ruta_setup, 'Images')
        self.ruta_tipografia = os.path.join(ruta_setup, 'Tipografia')
        self.ruta_icons = os.path.join(self.ruta_images, 'Icon')
        self.ruta_image = os.path.join(self.ruta_images, 'Image')
        self.ruta_folders = os.path.join(ruta_setup, 'Folders')
        self.ruta_Documents = os.path.join(self.ruta_folders, 'Documents')

        # Cargar Tipografia -------------------------------------------------------------

        self.font_id = QFontDatabase.addApplicationFont(self.ruta_tipografia + "/Avilock.ttf")
        if self.font_id != -1:  # Verifica si la fuente se ha cargado correctamente
            self.LemonMocktail = QFontDatabase.applicationFontFamilies(self.font_id)[0]
            print("La fuente se ha cargado correctamente:", self.LemonMocktail)
        else:
            print("Error al cargar la fuente")
            self.LemonMocktail = "Arial"                                                                # Usar una fuente de respaldo

        # Colores Grises y rojos -----------------------------------------------------------

        self.ColorDark = '#22201F'                                                                      # Color oscuro del tema
        self.ColorLight = '#4a4643'                                                                     # Color claro del tema
        self.ColorTheme = '#CD6155'                                                                     # Color temático del tema

        #Colores Turquesa
        #self.ColorDark = '#006852'                                                                     # Color oscuro del tema
        #self.ColorLight = '#9EB0AD'                                                                    # Color claro del tema

        self.setWindowTitle('Energy Data')
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.ColorDark))                                       # Color hexadecimal
        self.setPalette(palette)
        self.showFullScreen()

        # Crear un layout de cuadrícula
        layout = QGridLayout()
        self.setLayout(layout)

        # HUB SUPERIOR
        Hub_superior = QWidget(self)
        Hub_superior.setStyleSheet(f"background-color: {self.ColorDark};")
        Hub_superior.setGeometry(300, 0, self.width(), 150)                                             # Se expande horizontalmente
        Hub_superior.setVisible(True)

        # HUB LATERAL
        Hub_lateral = QWidget(self)
        Hub_lateral.setStyleSheet(f"background-color: {self.ColorDark};")
        Hub_lateral.setGeometry(0, 0, 300, self.height())                                               # Se expande verticalmente
        Hub_lateral.setVisible(True)

        # PANEL PRINCIPAL
        self.Main_panel = QWidget(self)
        self.Main_panel.setStyleSheet(f"background-color: {self.ColorLight} ; border-radius: 30px;")
        self.Main_panel.setGeometry(305, 155, self.width()-335, self.height()-185)
        self.Main_panel.setVisible(True)
        self.Main_panel_layout = QGridLayout(self.Main_panel)
        self.Main_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.resolucionW = self.Main_panel.width()
        self.resolucionH = self.Main_panel.height()

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ICONOS HUB LATERAL XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        layout = QVBoxLayout(Hub_lateral)
        layout.setSpacing(10)                                                                   # Establecemos el espaciado vertical a 0
        layout.setAlignment(Qt.AlignTop)                                                        # Alineamos los widgets al principio del layout vertical

        spacer = QSpacerItem(75, 75)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

        # ICONO DE USUARIO ------------------------------------------------------------------------------

        cuadro_usuario = QWidget()
        #cuadro_usuario.setStyleSheet("background-color: blue;")                                      # Establece el color de fondo
        cuadro_usuario.setFixedSize(150, 150)
        layout.addWidget(cuadro_usuario, alignment=Qt.AlignCenter)                                    # Agrega el cuadro al layout vertical

        # Imagen de usuario
        pixmap_usuario = QPixmap(self.ruta_image + '/usuario1.png')
        icono_usuario = QLabel(cuadro_usuario)
        icono_usuario.setPixmap(pixmap_usuario)
        icono_usuario.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        icono_usuario.setGeometry(0, 0, cuadro_usuario.width(), cuadro_usuario.height())               # Alinea la imagen al centro vertical y horizontal del cuadro

       # NOMBRE DE USUARIO ------------------------------------------------------------------------------

        nombre_usuario = QWidget()
        #cuadro2.setStyleSheet("background-color: red;")                                               # Establece el color de fondo
        nombre_usuario.setFixedSize(250, 40)                                                           # Establece el tamaño fijo de cuadro
        layout.addWidget(nombre_usuario, alignment=Qt.AlignCenter)                                     # Alinea cuadro2 al centro vertical y horizontal

        # Texto del nombre
        text_label = QLabel("Joose15", nombre_usuario)
        text_label.setStyleSheet("color: white; font-size: 20px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        text_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        text_label.setGeometry(0, 0, nombre_usuario.width(), nombre_usuario.height())

        spacer = QSpacerItem(0, 110)                                                                  # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # OPCION HOME ------------------------------------------------------------------------------

        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_home = QPushButton()
        boton_home.setFixedSize(30, 30)                                                                 # Establecemos el tamaño fijo de cuadro3
        boton_home.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(boton_home)                                                               # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_home.png')
        image_icono = QLabel(boton_home)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_home.width(), boton_home.height())

        # TEXTO
        texto_home = QPushButton()
        texto_home.setStyleSheet("background-color: transparent; border: none;")                        # Establecemos el color de fondo amarillo
        texto_home.setFixedSize(220, 45)                                                                # Establecemos el tamaño fijo de cuadro4
        texto_home.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(texto_home)                                                               # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.home_label = QLabel("Mode", texto_home)
        self.home_label.setStyleSheet("color: white; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.home_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.home_label.setGeometry(0, 0, 150, texto_home.height())

        # BOTONES

        boton_home.clicked.connect(self.home)
        texto_home.clicked.connect(self.home)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

    # OPCION DASHBOARD ------------------------------------------------------------------------------

        spacer = QSpacerItem(20, 20)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)
        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_dash = QPushButton()
        boton_dash.setFixedSize(30, 30)                                                                 # Establecemos el tamaño fijo de cuadro3
        boton_dash.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(boton_dash)                                                               # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_dash3.png')
        image_icono = QLabel(boton_dash)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_dash.width(), boton_dash.height())

        # TEXTO
        texto_dash = QPushButton()
        texto_dash.setStyleSheet("background-color: transparent; border: none;")                        # Establecemos el color de fondo amarillo
        texto_dash.setFixedSize(220, 45)                                                                # Establecemos el tamaño fijo de cuadro4
        texto_dash.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(texto_dash)                                                               # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.dash_label = QLabel("Dashboard", texto_dash)
        self.dash_label.setStyleSheet("color: white; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.dash_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.dash_label.setGeometry(0, 0, 150, texto_dash.height())

        # BOTONES

        boton_dash.clicked.connect(self.Dashboard)
        texto_dash.clicked.connect(self.Dashboard)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

    # OPCION ANALYSIS ------------------------------------------------------------------------------

        spacer = QSpacerItem(20, 20)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)
        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_analysis = QPushButton()
        boton_analysis.setFixedSize(30, 30)                                                             # Establecemos el tamaño fijo de cuadro3
        boton_analysis.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(boton_analysis)                                                           # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_graph.png')
        image_icono = QLabel(boton_analysis)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_analysis.width(), boton_analysis.height())

        # TEXTO
        texto_analysis = QPushButton()
        texto_analysis.setStyleSheet("background-color: transparent; border: none;")                    # Establecemos el color de fondo amarillo
        texto_analysis.setFixedSize(220, 45)                                                            # Establecemos el tamaño fijo de cuadro4
        texto_analysis.setCursor(Qt.PointingHandCursor)
        hbox_layout.addWidget(texto_analysis)                                                           # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.analysis_label = QLabel("Analysis", texto_analysis)
        self.analysis_label.setStyleSheet("color: white; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.analysis_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.analysis_label.setGeometry(0, 0, 150, texto_analysis.height())


        boton_analysis.clicked.connect(self.Analysis)                                                   # Conectar la señal clicked del botón al manejador de eventos
        texto_analysis.clicked.connect(self.Analysis)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

    # OPCION DOCUMENT ------------------------------------------------------------------------------

        spacer = QSpacerItem(20, 20)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)
        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_document = QPushButton()
        boton_document.setFixedSize(30, 30)                                                             # Establecemos el tamaño fijo de cuadro3
        hbox_layout.addWidget(boton_document)
        boton_document.setCursor(Qt.PointingHandCursor)                                                           # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_document.png')
        image_icono = QLabel(boton_document)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_document.width(), boton_document.height())

        # TEXTO
        texto_document = QPushButton()
        texto_document.setStyleSheet("background-color: transparent; border: none;")                    # Establecemos el color de fondo amarillo
        texto_document.setFixedSize(220, 45)
        texto_document.setCursor(Qt.PointingHandCursor)                                                             # Establecemos el tamaño fijo de cuadro4
        hbox_layout.addWidget(texto_document)                                                           # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.document_label = QLabel("Document", texto_document)
        self.document_label.setStyleSheet("color: white; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.document_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.document_label.setGeometry(0, 0, 150, texto_document.height())

        boton_document.clicked.connect(self.Document)                                                   # Conectar la señal clicked del botón al manejador de eventos
        texto_document.clicked.connect(self.Document)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

    # OPCION REPORT ------------------------------------------------------------------------------

        spacer = QSpacerItem(20, 20)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)
        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_report = QPushButton()
        boton_report.setFixedSize(30, 30)                                                             # Establecemos el tamaño fijo de cuadro3
        hbox_layout.addWidget(boton_report)
        boton_report.setCursor(Qt.PointingHandCursor)                                                           # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_report_dis.png')
        image_icono = QLabel(boton_report)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_report.width(), boton_report.height())

        # TEXTO
        texto_report = QPushButton()
        texto_report.setStyleSheet("background-color: transparent; border: none;")                    # Establecemos el color de fondo amarillo
        texto_report.setFixedSize(220, 45)
        texto_report.setCursor(Qt.PointingHandCursor)                                                             # Establecemos el tamaño fijo de cuadro4
        hbox_layout.addWidget(texto_report)                                                           # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.Report_label = QLabel("Report", texto_report)
        self.Report_label.setStyleSheet("color: #767575; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.Report_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.Report_label.setGeometry(0, 0, 150, texto_report.height())

        #boton_report.clicked.connect(self.Report)                                                   # Conectar la señal clicked del botón al manejador de eventos
        #texto_report.clicked.connect(self.Report)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

    # OPCION AJUSTES ------------------------------------------------------------------------------

        spacer = QSpacerItem(20, Hub_lateral.height() - 900)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)
        hbox_layout = QHBoxLayout()                                                                     # Crea layout para recuadro

        hbox_layout.addSpacing(50)                                                                      # Agrega un espacio horizontal para separar los cuadros

        # ICONO

        boton_settings = QPushButton()
        boton_settings.setFixedSize(30, 30)
        boton_settings.setCursor(Qt.PointingHandCursor)                                                               # Establecemos el tamaño fijo de cuadro3
        hbox_layout.addWidget(boton_settings)
                                                                  # Agregamos cuadro3 al layout horizontal

        # Imagen
        pixmap = QPixmap(self.ruta_icons + '\icono_settings.png')
        image_icono = QLabel(boton_settings)
        image_icono.setPixmap(pixmap)
        image_icono.setAlignment(Qt.AlignCenter)                                                        # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        image_icono.setGeometry(0, 0, boton_settings.width(), boton_settings.height())

        # TEXTO
        texto_settings = QPushButton()
        texto_settings.setStyleSheet("background-color: transparent; border: none;")                    # Establecemos el color de fondo amarillo
        texto_settings.setFixedSize(220, 45)
        texto_settings.setCursor(Qt.PointingHandCursor)                                                              # Establecemos el tamaño fijo de cuadro4
        hbox_layout.addWidget(texto_settings)                                                           # Agregamos cuadro4 al layout horizontal

        # Texto del nombre
        self.settings_label = QLabel("Settings", texto_settings)
        self.settings_label.setStyleSheet("color: white; font-size: 19px;")                                      # Establece el color blanco y el tamaño de fuente a 20px
        self.settings_label.setAlignment(Qt.AlignCenter)                                                         # Alinea el texto al centro tanto horizontal como verticalmente
        self.settings_label.setGeometry(0, 0, 150, texto_settings.height())


        boton_settings.clicked.connect(self.Settings)                                                   # Conectar la señal clicked del botón al manejador de eventos
        texto_settings.clicked.connect(self.Settings)

        # Agregamos el layout horizontal al layout vertical
        layout.addLayout(hbox_layout)

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ICONOS HUB SUPERIOR XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        layout = QHBoxLayout(Hub_superior)
        layout.setSpacing(10)                                                                   # Establecemos el espaciado vertical a 0
        layout.setAlignment(Qt.AlignLeft)                                                        # Alineamos los widgets al principio del layout vertical

        spacer = QSpacerItem(Hub_superior.width()-1020,0)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # ICONO DE START ------------------------------------------------------------------------------

        # Crear el botón sin texto
        self.boton_start = QPushButton()
        self.boton_start.setFixedSize(75, 75)
        self.boton_start.setStyleSheet(f"background-color: {self.ColorTheme}; border-radius: 37px;")
        self.boton_start.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.boton_start, alignment=Qt.AlignCenter)

        # Configurar el ícono inicial
        self.set_icon(self.ruta_icons + "\icono_play.png")

        # Conectar la señal clicked al método InicioMedidas
        self.boton_start.clicked.connect(self.InicioMedidas)


        spacer = QSpacerItem(100,0)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # ICONO DE SQL ------------------------------------------------------------------------------

        boton_sql = QPushButton()
        boton_sql.setFixedSize(75, 75)
        boton_sql.setStyleSheet(f"background-color: {self.ColorLight}; border-radius: 37px;")       # Establecer el botón como circular
        boton_sql.setCursor(Qt.PointingHandCursor)                                                  # Cambiar el cursor al pasar sobre el botón
        layout.addWidget(boton_sql, alignment=Qt.AlignCenter)

        # Imagen

        pixmap_sql = QPixmap(self.ruta_icons + '\icono_sql.png')
        icono_sql = QLabel(boton_sql)
        icono_sql.setPixmap(pixmap_sql)
        icono_sql.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        icono_sql.setGeometry(int((boton_sql.width() - pixmap_sql.width()) / 2),
                          int((boton_sql.height() - pixmap_sql.height()) / 2),
                          pixmap_sql.width(), pixmap_sql.height())

        # Funcion de los botones
        boton_sql.clicked.connect(self.SQL)

        spacer = QSpacerItem(40,0)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # ICONO DE PDF ------------------------------------------------------------------------------

        boton_pdf = QPushButton()                                   # Establece el color de fondo
        boton_pdf.setFixedSize(75, 75)
        boton_pdf.setStyleSheet(f"background-color: {self.ColorLight}; border-radius: 37px;")
        boton_pdf.setCursor(Qt.PointingHandCursor)
        layout.addWidget(boton_pdf, alignment=Qt.AlignCenter)



        # Imagen de usuario
        pixmap_pdf = QPixmap(self.ruta_icons + '\icono_pdf.png')
        icono_pdf = QLabel(boton_pdf)
        icono_pdf.setPixmap(pixmap_pdf)
        icono_pdf.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_pdf.setGeometry(int((boton_pdf.width() - pixmap_pdf.width()) / 2),
                          int((boton_pdf.height() - pixmap_pdf.height()) / 2),
                          pixmap_pdf.width(), pixmap_pdf.height())

        # Funcion de los botones
        boton_pdf.clicked.connect(self.Datasheet)

        spacer = QSpacerItem(40,0)                                                                  # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # ICONO DE TABLE ------------------------------------------------------------------------------

        boton_excel = QPushButton()
        boton_excel.setFixedSize(75, 75)
        boton_excel.setStyleSheet(f"background-color: {self.ColorLight}; border-radius: 37px;")
        boton_excel.setCursor(Qt.PointingHandCursor)

        layout.addWidget(boton_excel, alignment=Qt.AlignCenter)

                                          # Agrega el cuadro al layout vertical

        # Imagen de usuario
        pixmap_excel = QPixmap(self.ruta_icons + '\icono_table.png')
        icono_excel = QLabel(boton_excel)
        icono_excel.setPixmap(pixmap_excel)
        icono_excel.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_excel.setGeometry(int((boton_excel.width() - pixmap_excel.width()) / 2),
                          int((boton_excel.height() - pixmap_excel.height()) / 2),
                          pixmap_excel.width(), pixmap_excel.height())

        # Funcion de los botones
        boton_excel.clicked.connect(self.Excel)

        spacer = QSpacerItem(40,0)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

    # ICONO DE NOTAS ------------------------------------------------------------------------------

        boton_txt = QPushButton()                                     # Establece el color de fondo
        boton_txt.setFixedSize(75, 75)
        boton_txt.setStyleSheet(f"background-color: {self.ColorLight}; border-radius: 37px;")
        boton_txt.setCursor(Qt.PointingHandCursor)
        layout.addWidget(boton_txt, alignment=Qt.AlignCenter)

                                          # Agrega el cuadro al layout vertical

        # Imagen de usuario
        pixmap_txt = QPixmap(self.ruta_icons + '\icono_notes.png')
        icono_txt = QLabel(boton_txt)
        icono_txt.setPixmap(pixmap_txt)
        icono_txt.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_txt.setGeometry(int((boton_txt.width() - pixmap_txt.width()) / 2),
                          int((boton_txt.height() - pixmap_txt.height()) / 2),
                          pixmap_txt.width(), pixmap_txt.height())


        boton_txt.clicked.connect(self.txt)

        spacer = QSpacerItem(40,0)                                                                    # Creamos un espacio de 75 píxeles
        layout.addItem(spacer)

        self.home()

    # OPCIONES DEL MENU -------------------------------------------------------

    def home(self):
        self.limpiar_layout(self.Main_panel_layout)

        # Desaparecer boton de START
        self.boton_start.setVisible(False)

        # Destacar texto
        self.home_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")  
        self.dash_label.setStyleSheet(f"color: white; font-size: 19px;")  
        self.analysis_label.setStyleSheet(f"color: white; font-size: 19px;")
        self.document_label.setStyleSheet(f"color: white; font-size: 19px;")
        self.settings_label.setStyleSheet(f"color: white; font-size: 19px;")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX POSICIONES DE CONTENEDORES XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 0, 0)

        # TITULO

        titulo_label = QLabel("MODE")

        font = QFont(self.LemonMocktail)
        font.setPointSize(35)
        titulo_label.setFont(font)
        titulo_label.setStyleSheet("color: white; padding-left: 50px; margin-top=0px;")

        self.Main_panel_layout.addWidget(titulo_label,1,0)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 2, 0)

        # PANEL DEL BOTONES ---------------------------------------------------------------------------------------------------

        botones_panel = QWidget(self.Main_panel)                                                                    # Declaro el widget
        botones_panel.setStyleSheet("background-color: transparent;")                                                       # Color del panel
        botones_panel.setFixedSize(self.Main_panel.width()-25,100)                                                  # Tamaño del panel
        self.Main_panel_layout.addWidget(botones_panel, 3, 0)                                                       # Añadir fila1 al MainPanel

        botones_panel_layout = QGridLayout(botones_panel)                                                           # Crea layout del primera fila
        botones_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.Main_panel_layout.addLayout(botones_panel_layout, 1, 0)

        # PANEL DE OPCIONES ---------------------------------------------------------------------------------------------------

        self.panel_opciones = QWidget()
        self.panel_opciones.setStyleSheet("background-color: transparent;")
        self.panel_opciones.setGeometry(20, 5, 10, 10)
        self.panel_opciones.setFixedSize(self.Main_panel.width() - 30, self.Main_panel.height() - 235)
        self.Main_panel_layout.addWidget(self.panel_opciones, 4, 0)  

        self.layout_panel_opciones = QHBoxLayout(self.panel_opciones)
        self.layout_panel_opciones.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.Main_panel_layout.addLayout(self.layout_panel_opciones, 2, 0)

        self.scroll_area_home = QScrollArea()
        self.scroll_area_home.setWidgetResizable(True)
        self.scroll_area_home.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX BOTONES OPCIONES XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        # BOTON DE TACTIL   -------------------------------------------------------------------------------------------------------

        self.boton_tactil = QPushButton(botones_panel)                                   # Establece el color de fondo
        self.boton_tactil.setFixedSize(75, 75)
        self.boton_tactil.setStyleSheet(f"background-color: {self.ColorTheme}; border-radius: 37px;")
        self.boton_tactil.setCursor(Qt.PointingHandCursor)
        self.boton_tactil.setGeometry(botones_panel.width()-125,0,10,10)

        # Imagen de usuario
        pixmap_tactil = QPixmap(self.ruta_icons + '\icono_tactil.png')
        icono_tactil = QLabel(self.boton_tactil)
        icono_tactil.setPixmap(pixmap_tactil)
        icono_tactil.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_tactil.setGeometry(int((self.boton_tactil.width() - pixmap_tactil.width()) / 2),
                          int((self.boton_tactil.height() - pixmap_tactil.height()) / 2),
                          pixmap_tactil.width(), pixmap_tactil.height())
        

        self.boton_tactil.clicked.connect(self.opcionTactil)


        # BOTON DE MANDO   -------------------------------------------------------------------------------------------------------

        self.boton_mando = QPushButton(botones_panel)                                   # Establece el color de fondo
        self.boton_mando.setFixedSize(75, 75)
        self.boton_mando.setStyleSheet(f"background-color: {self.ColorTheme}; border-radius: 37px;")
        self.boton_mando.setCursor(Qt.PointingHandCursor)
        self.boton_mando.setGeometry(botones_panel.width()-225,0,10,10)

        # Imagen de usuario
        pixmap_mando = QPixmap(self.ruta_icons + '\icono_control.png')
        icono_mando = QLabel(self.boton_mando)
        icono_mando.setPixmap(pixmap_mando)
        icono_mando.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_mando.setGeometry(int((self.boton_mando.width() - pixmap_mando.width()) / 2),
                          int((self.boton_mando.height() - pixmap_mando.height()) / 2),
                          pixmap_mando.width(), pixmap_mando.height())

        self.boton_mando.clicked.connect(self.opcionMando)

    def Dashboard(self):

        self.limpiar_layout(self.Main_panel_layout)

        # Desaparecer boton de START
        self.boton_start.setVisible(True)

        # Destacar texto
        self.home_label.setStyleSheet("color: white; font-size: 19px;") 
        self.dash_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")  
        self.analysis_label.setStyleSheet("color: white; font-size: 19px;")
        self.document_label.setStyleSheet("color: white; font-size: 19px;")
        self.settings_label.setStyleSheet("color: white; font-size: 19px;")

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX POSICIONES DE CONTENEDORES XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 0, 0)

        # TITULO

        titulo_label = QLabel("DASHBOARD")

        font = QFont(self.LemonMocktail)
        font.setPointSize(35)
        titulo_label.setFont(font)
        titulo_label.setStyleSheet("color: white; padding-left: 50px; margin-top=0px;")


        self.Main_panel_layout.addWidget(titulo_label,1,0)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 2, 0)

    # FILA 1 DEL PANEL ----------------------------------------------------------------------------------------

        row_1_main = QWidget(self.Main_panel)                                                           # Declaro el widget
        row_1_main.setStyleSheet("background-color: transparent;")                                      # Color del panel
        row_1_main.setFixedSize(self.Main_panel.width()-25,310)                                         # Tamaño del panel
        self.Main_panel_layout.addWidget(row_1_main, 3, 0)                                              # Añadir fila1 al MainPanel

        row_1_main_layout = QGridLayout(self.Main_panel)                                                # Crea layout del primera fila
        row_1_main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.Main_panel_layout.addLayout(row_1_main_layout, 1, 0)                                      # Alineado arriba izquierda

        # ESPACIO
        spacer_vertical = QSpacerItem(0, 10)                                                            # Cambia el valor 20 según el espacio deseado
        self.Main_panel_layout.addItem(spacer_vertical, 4, 0)

    # FILA 2 DEL PANEL ----------------------------------------------------------------------------------------

        row_2_main = QWidget(self.Main_panel)                                                               # Declaro el widget
        row_2_main.setStyleSheet("background-color: transparent;")                                          # Color del panel
        row_2_main.setFixedSize(self.Main_panel.width()-25, self.Main_panel.height()-445)                                         # Tamaño del panel
        self.Main_panel_layout.addWidget(row_2_main, 5, 0)                                                  # Añadir fila1 al MainPanel

        row_2_main_layout = QGridLayout(self.Main_panel)                                                    # Crea layout del primera fila
        row_2_main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)                                          # Alineado arriba izquierda
        self.Main_panel_layout.addLayout(row_2_main_layout, 2, 0)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ELEMENTOS FILA 1 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        self.panelW = 495
        self.panelH = 285

    # Panel Voltaje-------------------------------------------
        voltaje_panel = QWidget(row_1_main)
        voltaje_panel.setStyleSheet("background-color: #CD6155;")
        voltaje_panel.setGeometry(20,5,10,10)
        voltaje_panel.setFixedSize(self.panelW,self.panelH)

        # Titulo
        self.titulo_voltaje_cont = QWidget(voltaje_panel)
        self.titulo_voltaje_cont.setStyleSheet("background-color: transparent;")
        self.titulo_voltaje_cont.setGeometry(0,30,self.panelW - 20,60)
        self.titulo_voltaje_cont_layout = QVBoxLayout(self.titulo_voltaje_cont)
        self.titulo_voltaje_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Valor
        self.valor_voltaje_cont = QWidget(voltaje_panel)
        self.valor_voltaje_cont.setStyleSheet("background-color: transparent;")
        self.valor_voltaje_cont.setGeometry(0,80,self.panelW - 20,170)
        self.layout_voltaje_panel = QVBoxLayout(self.valor_voltaje_cont)
        self.layout_voltaje_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_voltaje = QLabel("VOLTAJE")
        self.texto_voltaje = QLabel("00,00 V")

        self.DimenionLabel(self.titulo_voltaje, 30, "white", self.titulo_voltaje_cont_layout, self.panelW)
        self.DimenionLabel(self.texto_voltaje, 60, "white", self.layout_voltaje_panel, self.panelW)

    # Panel Corriente -------------------------------------------

        corriente_panel = QWidget(row_1_main)
        corriente_panel.setStyleSheet("background-color: #CD6155;")
        corriente_panel.setGeometry(535,5,10,10)
        corriente_panel.setFixedSize(self.panelW,self.panelH)

        # Titulo
        self.titulo_corriente_cont = QWidget(corriente_panel)
        self.titulo_corriente_cont.setStyleSheet("background-color: transparent;")
        self.titulo_corriente_cont.setGeometry(0,30,self.panelW - 20,60)
        self.titulo_corriente_cont_layout = QVBoxLayout(self.titulo_corriente_cont)
        self.titulo_corriente_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Valor
        self.valor_corriente_cont = QWidget(corriente_panel)
        self.valor_corriente_cont.setStyleSheet("background-color: transparent;")
        self.valor_corriente_cont.setGeometry(0,80,self.panelW - 20,170)
        self.layout_corriente_panel = QVBoxLayout(self.valor_corriente_cont)
        self.layout_corriente_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_corriente = QLabel("CORRIENTE")
        self.texto_corriente = QLabel("00,00 A")

        self.DimenionLabel(self.titulo_corriente, 30, "white", self.titulo_corriente_cont_layout, self.panelW)
        self.DimenionLabel(self.texto_corriente, 60, "white", self.layout_corriente_panel, self.panelW)

    # Panel Potencia -------------------------------------------

        potencia_panel = QWidget(row_1_main)
        potencia_panel.setStyleSheet("background-color: #CD6155;")
        potencia_panel.setGeometry(1050,5,10,10)
        potencia_panel.setFixedSize(self.panelW,self.panelH)

        # Titulo
        self.titulo_potencia_cont = QWidget(potencia_panel)
        self.titulo_potencia_cont.setStyleSheet("background-color: transparent;")
        self.titulo_potencia_cont.setGeometry(0,30,self.panelW - 20,60)
        self.titulo_potencia_cont_layout = QVBoxLayout(self.titulo_potencia_cont)
        self.titulo_potencia_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Valor
        self.valor_potencia_cont = QWidget(potencia_panel)
        self.valor_potencia_cont.setStyleSheet("background-color: transparent;")
        self.valor_potencia_cont.setGeometry(0,80,self.panelW - 20,170)
        self.layout_potencia_panel = QVBoxLayout(self.valor_potencia_cont)
        self.layout_potencia_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_potencia = QLabel("POTENCIA")
        self.texto_potencia = QLabel(f"00,00 W")

        self.DimenionLabel(self.titulo_potencia, 30, "white", self.titulo_potencia_cont_layout,self.panelW)
        self.DimenionLabel(self.texto_potencia, 60, "white", self.layout_potencia_panel,self.panelW)


# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ELEMENTOS FILA 2 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        self.auxpanelW = 490
        self.auxpanelH = 195

    # PANEL DEL GRÁFICO -------------------------------------------
        self.grafico_panel = QWidget(row_2_main)
        self.grafico_panel.setStyleSheet(f"background-color: {self.ColorLight};")
        self.grafico_panel.setGeometry(20,5,10,10)
        self.grafico_panel.setFixedSize(1000,430)

    # PANEL DE EFICIENCIA -------------------------------------------
        efiencia_panel = QWidget(row_2_main)
        efiencia_panel.setStyleSheet("background-color: white;")
        efiencia_panel.setGeometry(1055,10,10,10)
        efiencia_panel.setFixedSize(self.auxpanelW,self.auxpanelH)

        # Icono
        Icono_efficacy = QWidget(efiencia_panel)
        Icono_efficacy.setStyleSheet("background-color: transparent;")
        Icono_efficacy.setGeometry(40,60,10,10)
        Icono_efficacy.setFixedSize(80,80)

        # Imagen de usuario
        pixmap_efficacy = QPixmap(self.ruta_icons + '\icono_efficacy.png')
        pixmap_efficacy = pixmap_efficacy.scaled(Icono_efficacy.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)           # Redimensionar la imagen
        image_efficacy = QLabel(Icono_efficacy)
        image_efficacy.setPixmap(pixmap_efficacy)
        image_efficacy.setAlignment(Qt.AlignCenter)                                                                      # Alinear la imagen al centro del QLabel
        image_efficacy.setGeometry(0, 0, Icono_efficacy.width(), Icono_efficacy.height())
                                                                                                                              # Establecer la geometría del QLabel
        # Valor

        self.valor_efficacy = QWidget(efiencia_panel)
        self.valor_efficacy.setStyleSheet("background-color: transparent;")
        self.valor_efficacy.setGeometry(140,10,330,170)
        self.layout_efficay_panel = QHBoxLayout(self.valor_efficacy)
        self.layout_efficay_panel.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

        # Impresion Valor
        self.texto_efficacy = QLabel("48 %")
        self.DimenionLabel(self.texto_efficacy, 60, self.ColorTheme, self.layout_efficay_panel,self.auxpanelW-150)

    # PANEL DE TEMPERATURA -------------------------------------------
        temperature_panel = QWidget(row_2_main)
        temperature_panel.setStyleSheet("background-color: white;")
        temperature_panel.setGeometry(1055,225,10,10)
        temperature_panel.setFixedSize(self.auxpanelW,self.auxpanelH)

        # Icono
        Icono_temperature = QWidget(temperature_panel)
        Icono_temperature.setStyleSheet("background-color: transparent;")
        Icono_temperature.setGeometry(40,60,10,10)
        Icono_temperature.setFixedSize(80,80)

        # Imagen de usuario
        pixmap_usuario = QPixmap(self.ruta_icons + '\icono_temperature2.png')
        pixmap_usuario = pixmap_usuario.scaled(Icono_temperature.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)           # Redimensionar la imagen
        image_temperature = QLabel(Icono_temperature)
        image_temperature.setPixmap(pixmap_usuario)
        image_temperature.setAlignment(Qt.AlignCenter)                                                                      # Alinear la imagen al centro del QLabel
        image_temperature.setGeometry(0, 0, Icono_temperature.width(), Icono_temperature.height())
                                                                                                                              # Establecer la geometría del QLabel
        # Valor

        self.valor_temperature = QWidget(temperature_panel)
        self.valor_temperature.setStyleSheet("background-color: transparent;")
        self.valor_temperature.setGeometry(140,10,330,170)
        self.layout_temperature_panel = QHBoxLayout(self.valor_temperature)
        self.layout_temperature_panel.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

        # Impresion Valor
        self.texto_temperature = QLabel("00,00 cº")
        self.DimenionLabel(self.texto_temperature, 45, self.ColorTheme, self.layout_temperature_panel,self.auxpanelW-150)

        self.instanciar_grafico(self.grafico_panel)

    def Analysis(self):

        if self.BtimerMedidas:
            self.finalizar_medidas()
        
        self.boton_start.setVisible(False)
        self.limpiar_layout(self.Main_panel_layout)

        # Destacar texto
        self.home_label.setStyleSheet(f"color: white; font-size: 19px;")
        self.dash_label.setStyleSheet(f"color: white; font-size: 19px;")  
        self.analysis_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")
        self.document_label.setStyleSheet(f"color: white; font-size: 19px;")
        self.settings_label.setStyleSheet(f"color: white; font-size: 19px;")

        self.filtroGraph = ""
        self.filtroParameters = ""

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 0, 0)

        # TITULO -----------------------------------------------------------------------------------------------------------

        titulo_label = QLabel("ANALYSIS")

        font = QFont(self.LemonMocktail)                                                                       # Crear un objeto QFont con la fuente cargad)
        font.setPointSize(35)
        titulo_label.setFont(font)
        titulo_label.setStyleSheet("color: white; padding-left: 50px; margin-top=0px;")
        titulo_label.setMinimumSize(300, 50)

        self.Main_panel_layout.addWidget(titulo_label,1,0)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 2, 0)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx CONTENEDORES PANELES xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # PANEL DEL FILTRO ---------------------------------------------------------------------------------------------------

        filtro_panel = QWidget(self.Main_panel)                                                                 # Declaro el widget
        filtro_panel.setStyleSheet("background-color: transparent;")                                            # Color del panel
        filtro_panel.setFixedSize(self.Main_panel.width()-25,100)                                               # Tamaño del panel
        self.Main_panel_layout.addWidget(filtro_panel, 3, 0)                                                    # Añadir fila1 al MainPanel

        filtro_panel_layout = QGridLayout(filtro_panel)                                                         # Crea layout del primera fila
        filtro_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.Main_panel_layout.addLayout(filtro_panel_layout, 1, 0)

        # RECUADRO DE FILTRO
        self.filtro_grafico = QPushButton("SELECCIONA UN GRÁFICO", filtro_panel)
        self.filtro_grafico.setStyleSheet(f"background-color: {self.ColorTheme}; color: white;")
        self.filtro_grafico.setGeometry(50, 5, 10, 10)
        self.filtro_grafico.setFixedSize(300, 70)
        self.filtro_grafico.setCursor(Qt.PointingHandCursor)

        font = QFont(self.LemonMocktail)
        font.setPointSize(18)
        self.filtro_grafico.setFont(font)

        self.filtro_grafico.clicked.connect(self.menu_graficos)

        # ESPACIO
        spacer_vertical = QSpacerItem(0, 10)                                                                    # Cambia el valor 20 según el espacio deseado
        self.Main_panel_layout.addItem(spacer_vertical, 4, 0)

    # GRAFICO y TABLA ---------------------------------------------------------------------------------------------------

        self.dash_panel = QWidget(self.Main_panel)
        self.dash_panel.setStyleSheet("background-color: transparent;")
        self.dash_panel.setFixedSize(self.Main_panel.width()-25, self.Main_panel.height()-250)
        self.Main_panel_layout.addWidget(self.dash_panel, 5, 0)

        self.dash_panel_layout = QGridLayout(self.Main_panel)
        self.dash_panel_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.Main_panel_layout.addLayout(self.dash_panel_layout, 2, 0)                                               # Establecer el layout en dash_panel

    # PANEL DEL TABLA ---------------------------------------------------------------------------------------------------

        self.table_panel = QWidget(self.dash_panel)
        self.table_panel.setStyleSheet(f"background-color: white;")
        self.table_panel.setGeometry(self.dash_panel.width()-560,5,10,10)
        self.table_panel.setFixedSize(560,self.dash_panel.height()-20)
        self.layout_table_panel = QHBoxLayout(self.table_panel)
        self.layout_table_panel.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

    # PANEL DEL GRAFICO ---------------------------------------------------------------------------------------------------

        self.dash_grafico_panel = QWidget(self.dash_panel)
        self.dash_grafico_panel.setStyleSheet(f"background-color: transparent;")
        self.dash_grafico_panel.setGeometry(5,5,10,10)
        self.dash_grafico_panel.setFixedSize(980,self.dash_panel.height()-10)

        self.layout_dash_grafico_panel = QGridLayout(self.dash_grafico_panel)
        self.layout_dash_grafico_panel.setAlignment(Qt.AlignTop | Qt.AlignLeft)


# xxxxxxxxxxxxxxxxxxxxxxxxxxxx ELEMENTOS CONTENEDORES XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # BOTON DE EXPORTAR

        self.boton_export = QPushButton(filtro_panel)                                   # Establece el color de fondo
        self.boton_export.setFixedSize(75, 75)
        self.boton_export.setStyleSheet(f"background-color: {self.ColorTheme}; border-radius: 37px;")
        self.boton_export.setCursor(Qt.PointingHandCursor)
        self.boton_export.setGeometry(filtro_panel.width()-125,0,10,10)

        # Imagen de usuario
        pixmap_export = QPixmap(self.ruta_icons + '\icono_export.png')
        icono_export = QLabel(self.boton_export)
        icono_export.setPixmap(pixmap_export)
        icono_export.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_export.setGeometry(int((self.boton_export.width() - pixmap_export.width()) / 2),
                          int((self.boton_export.height() - pixmap_export.height()) / 2),
                          pixmap_export.width(), pixmap_export.height())
        
        if self.historialMedidas:
            self.boton_export.clicked.connect(lambda: self.exportar_medidas(self.historialMedidas))


    # BOTON DE FILTRO

        self.boton_filter = QPushButton(filtro_panel)                                   # Establece el color de fondo
        self.boton_filter.setFixedSize(75, 75)
        self.boton_filter.setStyleSheet(f"background-color: {self.ColorTheme}; border-radius: 37px;")
        self.boton_filter.setCursor(Qt.PointingHandCursor)
        self.boton_filter.setGeometry(filtro_panel.width()-225,0,10,10)

        # Imagen de usuario
        pixmap_export = QPixmap(self.ruta_icons + '\icono_filter.png')
        icono_export = QLabel(self.boton_filter)
        icono_export.setPixmap(pixmap_export)
        icono_export.setAlignment(Qt.AlignCenter)                                                     # Alineamos la imagen al centro de cuadro1 horizontal y verticalmente
        # Centrar el QLabel dentro del QPushButton
        icono_export.setGeometry(int((self.boton_filter.width() - pixmap_export.width()) / 2),
                          int((self.boton_filter.height() - pixmap_export.height()) / 2),
                          pixmap_export.width(), pixmap_export.height())

        self.boton_filter.clicked.connect(self.menu_parametros)

    # TABLA DE VALORES----------------------------------------------------------------------------------------------------------------------------------------------------

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)                                                                    # Permitir que el widget dentro del área de desplazamiento cambie de tamaño

        # Crear un widget para contener la tabla
        table_widget_container = QWidget()
        table_widget_container_layout = QVBoxLayout(table_widget_container)

        # Crear una tabla
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)                                                                     # Definir el número de columnas

        font = self.table_widget.font()                                                                         # Obtener la fuente actual de la tabla
        font.setPointSize(10)                                                                                   # Establecer el tamaño de la fuente a 14 puntos

        self.table_widget.setHorizontalHeaderLabels(["VOLTAJE", "CORRIENTE", "POTENCIA", "TEMPERATURA"])        # Etiquetas de las columnas

        for row, data in enumerate(self.historialMedidas):
            self.table_widget.insertRow(row)
            for col, (key, value) in enumerate(data.items()):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)
                if item is not None:
                    item.setFont(font)

        table_widget_container_layout.addWidget(self.table_widget)                                              # Agregar la tabla al widget contenedor
        table_widget_container_layout.setAlignment(Qt.AlignCenter)                                              # Centrar la tabla dentro del contenedor

        scroll_area.setWidget(table_widget_container)                                                           # Agregar el widget contenedor al área de desplazamiento
        self.layout_table_panel.addWidget(scroll_area)                                                          # Agregar el área de desplazamiento al layout del panel de la tabla

        if not self.historialMedidas:                                                                           # En caso de que la lista de medidas este vacia
            print("nada")
            
        else:
            self.Multi_Graph()

    def Document(self):

        if self.BtimerMedidas:
            self.finalizar_medidas()
        
        self.boton_start.setVisible(False)
        self.limpiar_layout(self.Main_panel_layout)

        # Destacar texto
        self.home_label.setStyleSheet("color: white; font-size: 19px;")
        self.dash_label.setStyleSheet("color: white; font-size: 19px;")  
        self.analysis_label.setStyleSheet("color: white; font-size: 19px;")
        self.document_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")
        self.settings_label.setStyleSheet("color: white; font-size: 19px;")

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 0, 0)

        # TITULO -----------------------------------------------------------------------------------------------------------

        titulo_label = QLabel("DOCUMENT")

        font = QFont(self.LemonMocktail)                                                                       # Crear un objeto QFont con la fuente cargad)
        font.setPointSize(35)
        titulo_label.setFont(font)
        titulo_label.setStyleSheet("color: white; padding-left: 50px; margin-top=0px;")
        titulo_label.setMinimumSize(300, 50)

        self.Main_panel_layout.addWidget(titulo_label,1,0)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 2, 0)

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxx SCROLL AREA  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        self.panel_area = QWidget()
        self.panel_area.setStyleSheet("background-color: transparent;")
        self.panel_area.setGeometry(20, 5, 10, 10)
        self.panel_area.setFixedSize(self.Main_panel.width() - 50, self.Main_panel.height() - 150)

        self.layout_panel_area = QVBoxLayout(self.panel_area)
        self.layout_panel_area.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.Main_panel_layout.addWidget(self.panel_area, 3, 0)

        self.scroll_area_document = QScrollArea()
        self.scroll_area_document.setWidgetResizable(True)
        self.scroll_area_document.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)                                  # Establece la política de la barra de desplazamiento horizontal

        # xxxxxxxxxxxxxxxxxxxxxxxxxxxx ELEMENTOS SCROLL AREA  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        container_widget = QWidget()
        container_layout = QVBoxLayout()

        container_widget.setLayout(container_layout)

        self.scroll_area_document.setWidget(container_widget)
        self.layout_panel_area.addWidget(self.scroll_area_document)

        self.update_iconos(container_layout)

    def Report(self, dataframe):

        if self.BtimerMedidas:
            self.finalizar_medidas()
        
        # Destacar texto
        self.home_label.setStyleSheet("color: white; font-size: 19px;")
        self.dash_label.setStyleSheet("color: white; font-size: 19px;")  
        self.analysis_label.setStyleSheet("color: white; font-size: 19px;")
        self.document_label.setStyleSheet("color: white; font-size: 19px;")
        self.settings_label.setStyleSheet("color: white; font-size: 19px;")
        self.Report_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")

        self.boton_start.setVisible(False)
        self.limpiar_layout(self.Main_panel_layout)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 0, 0)

        # TITULO -----------------------------------------------------------------------------------------------------------

        titulo_label = QLabel("ANALYSIS")

        font = QFont(self.LemonMocktail)                                                                       # Crear un objeto QFont con la fuente cargad)
        font.setPointSize(35)
        titulo_label.setFont(font)
        titulo_label.setStyleSheet("color: white; padding-left: 50px; margin-top=0px;")
        titulo_label.setMinimumSize(300, 50)

        self.Main_panel_layout.addWidget(titulo_label,1,0)

        spacer_vertical = QSpacerItem(0, 25)
        self.Main_panel_layout.addItem(spacer_vertical, 2, 0)

     # xxxxxxxxxxxxxxxxxxxxxxxxxxxx SCROLL AREA  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        self.analysis_area = QWidget()
        self.analysis_area.setStyleSheet("background-color: white;")
        self.analysis_area.setGeometry(20, 5, 10, 10)
        self.analysis_area.setFixedSize(self.Main_panel.width() - 50, self.Main_panel.height() - 150)

        self.layout_analysis_area = QVBoxLayout(self.analysis_area)
        self.layout_analysis_area.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.Main_panel_layout.addWidget(self.analysis_area, 3, 0)

        self.scroll_area_analysis = QScrollArea()
        self.scroll_area_analysis.setWidgetResizable(True)
        self.scroll_area_analysis.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)                                  # Establece la política de la barra de desplazamiento horizontal

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxx ELEMENTOS SCROLL AREA  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        container_widget = QWidget()
        container_layout = QVBoxLayout()

        container_widget.setLayout(container_layout)

        self.scroll_area_analysis.setWidget(container_widget)
        self.layout_analysis_area.addWidget(self.scroll_area_analysis)

        chart = self.create_table_chart(self.excel_df)

        canvas = FigureCanvas(chart)
        canvas.draw()
        img = QImage(canvas.buffer_rgba(), canvas.buffer_rgba().shape[1], canvas.buffer_rgba().shape[0], QImage.Format_RGBA8888)

        label = QLabel()
        label.setPixmap(QPixmap.fromImage(img))
        self.scroll_area_analysis.setWidget(label)
        self.layout_analysis_area.addWidget(self.scroll_area_analysis)
        self.layout_analysis_area.addWidget(self.scroll_area_analysis)  
    
    def Settings(self):

         # Destacar texto
        self.home_label.setStyleSheet("color: white; font-size: 19px;")
        self.dash_label.setStyleSheet("color: white; font-size: 19px;")  
        self.analysis_label.setStyleSheet("color: white; font-size: 19px;")
        self.document_label.setStyleSheet("color: white; font-size: 19px;")
        self.settings_label.setStyleSheet(f"color: {self.ColorTheme}; font-size: 19px;")
        print("Settings")

    # OPCIONES DEL HUB SUPERIOR --------------------------------------------------------------------------------------------------------------------------------

        self.move_scrollbar(50)

    def SQL(self):
        print("SQL")

    def Datasheet(self):
        print("Datasheet")

    def Excel(self):

        ruta_excel = self.open_file_dialog()                        # Obtenemos la ruta del excel

        if not ruta_excel.endswith('.xlsx'):
            print("TIPO NO ACEPTADO")
        else:
            self.excel_df = pd.read_excel(ruta_excel)                        
            self.Analysis(self.excel_df)

    def txt(self):
        print("txt")

    # PERSONALIZACIÓN ----------------------------------------------------------------------------------------------------------------------------------------

    def limpiar_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def expandir_pantalla(self):
            # Obtener la geometría de la pantalla
            screen_geometry = QApplication.desktop().screenGeometry()
            # Establecer la geometría del panel principal para llenar toda la pantalla
            self.Main_panel.setGeometry(screen_geometry)
            print(self.Main_panel.width())

    def DimenionLabel(self, label, tamaño, color, layout, panel):

        font = QFont(self.LemonMocktail)                                                       # Crear un objeto QFont con la fuente cargad)
        font.setPointSize(tamaño)
        label.setFont(font)
        label.setStyleSheet(f"color: {color};")
        label.setMinimumSize(panel - 20, 50)
        label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)  # Alineación al centro vertical y horizontal
        layout.addWidget(label)

    def set_icon(self, icon_path):
        # Configurar el ícono del botón
        pixmap = QPixmap(icon_path)
        icon = QIcon(pixmap)
        self.boton_start.setIcon(icon)
        self.boton_start.setIconSize(pixmap.size())

    # OBTENCION DE VALORES ------------------------------------------------------------------------------------------------------------------------------------

    def obtener_valores(self):

        voltaje =  round(random.uniform(11, 12),3)
        corriente = round(random.uniform(0, 1),3)
        potencia = round(voltaje*corriente,3)
        temperatura = round(random.uniform(24, 25),2)

        return voltaje, corriente, potencia, temperatura

    def InicioMedidas(self):

        if self.boton_start.icon().pixmap(QSize(75, 75)).toImage() == QPixmap(self.ruta_icons + "\icono_play.png").toImage():           # Comprobar que el icono es el de start
            self.BtimerMedidas = True                                                                                                   # Booleano de medidas a True
            self.historialMedidas = []                                                                                                  # Elimina las medidas anteriores
            self.set_icon(self.ruta_icons + "\icono_stop.png")                                                                          # Establece el icono de stop
            self.timerMedidas = QTimer()                                                                                                # Crear un QTimer
            self.timerMedidas.timeout.connect(self.actualizar_valores)                                                                  # Conectar la señal de timeout al método de actualización
            self.timerMedidas.start(1000)                                                                                               # Iniciar el temporizador con un intervalo de 1000 milisegundos (1 segundo)
        else:
            
            self.finalizar_medidas()

    def actualizar_valores(self):
        
        self.voltaje, self.corriente, self.potencia, self.temperatura = self.obtener_valores()

        self.actualizar_grafico(self.voltaje)

        # Actualizar los parámetros en la interfaz gráfica
        self.texto_voltaje.setText(f"{str(self.voltaje)} V")
        self.texto_corriente.setText(f"{str(self.corriente)} A")
        self.texto_potencia.setText(f"{str(self.potencia)} W")
        self.texto_temperature.setText(f"{str(self.temperatura)} cº")

        # Almacenar las medidas en el historial
        self.historialMedidas = self.almacenar_medidas(self.voltaje, self.corriente, self.potencia, self.temperatura, self.historialMedidas)

        self.cont_graph_act += 1

    def finalizar_medidas(self):

        self.set_icon(self.ruta_icons + "\icono_play.png")

        if hasattr(self, 'timerMedidas'):                                                                              # Detener el temporizador si está definido
            self.timerMedidas.stop()
            self.BtimerMedidas = False                                                                                 # Booleano de medidas a False

            # Inicializa los valores a 0 (fabrica)
            self.texto_voltaje.setText(f"{str(00.00)} V")
            self.texto_corriente.setText(f"{str(00.00)} A")
            self.texto_potencia.setText(f"{str(00.00)} W")
            self.texto_temperature.setText(f"{str(00.00)} cº")

            self.x_graph_act=[]
            self.y_graph_act=[]

    def almacenar_medidas(self, voltaje, corriente, potencia, temperatura, historial):

        historial.append({"Voltaje": voltaje, "Corriente": corriente, "Potencia": potencia, "Temperatura": temperatura})
        return historial

    def exportar_medidas(self,historial):

        # Convertir el diccionario a un DataFrame de pandas
        df = pd.DataFrame(historial)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # Construir el nombre del archivo
        nombre_archivo = f"/lista_guardada {fecha_actual}.xlsx"

        df.to_excel(self.ruta_Documents + nombre_archivo, index=False)

    # GRAFICOS -----------------------------------------------------------------------------------------------------------------------------------------------
        
    def grafico(self, panel, historial, parametro, color, opcion, layout, grafico, filtro):
        self.dash_grafico_panel.setStyleSheet(f"background-color: {self.ColorTheme};")

        df = pd.DataFrame(historial)

        # Obtener los datos del DataFrame
        x = np.arange(len(df))                                              # Cantidad de filas del DataFrame
        y = df[parametro]                                                   # Columna del DataFrame

    # LINEAS
        if grafico == 0:

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, color=color, linewidth=2)
            titulo = ax.set_title(parametro.upper())
            titulo.set_color('white')
    # BARRAS
        elif grafico == 1:

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(x, y, color=color, linewidth=2)
            titulo = ax.set_title(parametro.upper())
            titulo.set_color('white')
    # AREAS
        elif grafico == 2:

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.fill_between(x, y, color=color, alpha=0.5, linewidth=2)
            titulo = ax.set_title(parametro.upper())
            titulo.set_color('white')

    # DISPERSION
        elif grafico == 3:

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x, y, color=color, s=50, alpha=0.5)                  # s es el tamaño de los puntos
            titulo = ax.set_title(parametro.upper())
            titulo.set_color('white')

        # Configuraciones adicionales
        fig.patch.set_facecolor('none')
        fig.patch.set_alpha(0)

        ax.set_facecolor('none')
        ax.fill_between(x, y, color='none')

        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['left'].set_linewidth(0.5)

        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)

        ax.xaxis.set_tick_params(labelcolor='white')
        ax.yaxis.set_tick_params(labelcolor='white')

        canvas = FigureCanvas(fig)                                          # Creamos un lienzo para el gráfico de Matplotlib

        if opcion == 0:
            toolbar = NavigationToolbar2QT(canvas, panel)                   # Agregamos la barra de herramientas de navegación
            layout = QVBoxLayout(panel)                                     # Creamos un layout vertical para el panel

            container = QWidget()                                           # Creamos un widget contenedor para el lienzo y la barra de herramientas
            container.setLayout(layout)
            layout.addWidget(canvas)
            layout.addWidget(toolbar)

            panel.setLayout(layout)                                         # Agregamos el widget contenedor al layout vertical del panel

        elif opcion == 1:
            # Agregamos la barra de herramientas de navegación
            toolbar = NavigationToolbar2QT(canvas, self)

            # Agregamos el lienzo y la barra de herramientas al layout
            layout.addWidget(canvas, 0, 0)
            layout.addWidget(toolbar, 1, 0)

    def Multi_Graph(self):

        self.scroll_area_graph = QScrollArea()
        self.scroll_area_graph.setWidgetResizable(True)
    
        container_widget = QWidget()
        container_layout = QVBoxLayout()                                                                        # Usa un QVBoxLayout para organizar verticalmente tus paneles

    # PANELES DE GRAFICOS
        panel_tension = QWidget()
        panel_tension.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_tension.setFixedSize(self.dash_grafico_panel.width() - 75, self.panelH + 150)

        panel_corriente = QWidget()
        panel_corriente.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_corriente.setFixedSize(self.dash_grafico_panel.width() - 75, self.panelH + 150)

        panel_potencia = QWidget()
        panel_potencia.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_potencia.setFixedSize(self.dash_grafico_panel.width() - 75, self.panelH + 150)

        panel_temperatura = QWidget()
        panel_temperatura.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_temperatura.setFixedSize(self.dash_grafico_panel.width() - 75, self.panelH + 150)

    # CONTENEDORES DE PANELES
        container_layout.addWidget(panel_tension)
        container_layout.addSpacing(20)
        container_layout.addWidget(panel_corriente)
        container_layout.addSpacing(20)
        container_layout.addWidget(panel_potencia)
        container_layout.addSpacing(20)
        container_layout.addWidget(panel_temperatura)

        container_widget.setLayout(container_layout)                                                                # Establece el layout del contenedor

        self.scroll_area_graph.setWidget(container_widget)                                                          # Establece el contenedor como el widget del QScrollArea
        self.scroll_area_graph.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)                                  # Establece la política de la barra de desplazamiento horizontal

        self.layout_dash_grafico_panel.addWidget(self.scroll_area_graph)                                            # Agrega el QScrollArea al layout principal

    # GRÁFICOS

        self.grafico(panel_tension, self.historialMedidas,'Voltaje','white',0,0,0,0)
        self.grafico(panel_corriente, self.historialMedidas,'Corriente','white',0,0,0,0)
        self.grafico(panel_potencia, self.historialMedidas,'Potencia','white',0,0,0,0)
        self.grafico(panel_temperatura, self.historialMedidas,'Temperatura','white',0,0,0,0)
            
    def menu_parametros(self):
        mostrar_filtro = QMenu()

        # Crear las acciones del menú con su respectiva tipografía
        accion_voltaje = QAction("VOLTAJE", mostrar_filtro)
        font_voltaje = accion_voltaje.font()
        font_voltaje.setPointSize(14)  # Establecer el tamaño de la tipografía
        accion_voltaje.setFont(font_voltaje)

        accion_corriente = QAction("CORRIENTE", mostrar_filtro)
        font_corriente = accion_corriente.font()
        font_corriente.setPointSize(14)
        accion_corriente.setFont(font_corriente)

        accion_potencia = QAction("POTENCIA", mostrar_filtro)
        font_potencia = accion_potencia.font()
        font_potencia.setPointSize(14)
        accion_potencia.setFont(font_potencia)

        accion_temperatura = QAction("TEMPERATURA", mostrar_filtro)
        font_temperatura = accion_temperatura.font()
        font_temperatura.setPointSize(14)
        accion_temperatura.setFont(font_temperatura)

        accion_todos = QAction("SIN FILTROS", mostrar_filtro)
        font_todos = accion_todos.font()
        font_todos.setPointSize(14)
        accion_todos.setFont(font_todos)


        # Conectar las acciones a una función cuando se seleccionen
        accion_voltaje.triggered.connect(lambda: self.aplicar_filtro_parametros("Voltaje"))
        accion_corriente.triggered.connect(lambda: self.aplicar_filtro_parametros("Corriente"))
        accion_potencia.triggered.connect(lambda: self.aplicar_filtro_parametros("Potencia"))
        accion_temperatura.triggered.connect(lambda: self.aplicar_filtro_parametros("Temperatura"))
        accion_todos.triggered.connect(lambda: self.aplicar_filtro_parametros("SIN FILTROS"))

        # Agregar las acciones al menú desplegable
        mostrar_filtro.addAction(accion_voltaje)
        mostrar_filtro.addAction(accion_corriente)
        mostrar_filtro.addAction(accion_potencia)
        mostrar_filtro.addAction(accion_temperatura)
        mostrar_filtro.addSeparator()
        mostrar_filtro.addAction(accion_todos)

        mostrar_filtro.exec_(self.boton_filter.mapToGlobal(self.boton_filter.rect().bottomLeft()))

    def menu_graficos(self):
        filtro_graficos = QMenu()

        # Crear las acciones del menú con su respectiva tipografía
        accion_lineas = QAction("LINEAS", filtro_graficos)
        font_lineas = accion_lineas.font()
        font_lineas.setPointSize(14)  # Establecer el tamaño de la tipografía
        accion_lineas.setFont(font_lineas)

        accion_barras = QAction("BARRAS", filtro_graficos)
        font_barras = accion_barras.font()
        font_barras.setPointSize(14)
        accion_barras.setFont(font_barras)

        accion_disp = QAction("DISPERSION", filtro_graficos)
        font_disp = accion_disp.font()
        font_disp.setPointSize(14)
        accion_disp.setFont(font_disp)

        accion_areas = QAction("AREAS", filtro_graficos)
        font_areas = accion_areas.font()
        font_areas.setPointSize(14)
        accion_areas.setFont(font_areas)

        # Conectar las acciones a una función cuando se seleccionen
        accion_lineas.triggered.connect(lambda: self.aplicar_filtro_graph("LINEAS"))
        accion_barras.triggered.connect(lambda: self.aplicar_filtro_graph("BARRAS"))
        accion_disp.triggered.connect(lambda: self.aplicar_filtro_graph("DISPERSION"))
        accion_areas.triggered.connect(lambda: self.aplicar_filtro_graph("AREAS"))

        # Agregar las acciones al menú desplegable
        filtro_graficos.addAction(accion_lineas)
        filtro_graficos.addAction(accion_barras)
        filtro_graficos.addAction(accion_disp)
        filtro_graficos.addAction(accion_areas)

        # Mostrar el menú desplegable en la posición del botón
        filtro_graficos.exec_(self.filtro_grafico.mapToGlobal(self.filtro_grafico.rect().bottomLeft()))

    def aplicar_filtro_graph(self, action):
            if self.historialMedidas != []:
                self.limpiar_layout(self.layout_dash_grafico_panel)

                self.filtroGraph = action
                self.filtro_grafico.setText(action)

                if(self.filtroGraph == 'SIN FILTROS'):
                    self.Multi_Graph()
                elif (self.filtroGraph == 'LINEAS'):
                    self.grafico(self.dash_grafico_panel, self.historialMedidas,'Voltaje','white',1,self.layout_dash_grafico_panel,0,0)
                elif (self.filtroGraph == 'BARRAS'):
                    self.grafico(self.dash_grafico_panel, self.historialMedidas,'Voltaje','white',1,self.layout_dash_grafico_panel,1,0)
                elif (self.filtroGraph == 'AREAS'):
                    self.grafico(self.dash_grafico_panel, self.historialMedidas,'Voltaje','white',1,self.layout_dash_grafico_panel,2,0)
                elif (self.filtroGraph == 'DISPERSION'):
                    self.grafico(self.dash_grafico_panel, self.historialMedidas,'Voltaje','white',1,self.layout_dash_grafico_panel,3,0)

    def aplicar_filtro_parametros(self, action):
        if self.historialMedidas and self.filtroGraph != "":

            self.limpiar_layout(self.layout_dash_grafico_panel)
            self.filtroParameters = action

            if(self.filtroGraph == 'LINEAS'):
                opcion_graph = 0
            elif(self.filtroGraph == 'BARRAS'):
                opcion_graph = 1
            elif(self.filtroGraph == 'AREAS'):
                opcion_graph = 2
            elif(self.filtroGraph == 'DISPERSION'):
                opcion_graph = 3

            if(self.filtroParameters == 'SIN FILTROS'):
                self.grafico(self.dash_grafico_panel, self.historialMedidas,self.filtroParameters,'white',1,self.layout_dash_grafico_panel,opcion_graph,1)
            else:
                self.grafico(self.dash_grafico_panel, self.historialMedidas,self.filtroParameters,'white',1,self.layout_dash_grafico_panel,opcion_graph,0)
  
    def instanciar_grafico(self, panel):
        
        self.figure_act, self.ax_act = plt.subplots(figsize=(10, 6))                                                        # Crea la figura y los ejes del gráfico
        
        
        self.canvas_act = FigureCanvas(self.figure_act)                                                                     # Crea el lienzo del gráfico
        
        
        self.figure_act.patch.set_facecolor('none')                                                                         # Configura el fondo del gráfico y el lienzo
        self.figure_act.patch.set_alpha(0)
        self.ax_act.set_facecolor('none')
        
        
        self.line_act, = self.ax_act.plot(self.x_graph_act, self.y_graph_act, color=self.ColorTheme, marker='o')            # Graficar los datos iniciales (vacío)

        # ESTILOS INICIALES

        self.ax_act.spines['top'].set_linewidth(0)
        self.ax_act.spines['right'].set_linewidth(0)
        self.ax_act.spines['bottom'].set_linewidth(0.5)
        self.ax_act.spines['left'].set_linewidth(0.5)

        self.ax_act.spines['top'].set_color('white')
        self.ax_act.spines['right'].set_color('white')
        self.ax_act.spines['bottom'].set_color('white')
        self.ax_act.spines['left'].set_color('white')

        self.ax_act.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
        self.ax_act.xaxis.set_tick_params(labelcolor='white')
        self.ax_act.yaxis.set_tick_params(labelcolor='white')

        toolbar = NavigationToolbar2QT(self.canvas_act, panel)

        layout = QVBoxLayout(panel)
        self.figure_act.tight_layout()

        # CONTENENDORES Y LAYOUTS

        container = QWidget()
        container.setLayout(layout)
        layout.addWidget(self.canvas_act)
        layout.addWidget(toolbar)

        panel.setLayout(layout)

    def actualizar_grafico(self, parametro):

        # Agregar el nuevo valor a los datos del gráfico
        self.x_graph_act.append(len(self.x_graph_act) + 1)
        self.y_graph_act.append(parametro)

        # Limitar la cantidad de puntos mostrados para mantener el gráfico actualizado
        if len(self.x_graph_act) > 100:
            self.x_graph_act = self.x_graph_act[-100:]
            self.y_graph_act = self.y_graph_act[-100:]

        # Actualizar los datos de la línea del gráfico
        self.line_act.set_xdata(self.x_graph_act)
        self.line_act.set_ydata(self.y_graph_act)

        # Ajustar los ejes x e y
        self.figure_act.gca().set_xlim(0, max(10, len(self.x_graph_act)))
        self.actualizar_ejes_y(parametro)

        # Redibujar el gráfico
        self.canvas_act.draw()

    def actualizar_ejes_y(self, parametro):
        # Actualizar los límites del eje y
        min_y = min(self.y_graph_act)
        max_y = max(self.y_graph_act)

        if min_y < self.y_min:
            self.y_min = min_y
        if max_y > self.y_max:
            self.y_max = max_y

        self.figure_act.gca().set_ylim(0, parametro+5)

    # DOCUMENTS -------------------------------------------------------------------------------------------------------------------------------------------------
    
    def update_iconos(self, container_layout):

        cuadrados_por_fila = 6
        cuadrados_agregados = 0
        fila_layout = None

        items_documentos = os.listdir(self.ruta_Documents)                                                          # Obtengo lista de los nombres de los elementos de la carpeta    

        for item in items_documentos:                                                                               # Paso por cada uno de los elementos
            
            cuadrado_layout = QVBoxLayout()
            boton = QPushButton()                                                                                   # Crear QPushButton para el icono
            
        # ICONOS
            
            if item.endswith('.xlsx'):
                ruta = self.ruta_icons + '/archivo_excel'
            elif item.endswith('.pdf'):
                ruta = self.ruta_icons + '/archivo_pdf'
            elif item.endswith('.png'):
                ruta = self.ruta_icons + '/archivo_png'
            else:
                ruta = self.ruta_icons + '/archivo_png'

            print(item)

            boton.setIcon(QIcon(ruta))                                                                              # Configurar el ícono
            boton.setIconSize(QSize(150, 150))                                                                      # Establecer el tamaño del ícono
            
            
            file_label = QLabel(item)
            file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)                                                   # Alineación al centro
            file_label.setStyleSheet("color: white; font-size: 9pt;")
            file_label.setFixedSize(150,50)                                                                         # Permitir que el QLabel se expanda verticalmente
            file_label.setWordWrap(True)

            boton.clicked.connect(lambda _, item=item: self.open_folder(item))                                      # Capturar el nombre del ítem como un valor predeterminado

            # Agregar botones al layout vertical
            cuadrado_layout.addWidget(boton, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            cuadrado_layout.addWidget(file_label)

            # Agregar layout vertical a la fila_layout
            if cuadrados_agregados % cuadrados_por_fila == 0:
                fila_layout = QHBoxLayout()
                fila_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)                                                # Alineación a la izquierda
                fila_layout.setContentsMargins(80, 50, 0, 0)
                container_layout.addLayout(fila_layout)
            else:
                fila_layout.addSpacing(80)                                                                          # Espacio entre cuadrados

            fila_layout.addLayout(cuadrado_layout)
            cuadrados_agregados += 1

            if cuadrados_agregados % cuadrados_por_fila == 0 and cuadrados_agregados < 29:
                spacer_item = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
                container_layout.addItem(spacer_item)

        self.setLayout(container_layout)

    def open_folder(self,item):
        try:

            ruta_archivo = f"{self.ruta_Documents}\{item}"                          # Ruta del archivo
            subprocess.Popen(["start", "", ruta_archivo], shell=True)               # Sentencia para abrir archivos

        except Exception as e:
            print("Error al abrir el archivo:", e)
        
    # REPORT -------------------------------------------------------------------------------------------------------------------------------------------------
            
    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.Detail)
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                return file_path
                
        else:
            print("No se seleccionó ningún archivo.")
        
    def create_table_chart(self,df):
        # Crear un gráfico de tabla usando pandas
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))
        plt.close(fig)  # Cerrar la figura para que no se muestre

        return fig
    
    # ANALYSIS -------------------------------------------------------------------------------------------------------------------------------------------------

    def opcionTactil(self):

        container_widget = QWidget()
        container_layout = QHBoxLayout()                                                                        # Usa un QVBoxLayout para organizar verticalmente tus paneles

    # VOLTAJE DC ---------------------------------------------

        # Panel
        panel_tensionDC = QPushButton()
        panel_tensionDC.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_tensionDC.setFixedSize(self.panel_opciones.width() - 700, self.panel_opciones.height() -200)

        # Titulo
        self.titulo_voltajeDC_cont = QWidget(panel_tensionDC)
        self.titulo_voltajeDC_cont.setStyleSheet("background-color: transparent;")
        self.titulo_voltajeDC_cont.setGeometry(0,0,panel_tensionDC.width(),panel_tensionDC.height())
        self.titulo_voltajeDC_cont_layout = QVBoxLayout(self.titulo_voltajeDC_cont)
        self.titulo_voltajeDC_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_voltajeDC = QLabel("VOLTAJE")
        self.DC = QLabel("DC")
        self.DimenionLabel(self.titulo_voltajeDC, 80, "white", self.titulo_voltajeDC_cont_layout, panel_tensionDC.width())
        self.DimenionLabel(self.DC, 80, "white", self.titulo_voltajeDC_cont_layout, panel_tensionDC.width())
        
        panel_tensionDC.clicked.connect(self.Settings)

    # CORRIENTE DC ---------------------------------------------

        # Panel
        panel_corrienteDC = QWidget()
        panel_corrienteDC.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_corrienteDC.setFixedSize(self.panel_opciones.width() - 700, self.panel_opciones.height() -200)

        # Titulo
        self.titulo_corrienteDC_cont = QWidget(panel_corrienteDC)
        self.titulo_corrienteDC_cont.setStyleSheet("background-color: transparent;")
        self.titulo_corrienteDC_cont.setGeometry(0,0,panel_corrienteDC.width(),panel_corrienteDC.height())
        self.titulo_corrienteDC_cont_layout = QVBoxLayout(self.titulo_corrienteDC_cont)
        self.titulo_corrienteDC_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_corrienteDC = QLabel("CORRIENTE")
        self.DC = QLabel("DC")
        self.DimenionLabel(self.titulo_corrienteDC, 80, "white", self.titulo_corrienteDC_cont_layout, panel_corrienteDC.width())
        self.DimenionLabel(self.DC, 80, "white", self.titulo_corrienteDC_cont_layout, panel_corrienteDC.width())
        
    # VOLTAJE AC ---------------------------------------------

        # Panel
        panel_voltajeAC = QWidget()
        panel_voltajeAC.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_voltajeAC.setFixedSize(self.panel_opciones.width() - 700, self.panel_opciones.height() -200)

        # Titulo
        self.titulo_voltajeAC_cont = QWidget(panel_voltajeAC)
        self.titulo_voltajeAC_cont.setStyleSheet("background-color: transparent;")
        self.titulo_voltajeAC_cont.setGeometry(0,0,panel_voltajeAC.width(),panel_voltajeAC.height())
        self.titulo_voltajeAC_cont_layout = QVBoxLayout(self.titulo_voltajeAC_cont)
        self.titulo_voltajeAC_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_voltajeAC = QLabel("VOLTAJE")
        self.AC = QLabel("AC")
        self.DimenionLabel(self.titulo_voltajeAC, 80, "white", self.titulo_voltajeAC_cont_layout, panel_voltajeAC.width())
        self.DimenionLabel(self.AC, 80, "white", self.titulo_voltajeAC_cont_layout, panel_voltajeAC.width())

    # CORRIENTE AC ---------------------------------------------

        # Panel
        panel_corrienteAC = QWidget()
        panel_corrienteAC.setStyleSheet(f"background-color: {self.ColorTheme};")
        panel_corrienteAC.setFixedSize(self.panel_opciones.width() - 700, self.panel_opciones.height() -200)

        # Titulo
        self.titulo_corrienteAC_cont = QWidget(panel_corrienteAC)
        self.titulo_corrienteAC_cont.setStyleSheet("background-color: transparent;")
        self.titulo_corrienteAC_cont.setGeometry(0,0,panel_corrienteAC.width(),panel_corrienteAC.height())
        self.titulo_corrienteAC_cont_layout = QVBoxLayout(self.titulo_corrienteAC_cont)
        self.titulo_corrienteAC_cont_layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # Impresion Valor
        self.titulo_corrienteAC = QLabel("CORRIENTE")
        self.AC = QLabel("AC")
        self.DimenionLabel(self.titulo_corrienteAC, 80, "white", self.titulo_corrienteAC_cont_layout, panel_corrienteAC.width())
        self.DimenionLabel(self.AC, 80, "white", self.titulo_corrienteAC_cont_layout, panel_corrienteAC.width())



    # CONTENEDORES DE PANELES
        container_layout.addWidget(panel_tensionDC)
        container_layout.addSpacing(50)
        container_layout.addWidget(panel_corrienteDC)
        container_layout.addSpacing(50)
        container_layout.addWidget(panel_voltajeAC)
        container_layout.addSpacing(50)
        container_layout.addWidget(panel_corrienteAC)

        container_widget.setLayout(container_layout)                                                                # Establece el layout del contenedor

        self.scroll_area_home.setWidget(container_widget)                                                          # Establece el contenedor como el widget del QScrollArea                                  # Establece la política de la barra de desplazamiento horizontal

        self.layout_panel_opciones.addWidget(self.scroll_area_home)                                            # Agrega el QScrollArea al layout principal

    def opcionMando(self):
        print("Mando")

    def move_scrollbar(self, delta):
        # Obtener la posición actual del scrollbar
        current_value = self.scroll_area_home.horizontalScrollBar().value()

        # Calcular la nueva posición
        new_value = current_value + delta

        # Asegurarse de que la nueva posición esté dentro de los límites
        max_value = self.scroll_area_home.horizontalScrollBar().maximum()
        new_value = min(max_value, max(0, new_value))

        # Establecer la nueva posición del scrollbar
        self.scroll_area_home.horizontalScrollBar().setValue(new_value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())
