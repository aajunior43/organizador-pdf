import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton, QScrollArea, QFrame, QFileDialog,
    QMessageBox, QToolBar, QStatusBar, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, QMimeData, QThread, pyqtSignal, QSize, QPoint
from PyQt6.QtGui import QPixmap, QIcon, QFont, QAction, QPalette, QColor, QDragEnterEvent, QDropEvent, QDrag, QPainter
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageQt
import fitz  # PyMuPDF

class PDFCardQt(QFrame):
    """Card elegante para PDF usando PyQt6"""
    
    clicked = pyqtSignal(object)  # Signal para quando o card é clicado
    
    def __init__(self, arquivo_pdf, numero, parent=None):
        super().__init__(parent)
        self.arquivo_pdf = arquivo_pdf
        self.numero = numero
        self.selected = False
        
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
        
        self.criar_card()
    
    def criar_card(self):
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
        self.gerar_preview()
        
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
                color: #333;
                background-color: #f8f9fa;
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #e9ecef;
            }
        """)
        layout.addWidget(self.nome_label)
        
        # Ícone de tipo
        icon_label = QLabel("📄")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_label)
        
        layout.addStretch()
    
    def gerar_preview(self):
        """Gera preview da primeira página"""
        try:
            doc = fitz.open(self.arquivo_pdf)
            page = doc[0]
            
            # Renderizar página
            mat = fitz.Matrix(0.5, 0.5)  # Escala
            pix = page.get_pixmap(matrix=mat)
            
            # Converter para QPixmap
            img_data = pix.tobytes("ppm")
            qimg = ImageQt.ImageQt(Image.open(io.BytesIO(img_data)))
            pixmap = QPixmap.fromImage(qimg)
            
            # Redimensionar para caber no preview
            scaled_pixmap = pixmap.scaled(
                160, 130, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.preview_label.setPixmap(scaled_pixmap)
            doc.close()
            
        except Exception as e:
            # Se falhar, mostrar ícone padrão
            self.preview_label.setText("📄\nPDF")
            self.preview_label.setStyleSheet("""
                QLabel {
                    background-color: #f5f5f5;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 24px;
                    color: #666;
                }
            """)
    
    def selecionar(self):
        """Marca como selecionado"""
        self.selected = True
        self.setStyleSheet("""
            QFrame {
                background-color: #e3f2fd;
                border: 3px solid #2196F3;
                border-radius: 12px;
                padding: 8px;
            }
        """)
    
    def desselecionar(self):
        """Desmarca seleção"""
        self.selected = False
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
    
    def atualizar_numero(self, novo_numero):
        """Atualiza o número do card"""
        self.numero = novo_numero
        self.numero_label.setText(str(novo_numero))
    
    def mousePressEvent(self, event):
        """Handle mouse click and start drag"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operation"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        
        if not hasattr(self, 'drag_start_position'):
            return
            
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        # Iniciar operação de drag
        drag = QDrag(self)
        mimeData = QMimeData()
        
        # Armazenar ID do card no mime data
        mimeData.setText(f"pdf_card:{self.numero}")
        drag.setMimeData(mimeData)
        
        # Criar pixmap do card para mostrar durante o drag
        pixmap = self.grab()
        
        # Criar painter para adicionar transparência
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(0.7)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        
        drag.setPixmap(transparent_pixmap)
        drag.setHotSpot(self.drag_start_position)
        
        # Executar drag
        dropAction = drag.exec(Qt.DropAction.MoveAction)
        
        super().mouseMoveEvent(event)

class OrganizadorPDFQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdfs_lista = []
        self.cards = []
        self.card_selecionado = None
        
        self.setWindowTitle("📄 Organizador de PDFs - Versão Profissional")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Configurar estilo da aplicação
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QToolBar {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #e9ecef;
                spacing: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #e9ecef;
                padding: 5px;
            }
        """)
        
        self.criar_interface()
        self.configurar_drag_drop()
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Criar toolbar
        self.criar_toolbar()
        
        # Área principal com splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Área de cards (lado esquerdo)
        self.criar_area_cards(splitter)
        
        # Painel lateral (lado direito)
        self.criar_painel_lateral(splitter)
        
        # Configurar proporções do splitter
        splitter.setSizes([1000, 300])
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✅ Pronto para usar - Arraste PDFs ou use o botão Adicionar")
    
    def criar_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        
        # Botão Adicionar
        action_adicionar = QAction("📁 Adicionar PDFs", self)
        action_adicionar.triggered.connect(self.adicionar_pdfs)
        toolbar.addAction(action_adicionar)
        
        toolbar.addSeparator()
        
        # Botão Remover
        action_remover = QAction("🗑️ Remover", self)
        action_remover.triggered.connect(self.remover_pdf)
        toolbar.addAction(action_remover)
        
        # Botão Limpar
        action_limpar = QAction("🧹 Limpar", self)
        action_limpar.triggered.connect(self.limpar_lista)
        toolbar.addAction(action_limpar)
        
        toolbar.addSeparator()
        
        # Botões de movimento
        action_subir = QAction("⬆️ Subir", self)
        action_subir.triggered.connect(self.mover_para_cima)
        toolbar.addAction(action_subir)
        
        action_descer = QAction("⬇️ Descer", self)
        action_descer.triggered.connect(self.mover_para_baixo)
        toolbar.addAction(action_descer)
        
        toolbar.addSeparator()
        
        # Botão Gerar PDF
        action_gerar = QAction("📄 Gerar PDF", self)
        action_gerar.triggered.connect(self.gerar_pdf_final)
        toolbar.addAction(action_gerar)
    
    def criar_area_cards(self, parent):
        """Cria a área scrollável para os cards"""
        # Frame container
        cards_frame = QFrame()
        cards_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(cards_frame)
        
        # Título
        title_label = QLabel("📋 PDFs Selecionados")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #495057; padding: 15px;")
        layout.addWidget(title_label)
        
        # Área de scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget para conter os cards
        self.cards_widget = QWidget()
        self.cards_widget.setAcceptDrops(True)
        self.cards_layout = QGridLayout(self.cards_widget)
        self.cards_layout.setSpacing(15)
        self.cards_layout.setContentsMargins(20, 20, 20, 20)
        
        # Conectar eventos de drag and drop
        self.cards_widget.dragEnterEvent = self.card_drag_enter_event
        self.cards_widget.dragMoveEvent = self.card_drag_move_event
        self.cards_widget.dropEvent = self.card_drop_event
        
        self.scroll_area.setWidget(self.cards_widget)
        layout.addWidget(self.scroll_area)
        
        # Mostrar instruções iniciais
        self.mostrar_instrucoes()
        
        parent.addWidget(cards_frame)
    
    def criar_painel_lateral(self, parent):
        """Cria painel lateral com informações"""
        painel = QFrame()
        painel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(painel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título do painel
        title = QLabel("📊 Informações")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #495057; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Estatísticas
        self.stats_group = QGroupBox("Estatísticas")
        stats_layout = QVBoxLayout(self.stats_group)
        
        self.total_pdfs_label = QLabel("📄 Total de PDFs: 0")
        self.total_paginas_label = QLabel("📑 Total de páginas: 0")
        self.arquivo_selecionado_label = QLabel("📌 Selecionado: Nenhum")
        
        for label in [self.total_pdfs_label, self.total_paginas_label, self.arquivo_selecionado_label]:
            label.setStyleSheet("padding: 5px; font-size: 12px;")
            stats_layout.addWidget(label)
        
        layout.addWidget(self.stats_group)
        
        # Instruções
        instrucoes_group = QGroupBox("Como usar")
        instrucoes_layout = QVBoxLayout(instrucoes_group)
        
        instrucoes_text = (
            "1. 📁 Adicione PDFs usando o botão ou arrastando\n\n"
            "2. 🖱️ Clique nos cards para selecioná-los\n\n"
            "3. ⬆️⬇️ Use os botões para reordenar\n\n"
            "4. 📄 Gere o PDF final organizado"
        )
        
        instrucoes_label = QLabel(instrucoes_text)
        instrucoes_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #6c757d;
                line-height: 1.4;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
            }
        """)
        instrucoes_layout.addWidget(instrucoes_label)
        
        layout.addWidget(instrucoes_group)
        layout.addStretch()
        
        parent.addWidget(painel)
    
    def mostrar_instrucoes(self):
        """Mostra instruções quando não há PDFs"""
        if len(self.pdfs_lista) == 0:
            # Limpar layout
            for i in reversed(range(self.cards_layout.count())):
                self.cards_layout.itemAt(i).widget().setParent(None)
            
            # Criar widget de instruções
            instrucoes_widget = QFrame()
            instrucoes_widget.setFixedSize(600, 300)
            instrucoes_widget.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    border-radius: 12px;
                }
            """)
            
            layout = QVBoxLayout(instrucoes_widget)
            
            icon_label = QLabel("📁")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("font-size: 48px; margin-bottom: 20px;")
            layout.addWidget(icon_label)
            
            text_label = QLabel(
                "Arraste arquivos PDF aqui\n"
                "ou use o botão 'Adicionar PDFs'\n\n"
                "Os PDFs aparecerão como cards visuais\n"
                "com preview da primeira página"
            )
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #6c757d;
                    line-height: 1.5;
                }
            """)
            layout.addWidget(text_label)
            
            self.cards_layout.addWidget(instrucoes_widget, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
    
    def reorganizar_cards(self):
        """Reorganiza os cards na grade"""
        cols = 4
        for i, card in enumerate(self.cards):
            row = i // cols
            col = i % cols
            self.cards_layout.addWidget(card, row, col)
            card.atualizar_numero(i + 1)
        
        self.atualizar_estatisticas()
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas no painel lateral"""
        total_pdfs = len(self.pdfs_lista)
        self.total_pdfs_label.setText(f"📄 Total de PDFs: {total_pdfs}")
        
        # Calcular total de páginas
        total_paginas = 0
        for arquivo in self.pdfs_lista:
            try:
                reader = PdfReader(arquivo)
                total_paginas += len(reader.pages)
            except:
                pass
        
        self.total_paginas_label.setText(f"📑 Total de páginas: {total_paginas}")
    
    def selecionar_card(self, card):
        """Seleciona um card"""
        # Desselecionar anterior
        if self.card_selecionado:
            self.card_selecionado.desselecionar()
        
        # Selecionar novo
        self.card_selecionado = card
        card.selecionar()
        
        # Atualizar painel
        nome_arquivo = os.path.basename(card.arquivo_pdf)
        self.arquivo_selecionado_label.setText(f"📌 Selecionado: {nome_arquivo[:20]}...")
        self.status_bar.showMessage(f"📌 Selecionado: {nome_arquivo}")
    
    def adicionar_pdfs(self):
        """Adiciona PDFs via dialog"""
        arquivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecione os arquivos PDF",
            "",
            "Arquivos PDF (*.pdf)"
        )
        
        if arquivos:
            self.processar_novos_arquivos(arquivos)
    
    def processar_novos_arquivos(self, arquivos):
        """Processa novos arquivos PDF"""
        # Remover instruções se existirem
        if len(self.pdfs_lista) == 0:
            for i in reversed(range(self.cards_layout.count())):
                item = self.cards_layout.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
        
        novos_arquivos = 0
        for arquivo in arquivos:
            if arquivo not in self.pdfs_lista:
                self.pdfs_lista.append(arquivo)
                
                # Criar card
                card = PDFCardQt(arquivo, len(self.cards) + 1)
                card.clicked.connect(self.selecionar_card)
                self.cards.append(card)
                novos_arquivos += 1
        
        self.reorganizar_cards()
        self.status_bar.showMessage(f"✅ {novos_arquivos} PDF(s) adicionado(s)")
    
    def remover_pdf(self):
        """Remove PDF selecionado"""
        if self.card_selecionado:
            indice = self.cards.index(self.card_selecionado)
            
            # Remover da lista
            self.pdfs_lista.pop(indice)
            
            # Remover card
            self.card_selecionado.setParent(None)
            self.cards.remove(self.card_selecionado)
            self.card_selecionado = None
            
            # Reorganizar
            self.reorganizar_cards()
            
            if len(self.cards) == 0:
                self.mostrar_instrucoes()
                self.arquivo_selecionado_label.setText("📌 Selecionado: Nenhum")
            
            self.status_bar.showMessage("🗑️ PDF removido")
        else:
            self.status_bar.showMessage("⚠️ Selecione um PDF para remover")
    
    def limpar_lista(self):
        """Limpa toda a lista"""
        self.pdfs_lista.clear()
        
        for card in self.cards:
            card.setParent(None)
        self.cards.clear()
        self.card_selecionado = None
        
        self.mostrar_instrucoes()
        self.arquivo_selecionado_label.setText("📌 Selecionado: Nenhum")
        self.atualizar_estatisticas()
        self.status_bar.showMessage("🧹 Lista limpa")
    
    def mover_para_cima(self):
        """Move card para cima"""
        if self.card_selecionado:
            indice = self.cards.index(self.card_selecionado)
            if indice > 0:
                # Trocar posições
                self.pdfs_lista[indice], self.pdfs_lista[indice-1] = \
                    self.pdfs_lista[indice-1], self.pdfs_lista[indice]
                self.cards[indice], self.cards[indice-1] = \
                    self.cards[indice-1], self.cards[indice]
                
                self.reorganizar_cards()
                self.status_bar.showMessage("⬆️ PDF movido para cima")
            else:
                self.status_bar.showMessage("⚠️ PDF já está no início")
        else:
            self.status_bar.showMessage("⚠️ Selecione um PDF para mover")
    
    def mover_para_baixo(self):
        """Move card para baixo"""
        if self.card_selecionado:
            indice = self.cards.index(self.card_selecionado)
            if indice < len(self.cards) - 1:
                # Trocar posições
                self.pdfs_lista[indice], self.pdfs_lista[indice+1] = \
                    self.pdfs_lista[indice+1], self.pdfs_lista[indice]
                self.cards[indice], self.cards[indice+1] = \
                    self.cards[indice+1], self.cards[indice]
                
                self.reorganizar_cards()
                self.status_bar.showMessage("⬇️ PDF movido para baixo")
            else:
                self.status_bar.showMessage("⚠️ PDF já está no final")
        else:
            self.status_bar.showMessage("⚠️ Selecione um PDF para mover")
    
    def configurar_drag_drop(self):
        """Configura drag and drop"""
        self.setAcceptDrops(True)
    
    def card_drag_enter_event(self, event):
        """Handle drag enter para cards"""
        if event.mimeData().hasText() and event.mimeData().text().startswith("pdf_card:"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def card_drag_move_event(self, event):
        """Handle drag move para cards"""
        if event.mimeData().hasText() and event.mimeData().text().startswith("pdf_card:"):
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def card_drop_event(self, event):
        """Handle drop para reordenar cards"""
        if not (event.mimeData().hasText() and event.mimeData().text().startswith("pdf_card:")):
            event.ignore()
            return
        
        # Extrair número do card sendo arrastado
        drag_text = event.mimeData().text()
        drag_card_numero = int(drag_text.split(":")[1])
        
        # Encontrar posição do drop
        drop_pos = event.pos()
        target_card = None
        target_index = -1
        
        # Encontrar o card mais próximo da posição do drop
        min_distance = float('inf')
        for i, card in enumerate(self.cards):
            card_center = card.geometry().center()
            distance = ((card_center.x() - drop_pos.x()) ** 2 + 
                       (card_center.y() - drop_pos.y()) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                target_card = card
                target_index = i
        
        if target_card and target_index != -1:
            # Encontrar índice do card sendo arrastado
            drag_index = -1
            for i, card in enumerate(self.cards):
                if card.numero == drag_card_numero:
                    drag_index = i
                    break
            
            if drag_index != -1 and drag_index != target_index:
                # Reordenar listas
                pdf_item = self.pdfs_lista.pop(drag_index)
                card_item = self.cards.pop(drag_index)
                
                # Ajustar target_index se necessário
                if drag_index < target_index:
                    target_index -= 1
                
                # Inserir na nova posição
                self.pdfs_lista.insert(target_index, pdf_item)
                self.cards.insert(target_index, card_item)
                
                # Reorganizar visualmente
                self.reorganizar_cards()
                
                self.status_bar.showMessage(f"📋 PDF reordenado: posição {drag_index + 1} → {target_index + 1}")
        
        event.acceptProposedAction()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop"""
        urls = event.mimeData().urls()
        arquivos = []
        
        for url in urls:
            arquivo = url.toLocalFile()
            if arquivo.lower().endswith('.pdf') and os.path.isfile(arquivo):
                arquivos.append(arquivo)
        
        if arquivos:
            self.processar_novos_arquivos(arquivos)
            self.status_bar.showMessage(f"🎯 {len(arquivos)} PDF(s) adicionado(s) via drag-and-drop")
        else:
            self.status_bar.showMessage("❌ Apenas arquivos PDF são aceitos")
    
    def gerar_pdf_final(self):
        """Gera PDF final"""
        if not self.pdfs_lista:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um PDF à lista!")
            return
        
        arquivo_saida, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF Organizado",
            "PDF_Organizado.pdf",
            "Arquivos PDF (*.pdf)"
        )
        
        if not arquivo_saida:
            return
        
        try:
            self.status_bar.showMessage("⏳ Gerando PDF...")
            QApplication.processEvents()
            
            pdf_writer = PdfWriter()
            
            for arquivo_pdf in self.pdfs_lista:
                pdf_reader = PdfReader(arquivo_pdf)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            
            with open(arquivo_saida, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            self.status_bar.showMessage(f"✅ PDF salvo: {os.path.basename(arquivo_saida)}")
            QMessageBox.information(
                self,
                "Sucesso",
                f"PDF organizado criado com sucesso!\n\n"
                f"📁 Arquivo: {arquivo_saida}\n"
                f"📄 Total de PDFs mesclados: {len(self.pdfs_lista)}"
            )
            
        except Exception as e:
            self.status_bar.showMessage("❌ Erro ao gerar PDF")
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Organizador de PDFs")
    app.setApplicationVersion("2.0")
    
    # Configurar ícone da aplicação (opcional)
    # app.setWindowIcon(QIcon("icon.png"))
    
    window = OrganizadorPDFQt()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    import io  # Adicionar import que estava faltando
    main()