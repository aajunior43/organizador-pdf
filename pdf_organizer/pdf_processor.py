"""
Processador de PDFs - lógica de manipulação de arquivos PDF
"""

import os
from typing import List
from PyPDF2 import PdfReader, PdfWriter
from PyQt6.QtCore import QThread, pyqtSignal


class PDFProcessor(QThread):
    """Worker thread para processamento de PDFs"""

    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, arquivos_pdf: List[str], arquivo_saida: str):
        super().__init__()
        self.arquivos_pdf = arquivos_pdf
        self.arquivo_saida = arquivo_saida

    def run(self):
        """Executa o processamento dos PDFs"""
        try:
            self._merge_pdfs()
        except Exception as e:
            self.error.emit(f"Erro ao processar PDFs: {str(e)}")

    def _merge_pdfs(self):
        """Realiza a mesclagem dos PDFs"""
        writer = PdfWriter()
        total_files = len(self.arquivos_pdf)

        for i, arquivo_pdf in enumerate(self.arquivos_pdf):
            try:
                reader = PdfReader(arquivo_pdf)

                for page in reader.pages:
                    writer.add_page(page)

                # Emitir progresso
                progress_percent = int((i + 1) / total_files * 100)
                self.progress.emit(progress_percent)

            except Exception as e:
                self.error.emit(f"Erro ao processar {os.path.basename(arquivo_pdf)}: {str(e)}")
                return

        # Salvar arquivo final
        try:
            with open(self.arquivo_saida, 'wb') as arquivo_final:
                writer.write(arquivo_final)

            self.finished.emit(self.arquivo_saida)

        except Exception as e:
            self.error.emit(f"Erro ao salvar arquivo final: {str(e)}")


class PDFUtils:
    """Utilitários para trabalhar com PDFs"""

    @staticmethod
    def get_pdf_info(arquivo_pdf: str) -> dict:
        """Obtém informações básicas do PDF"""
        try:
            reader = PdfReader(arquivo_pdf)
            info = reader.metadata or {}

            return {
                'num_pages': len(reader.pages),
                'title': info.get('/Title', 'Sem título'),
                'author': info.get('/Author', 'Autor desconhecido'),
                'subject': info.get('/Subject', ''),
                'creator': info.get('/Creator', ''),
                'producer': info.get('/Producer', ''),
                'creation_date': info.get('/CreationDate', ''),
                'modification_date': info.get('/ModDate', ''),
                'file_size': os.path.getsize(arquivo_pdf)
            }
        except Exception as e:
            return {
                'error': str(e),
                'num_pages': 0,
                'title': 'Erro ao ler arquivo',
                'file_size': 0
            }

    @staticmethod
    def validate_pdf_file(arquivo_pdf: str) -> bool:
        """Valida se o arquivo é um PDF válido"""
        try:
            reader = PdfReader(arquivo_pdf)
            # Tenta ler pelo menos uma página
            _ = len(reader.pages)
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_size_formatted(arquivo_pdf: str) -> str:
        """Retorna o tamanho do arquivo formatado"""
        try:
            size_bytes = os.path.getsize(arquivo_pdf)

            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except Exception:
            return "Tamanho desconhecido"