import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QHBoxLayout, QLineEdit, QListWidget, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont


# Widget para dibujar
class CabeceraRanita(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ojos (Verde exterior)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(181, 204, 127)))
        painter.drawEllipse(88, 13, 44, 44)
        painter.drawEllipse(228, 13, 44, 44)

        # Pupilas (Negro)
        painter.setBrush(QBrush(QColor(20, 20, 20)))
        painter.drawEllipse(94, 19, 32, 32)
        painter.drawEllipse(234, 19, 32, 32)

        # Brillos de los ojos (Blanco)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(99, 24, 12, 12)
        painter.drawEllipse(239, 24, 12, 12)

        # Mejillas Rosadas
        painter.setBrush(QBrush(QColor(255, 150, 170)))
        painter.drawEllipse(63, 40, 30, 16)
        painter.drawEllipse(267, 40, 30, 16)

        # Boca
        painter.setBrush(QBrush(QColor(20, 20, 20)))
        painter.drawChord(QRectF(145, 28, 70, 40), 0 * 16, -180 * 16)

        # Lengua
        painter.setBrush(QBrush(QColor(255, 140, 160)))
        painter.drawChord(QRectF(155, 40, 50, 26), 0 * 16, -180 * 16)


# Clases Base para la Calculadora Ranita
class BaseCalculadoraRanita(QMainWindow):
    def __init__(self, titulo="Calculadora Ranita "):
        super().__init__()
        self.setWindowTitle(f"{titulo} - Brisa Maribel V.")
        self.historial = []
        self.en_estado_error = False
        self.aplicar_estilos()

    def conectar_boton(self, btn, texto):
        if texto == 'C':
            btn.clicked.connect(self.limpiar)
        elif texto == 'CE':
            btn.clicked.connect(self.borrar_ultimo)
        elif texto == '=':
            btn.clicked.connect(self.calcular)
        elif texto == 'Info':
            btn.clicked.connect(self.abrir_info)
        elif texto == '√':
            btn.clicked.connect(lambda: self.agregar_caracter("math.sqrt("))
        elif texto == '^':
            btn.clicked.connect(lambda: self.agregar_caracter("**"))
        elif texto == 'π':
            btn.clicked.connect(lambda: self.agregar_caracter("math.pi"))
        elif texto in ['sin', 'cos', 'tan']:
            btn.clicked.connect(lambda t=texto: self.agregar_caracter(f"math.{t}(math.radians("))
        else:
            btn.clicked.connect(lambda _, t=texto: self.agregar_caracter(t))

    def agregar_caracter(self, char):
        if self.en_estado_error:
            return
        self.display.setText(self.display.text() + char)

    def limpiar(self):
        self.display.setText("")
        self.en_estado_error = False

    def borrar_ultimo(self):
        if self.en_estado_error:
            return
        texto = self.display.text()
        if texto:
            self.display.setText(texto[:-1])

    def calcular(self):
        if self.en_estado_error:
            return

        expr = self.display.text()
        if not expr:
            return

        try:
            res = eval(expr, {"__builtins__": None, "math": math}, {})
            if isinstance(res, float) and res.is_integer():
                res = int(res)

            res_str = str(res)
            self.actualizar_historial(f"{expr} = {res_str}")
            self.display.setText(res_str)
        except Exception:
            self.display.setText("Error")
            self.en_estado_error = True

    def actualizar_historial(self, operacion):
        self.historial.append(operacion)
        if len(self.historial) > 5:
            self.historial.pop(0)

        self.list_historial.clear()
        self.list_historial.addItems(self.historial)

    def cargar_desde_historial(self, item):
        texto = item.text()
        if "=" in texto:
            resultado = texto.split("=")[-1].strip()
            self.display.setText(resultado)
            self.en_estado_error = False

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #b5cc7f;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                background-color: #c8e1e6;
                color: #222222;
                border: none;
                border-radius: 12px;
                padding: 8px 12px;
            }
            QListWidget {
                background-color: #a8c072;
                color: #1a1a1a;
                border: none;
                border-radius: 10px;
                padding: 4px;
                font-size: 11px;
            }
            QListWidget::item:selected {
                background-color: #f4b41a;
                color: #ffffff;
                border-radius: 4px;
            }
            QPushButton#btn_blanco {
                background-color: #f0f0f0;
                color: #333333;
                border: none;
                border-radius: 14px;
            }
            QPushButton#btn_blanco:hover {
                background-color: #ffffff;
            }
            QPushButton#btn_blanco:pressed {
                background-color: #d8d8d8;
            }
            QPushButton#btn_amarillo {
                background-color: #f4b41a;
                color: #ffffff;
                border: none;
                border-radius: 14px;
            }
            QPushButton#btn_amarillo:hover {
                background-color: #ffc52d;
            }
            QPushButton#btn_amarillo:pressed {
                background-color: #dc9f0e;
            }
        """)

    def abrir_info(self):
        QMessageBox.information(
            self,
            "Información",
            "Calculadora Ranita 🐸\n"
            "Autor: Brisa Maribel V.\n"
            "Librería: PySide6 (Qt)"
        )


# Ventana Estándar
class VentanaEstandar(BaseCalculadoraRanita):
    def __init__(self):
        super().__init__("Modo Estándar")
        self.setFixedSize(380, 580)
        self.iniciar_ui()

    def iniciar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(15, 10, 15, 15)
        layout_principal.setSpacing(6)

        layout_principal.addWidget(CabeceraRanita())

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout_principal.addWidget(self.display)

        lbl_historial = QLabel("Historial (Doble clic para cargar):")
        lbl_historial.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout_principal.addWidget(lbl_historial)

        self.list_historial = QListWidget()
        self.list_historial.setFixedHeight(65)
        self.list_historial.itemDoubleClicked.connect(self.cargar_desde_historial)
        layout_principal.addWidget(self.list_historial)

        layout_botones = QHBoxLayout()
        grid_izq = QGridLayout()

        botones_izq = [
            ('C', 0, 0, "amarillo"),  ('CE', 0, 1, "amarillo"), ('/', 0, 2, "amarillo"),
            ('7', 1, 0, "blanco"),    ('8', 1, 1, "blanco"),    ('9', 1, 2, "blanco"),
            ('4', 2, 0, "blanco"),    ('5', 2, 1, "blanco"),    ('6', 2, 2, "blanco"),
            ('1', 3, 0, "blanco"),    ('2', 3, 1, "blanco"),    ('3', 3, 2, "blanco"),
            ('0', 4, 0, "blanco"),    ('.', 4, 1, "blanco"),    ('Info', 4, 2, "blanco")
        ]

        for texto, fila, col, tipo in botones_izq:
            btn = QPushButton(texto)
            btn.setObjectName(f"btn_{tipo}")
            btn.setFixedHeight(42)
            btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_izq.addWidget(btn, fila, col)

        grid_der = QGridLayout()
        ops = [('*', 0), ('-', 1), ('+', 2)]
        for texto, fila in ops:
            btn = QPushButton(texto)
            btn.setObjectName("btn_amarillo")
            btn.setFixedHeight(42)
            btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_der.addWidget(btn, fila, 0)

        btn_eq = QPushButton("=")
        btn_eq.setObjectName("btn_amarillo")
        btn_eq.setFixedHeight(90)
        btn_eq.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.conectar_boton(btn_eq, "=")
        grid_der.addWidget(btn_eq, 3, 0, 2, 1)

        layout_botones.addLayout(grid_izq, stretch=3)
        layout_botones.addLayout(grid_der, stretch=1)
        layout_principal.addLayout(layout_botones)


# Ventana Científica
class VentanaCientifica(BaseCalculadoraRanita):
    def __init__(self):
        super().__init__("Modo Científico")
        self.setFixedSize(380, 660)
        self.iniciar_ui()

    def iniciar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(15, 10, 15, 15)
        layout_principal.setSpacing(6)

        layout_principal.addWidget(CabeceraRanita())

        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout_principal.addWidget(self.display)

        lbl_historial = QLabel("Historial (Doble clic para cargar):")
        lbl_historial.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        layout_principal.addWidget(lbl_historial)

        self.list_historial = QListWidget()
        self.list_historial.setFixedHeight(60)
        self.list_historial.itemDoubleClicked.connect(self.cargar_desde_historial)
        layout_principal.addWidget(self.list_historial)

        # Panel Científico Adicional
        grid_cientifico = QGridLayout()
        grid_cientifico.setSpacing(6)
        botones_cien = [
            ('√', 0, 0), ('^', 0, 1), ('π', 0, 2),
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2)
        ]
        for texto, fila, col in botones_cien:
            btn = QPushButton(texto)
            btn.setObjectName("btn_amarillo")
            btn.setFixedHeight(35)
            btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_cientifico.addWidget(btn, fila, col)

        layout_principal.addLayout(grid_cientifico)

        # Botones Estándar
        layout_botones = QHBoxLayout()
        grid_izq = QGridLayout()

        botones_izq = [
            ('C', 0, 0, "amarillo"),  ('CE', 0, 1, "amarillo"), ('/', 0, 2, "amarillo"),
            ('7', 1, 0, "blanco"),    ('8', 1, 1, "blanco"),    ('9', 1, 2, "blanco"),
            ('4', 2, 0, "blanco"),    ('5', 2, 1, "blanco"),    ('6', 2, 2, "blanco"),
            ('1', 3, 0, "blanco"),    ('2', 3, 1, "blanco"),    ('3', 3, 2, "blanco"),
            ('0', 4, 0, "blanco"),    ('.', 4, 1, "blanco"),    ('Info', 4, 2, "blanco")
        ]

        for texto, fila, col, tipo in botones_izq:
            btn = QPushButton(texto)
            btn.setObjectName(f"btn_{tipo}")
            btn.setFixedHeight(40)
            btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_izq.addWidget(btn, fila, col)

        grid_der = QGridLayout()
        ops = [('*', 0), ('-', 1), ('+', 2)]
        for texto, fila in ops:
            btn = QPushButton(texto)
            btn.setObjectName("btn_amarillo")
            btn.setFixedHeight(40)
            btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            self.conectar_boton(btn, texto)
            grid_der.addWidget(btn, fila, 0)

        btn_eq = QPushButton("=")
        btn_eq.setObjectName("btn_amarillo")
        btn_eq.setFixedHeight(86)
        btn_eq.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.conectar_boton(btn_eq, "=")
        grid_der.addWidget(btn_eq, 3, 0, 2, 1)

        layout_botones.addLayout(grid_izq, stretch=3)
        layout_botones.addLayout(grid_der, stretch=1)
        layout_principal.addLayout(layout_botones)


# Ventana Principal (Menú Selector de Ventanas)
class VentanaMenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ranita App - Brisa Maribel V.")
        self.setFixedSize(320, 260)

        # Referencias para las subventanas
        self.win_estandar = None
        self.win_cientifica = None

        self.iniciar_ui()
        self.aplicar_estilos()

    def iniciar_ui(self):
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout = QVBoxLayout(widget_central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl_titulo = QLabel("Calculadora")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(lbl_titulo)

        lbl_autor = QLabel("Autor: Brisa Maribel V.")
        lbl_autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_autor.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(lbl_autor)

        btn_estandar = QPushButton("Abrir Modo Estándar")
        btn_estandar.setObjectName("btn_amarillo")
        btn_estandar.setFixedHeight(45)
        btn_estandar.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn_estandar.clicked.connect(self.abrir_estandar)
        layout.addWidget(btn_estandar)

        btn_cientifico = QPushButton("Abrir Modo Científico")
        btn_cientifico.setObjectName("btn_blanco")
        btn_cientifico.setFixedHeight(45)
        btn_cientifico.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn_cientifico.clicked.connect(self.abrir_cientifico)
        layout.addWidget(btn_cientifico)

    def abrir_estandar(self):
        if self.win_estandar is None or not self.win_estandar.isVisible():
            self.win_estandar = VentanaEstandar()
            self.win_estandar.show()
        else:
            self.win_estandar.activateWindow()

    def abrir_cientifico(self):
        if self.win_cientifica is None or not self.win_cientifica.isVisible():
            self.win_cientifica = VentanaCientifica()
            self.win_cientifica.show()
        else:
            self.win_cientifica.activateWindow()

    def aplicar_estilos(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #b5cc7f; }
            QLabel { color: #222222; }
            QPushButton#btn_blanco {
                background-color: #f0f0f0;
                color: #333333;
                border: none;
                border-radius: 12px;
            }
            QPushButton#btn_blanco:hover { background-color: #ffffff; }
            QPushButton#btn_amarillo {
                background-color: #f4b41a;
                color: #ffffff;
                border: none;
                border-radius: 12px;
            }
            QPushButton#btn_amarillo:hover { background-color: #ffc52d; }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = VentanaMenuPrincipal()
    menu.show()
    sys.exit(app.exec())