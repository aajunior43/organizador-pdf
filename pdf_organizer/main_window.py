"""
Janela principal da aplicação PDF Organizer
"""

import os
import sys
from typing import List
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QLabel, QPushButton, QFileDialog,
    QMessageBox, QToolBar, QStatusBar, QProgressBar,
    QFrame, QSplitter, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont, QIcon, QPalette, QColor

from .pdf_card import PDFCard
from .pdf_processor import PDFProcessor, PDFUtils


class PDFOrganizerWindow(QMainWindow):
    """Janela principal do organizador de PDFs"""

    def __init__(self):
        super().__init__()
        self.arquivos_pdf = []
        self.cards_pdf = []
        self.pdf_processor = None

        self._setup_ui()
        self._setup_connections()
        self._apply_theme()

    def _setup_ui(self):
        """Configura a interface principal"""
        self.setWindowTitle("📄 PDF Organizer v3.0 - Plataforma Moderna")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Criar sidebar
        self._create_sidebar(main_layout)

        # Criar área principal
        self._create_main_area(main_layout)

        # Criar toolbar
        self._create_toolbar()

        # Criar status bar
        self._create_status_bar()

    def _create_sidebar(self, parent_layout):
        """Cria a barra lateral com controles"""
        sidebar = QFrame()
        sidebar.setFrameStyle(QFrame.Shape.Box)
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(15)

        # Título da sidebar
        title_label = QLabel("🔧 Controles")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #495057; margin-bottom: 10px;")
        sidebar_layout.addWidget(title_label)

        # Grupo de arquivos
        files_group = QGroupBox("📁 Gerenciar Arquivos")
        files_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        files_layout = QVBoxLayout(files_group)

        self.btn_adicionar = QPushButton("➕ Adicionar PDFs")
        self.btn_adicionar.setMinimumHeight(40)
        self.btn_limpar = QPushButton("🗑️ Limpar Todos")
        self.btn_limpar.setMinimumHeight(40)

        files_layout.addWidget(self.btn_adicionar)
        files_layout.addWidget(self.btn_limpar)
        sidebar_layout.addWidget(files_group)

        # Grupo de organização
        org_group = QGroupBox("📋 Organizar")
        org_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        org_layout = QVBoxLayout(org_group)

        self.btn_mover_cima = QPushButton("⬆️ Mover para Cima")
        self.btn_mover_baixo = QPushButton("⬇️ Mover para Baixo")
        self.btn_remover = QPushButton("❌ Remover Selecionado")

        for btn in [self.btn_mover_cima, self.btn_mover_baixo, self.btn_remover]:
            btn.setMinimumHeight(35)
            btn.setEnabled(False)

        org_layout.addWidget(self.btn_mover_cima)
        org_layout.addWidget(self.btn_mover_baixo)
        org_layout.addWidget(self.btn_remover)
        sidebar_layout.addWidget(org_group)

        # Grupo de processamento
        process_group = QGroupBox("⚙️ Processar")
        process_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        process_layout = QVBoxLayout(process_group)

        self.btn_mesclar = QPushButton("🔗 Mesclar PDFs")
        self.btn_mesclar.setMinimumHeight(45)
        self.btn_mesclar.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.btn_mesclar.setEnabled(False)

        process_layout.addWidget(self.btn_mesclar)
        sidebar_layout.addWidget(process_group)

        # Informações
        info_group = QGroupBox("ℹ️ Informações")
        info_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        info_layout = QVBoxLayout(info_group)

        self.info_arquivos = QLabel("Arquivos: 0")
        self.info_paginas = QLabel("Total de páginas: 0")
        self.info_tamanho = QLabel("Tamanho total: 0 MB")

        for info_label in [self.info_arquivos, self.info_paginas, self.info_tamanho]:
            info_label.setStyleSheet("color: #6c757d; font-size: 12px;")

        info_layout.addWidget(self.info_arquivos)
        info_layout.addWidget(self.info_paginas)
        info_layout.addWidget(self.info_tamanho)
        sidebar_layout.addWidget(info_group)

        sidebar_layout.addStretch()
        parent_layout.addWidget(sidebar)

    def _create_main_area(self, parent_layout):
        """Cria a área principal de visualização"""
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.Shape.Box)
        main_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)

        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título da área principal
        title_label = QLabel("📄 Seus Arquivos PDF")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #343a40; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Área de drag and drop / lista de arquivos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(600)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px dashed #6c757d;
                border-radius: 12px;
                background-color: #f8f9fa;
            }
        """)

        # Widget que contém os cards
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Label de instrução inicial
        self.instruction_label = QLabel(
            "🎯 Arraste arquivos PDF aqui ou clique em 'Adicionar PDFs'\n\n"
            "✨ Funcionalidades:\n"
            "• Visualização de preview das páginas\n"
            "• Organização por drag-and-drop\n"
            "• Mesclagem em ordem personalizada\n"
            "• Interface moderna e intuitiva"
        )
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 16px;
                line-height: 1.5;
                padding: 40px;
            }
        """)

        self.scroll_layout.addWidget(self.instruction_label, 0, 0)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Progress bar (inicialmente oculta)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #28a745;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        parent_layout.addWidget(main_frame)

    def _create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar("Ferramentas")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #343a40;
                border: none;
                spacing: 8px;
                padding: 8px;
            }
            QToolButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #495057;
            }
        """)

        # Ações da toolbar
        action_about = QAction("ℹ️ Sobre", self)
        action_help = QAction("❓ Ajuda", self)
        action_settings = QAction("⚙️ Configurações", self)

        toolbar.addAction(action_about)
        toolbar.addSeparator()
        toolbar.addAction(action_help)
        toolbar.addSeparator()
        toolbar.addAction(action_settings)

        self.addToolBar(toolbar)

    def _create_status_bar(self):
        """Cria a barra de status"""
        status_bar = QStatusBar()
        status_bar.showMessage("Pronto para organizar PDFs | PDF Organizer v3.0")
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
                font-size: 12px;
            }
        """)
        self.setStatusBar(status_bar)

    def _setup_connections(self):
        """Configura as conexões de sinais"""
        self.btn_adicionar.clicked.connect(self.adicionar_pdfs)
        self.btn_limpar.clicked.connect(self.limpar_arquivos)
        self.btn_mover_cima.clicked.connect(self.mover_selecionado_cima)
        self.btn_mover_baixo.clicked.connect(self.mover_selecionado_baixo)
        self.btn_remover.clicked.connect(self.remover_selecionado)
        self.btn_mesclar.clicked.connect(self.mesclar_pdfs)

    def _apply_theme(self):
        """Aplica tema moderno à aplicação"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
            }
        """)

    # Métodos de funcionalidade (implementação básica)
    def adicionar_pdfs(self):
        """Adiciona arquivos PDF à lista"""
        arquivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Arquivos PDF",
            "",
            "Arquivos PDF (*.pdf);;Todos os arquivos (*)"
        )

        if arquivos:
            self._processar_novos_arquivos(arquivos)

    def _processar_novos_arquivos(self, novos_arquivos: List[str]):
        """Processa novos arquivos adicionados"""
        for arquivo in novos_arquivos:
            if arquivo not in self.arquivos_pdf:
                if PDFUtils.validate_pdf_file(arquivo):
                    self.arquivos_pdf.append(arquivo)
                else:
                    QMessageBox.warning(
                        self, "Arquivo Inválido",
                        f"O arquivo {os.path.basename(arquivo)} não é um PDF válido."
                    )

        self._atualizar_interface()

    def _atualizar_interface(self):
        """Atualiza a interface com os arquivos carregados"""
        # Limpar cards existentes
        self._limpar_cards()

        if not self.arquivos_pdf:
            self.instruction_label.setVisible(True)
            self.btn_mesclar.setEnabled(False)
            return

        self.instruction_label.setVisible(False)

        # Criar novos cards
        for i, arquivo in enumerate(self.arquivos_pdf):
            card = PDFCard(arquivo, i + 1)
            card.clicked.connect(self._on_card_clicked)
            self.cards_pdf.append(card)

            row = i // 4
            col = i % 4
            self.scroll_layout.addWidget(card, row, col)

        # Atualizar informações
        self._atualizar_informacoes()
        self.btn_mesclar.setEnabled(len(self.arquivos_pdf) > 1)

    def _limpar_cards(self):
        """Remove todos os cards da interface"""
        for card in self.cards_pdf:
            card.deleteLater()
        self.cards_pdf.clear()

    def _on_card_clicked(self, card):
        """Manipula clique em um card"""
        # Desselecionar outros cards
        for c in self.cards_pdf:
            if c != card:
                c.set_selected(False)

        # Alternar seleção do card clicado
        card.toggle_selection()

        # Atualizar botões de organização
        has_selection = any(c.selected for c in self.cards_pdf)
        self.btn_mover_cima.setEnabled(has_selection)
        self.btn_mover_baixo.setEnabled(has_selection)
        self.btn_remover.setEnabled(has_selection)

    def _atualizar_informacoes(self):
        """Atualiza as informações na sidebar"""
        total_arquivos = len(self.arquivos_pdf)
        total_paginas = 0
        total_tamanho = 0

        for arquivo in self.arquivos_pdf:
            info = PDFUtils.get_pdf_info(arquivo)
            total_paginas += info.get('num_pages', 0)
            total_tamanho += info.get('file_size', 0)

        tamanho_mb = total_tamanho / (1024 * 1024)

        self.info_arquivos.setText(f"Arquivos: {total_arquivos}")
        self.info_paginas.setText(f"Total de páginas: {total_paginas}")
        self.info_tamanho.setText(f"Tamanho total: {tamanho_mb:.1f} MB")

    def limpar_arquivos(self):
        """Remove todos os arquivos"""
        if self.arquivos_pdf:
            reply = QMessageBox.question(
                self, "Confirmar",
                "Deseja remover todos os arquivos da lista?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.arquivos_pdf.clear()
                self._atualizar_interface()

    def mover_selecionado_cima(self):
        """Move o arquivo selecionado para cima"""
        selected_card = next((c for c in self.cards_pdf if c.selected), None)
        if not selected_card:
            return

        index = self.cards_pdf.index(selected_card)
        if index > 0:
            self.arquivos_pdf[index], self.arquivos_pdf[index - 1] = \
                self.arquivos_pdf[index - 1], self.arquivos_pdf[index]
            self._atualizar_interface()

    def mover_selecionado_baixo(self):
        """Move o arquivo selecionado para baixo"""
        selected_card = next((c for c in self.cards_pdf if c.selected), None)
        if not selected_card:
            return

        index = self.cards_pdf.index(selected_card)
        if index < len(self.cards_pdf) - 1:
            self.arquivos_pdf[index], self.arquivos_pdf[index + 1] = \
                self.arquivos_pdf[index + 1], self.arquivos_pdf[index]
            self._atualizar_interface()

    def remover_selecionado(self):
        """Remove o arquivo selecionado"""
        selected_card = next((c for c in self.cards_pdf if c.selected), None)
        if not selected_card:
            return

        index = self.cards_pdf.index(selected_card)
        arquivo_nome = os.path.basename(self.arquivos_pdf[index])

        reply = QMessageBox.question(
            self, "Confirmar Remoção",
            f"Deseja remover '{arquivo_nome}' da lista?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            del self.arquivos_pdf[index]
            self._atualizar_interface()

    def mesclar_pdfs(self):
        """Inicia o processo de mesclagem dos PDFs"""
        if len(self.arquivos_pdf) < 2:
            QMessageBox.information(
                self, "Informação",
                "É necessário pelo menos 2 arquivos PDF para mesclar."
            )
            return

        # Solicitar nome do arquivo de saída
        arquivo_saida, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF Mesclado",
            "PDF_Mesclado.pdf",
            "Arquivos PDF (*.pdf)"
        )

        if arquivo_saida:
            self._iniciar_processamento(arquivo_saida)

    def _iniciar_processamento(self, arquivo_saida: str):
        """Inicia o processamento dos PDFs"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_mesclar.setEnabled(False)

        # Criar e iniciar worker thread
        self.pdf_processor = PDFProcessor(self.arquivos_pdf, arquivo_saida)
        self.pdf_processor.progress.connect(self.progress_bar.setValue)
        self.pdf_processor.finished.connect(self._on_processing_finished)
        self.pdf_processor.error.connect(self._on_processing_error)
        self.pdf_processor.start()

        self.statusBar().showMessage("Processando PDFs...")

    def _on_processing_finished(self, arquivo_saida: str):
        """Chamado quando o processamento termina com sucesso"""
        self.progress_bar.setVisible(False)
        self.btn_mesclar.setEnabled(True)
        self.statusBar().showMessage("Pronto para organizar PDFs | PDF Organizer v3.0")

        QMessageBox.information(
            self, "Sucesso!",
            f"PDFs mesclados com sucesso!\n\nArquivo salvo em:\n{arquivo_saida}"
        )

    def _on_processing_error(self, erro: str):
        """Chamado quando ocorre erro no processamento"""
        self.progress_bar.setVisible(False)
        self.btn_mesclar.setEnabled(True)
        self.statusBar().showMessage("Erro no processamento")

        QMessageBox.critical(self, "Erro", erro)

    def closeEvent(self, event):
        """Manipula o fechamento da aplicação"""
        if self.pdf_processor and self.pdf_processor.isRunning():
            reply = QMessageBox.question(
                self, "Processamento em Andamento",
                "Há um processamento em andamento. Deseja realmente sair?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
            else:
                self.pdf_processor.terminate()
                self.pdf_processor.wait()

        event.accept()