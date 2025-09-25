"""
Componente de card para visualização de PDFs
"""

import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageQt
import fitz  # PyMuPDF


class PDFCard(QFrame):
    """Card elegante para PDF usando PyQt6"""

    clicked = pyqtSignal(object)  # Signal para quando o card é clicado

    def __init__(self, arquivo_pdf, numero, parent=None):
        super().__init__(parent)
        self.arquivo_pdf = arquivo_pdf
        self.numero = numero
        self.selected = False

        self._setup_ui()
        self._create_card()

    def _setup_ui(self):
        """Configura a interface do card"""
        self.setFixedSize(200, 280)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Estilo inicial
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 8px;
            }
            QFrame:hover {
                border-color: #2196F3;
                background-color: #f8f9ff;
            }
        """)

    def _create_card(self):
        """Cria o layout do card"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Header com número
        header_layout = QHBoxLayout()
        header_layout.addStretch()

        self.numero_label = QLabel(str(self.numero))
        self.numero_label.setFixedSize(30, 30)
        self.numero_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.numero_label.setStyleSheet("""
            QLabel {
                background-color: #2196F3;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        header_layout.addWidget(self.numero_label)
        layout.addLayout(header_layout)

        # Preview area
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(170, 140)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)

        # Gerar preview
        self._generate_preview()

        layout.addWidget(self.preview_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nome do arquivo
        nome_arquivo = os.path.basename(self.arquivo_pdf)
        if len(nome_arquivo) > 28:
            nome_exibido = nome_arquivo[:25] + "..."
        else:
            nome_exibido = nome_arquivo

        self.nome_label = QLabel(nome_exibido)
        self.nome_label.setWordWrap(True)
        self.nome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nome_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: 500;
                color: #333;
                margin-top: 4px;
            }
        """)
        layout.addWidget(self.nome_label)

        # Info adicional (páginas)
        try:
            doc = fitz.open(self.arquivo_pdf)
            num_paginas = len(doc)
            doc.close()

            info_text = f"{num_paginas} página{'s' if num_paginas != 1 else ''}"
        except Exception:
            info_text = "Erro ao ler PDF"

        self.info_label = QLabel(info_text)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #666;
                margin-top: 2px;
            }
        """)
        layout.addWidget(self.info_label)

    def _generate_preview(self):
        """Gera preview da primeira página do PDF"""
        try:
            doc = fitz.open(self.arquivo_pdf)
            page = doc[0]

            # Renderizar em alta resolução
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")

            # Converter para PIL Image
            pil_image = Image.open(fitz.io.BytesIO(img_data))

            # Redimensionar mantendo proporção
            pil_image.thumbnail((160, 130), Image.Resampling.LANCZOS)

            # Converter para Qt
            qt_image = ImageQt.ImageQt(pil_image)
            pixmap = QPixmap.fromImage(qt_image)

            self.preview_label.setPixmap(pixmap)
            doc.close()

        except Exception as e:
            # Mostrar ícone de erro
            self.preview_label.setText("❌\nErro ao\ncarregar\npreview")
            self.preview_label.setStyleSheet("""
                QLabel {
                    background-color: #ffebee;
                    border: 1px solid #ffcdd2;
                    border-radius: 8px;
                    color: #c62828;
                    font-size: 11px;
                    font-weight: bold;
                }
            """)

    def toggle_selection(self):
        """Alterna o estado de seleção do card"""
        self.selected = not self.selected
        self._update_style()

    def set_selected(self, selected):
        """Define o estado de seleção"""
        self.selected = selected
        self._update_style()

    def _update_style(self):
        """Atualiza o estilo baseado no estado de seleção"""
        if self.selected:
            self.setStyleSheet("""
                QFrame {
                    background-color: #e3f2fd;
                    border: 2px solid #2196F3;
                    border-radius: 12px;
                    padding: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 2px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 8px;
                }
                QFrame:hover {
                    border-color: #2196F3;
                    background-color: #f8f9ff;
                }
            """)

    def mousePressEvent(self, event):
        """Manipula clique no card"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
        super().mousePressEvent(event)

    def update_number(self, novo_numero):
        """Atualiza o número do card"""
        self.numero = novo_numero
        self.numero_label.setText(str(novo_numero))