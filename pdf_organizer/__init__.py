"""
PDF Organizer - Aplicação desktop para organização de PDFs
Versão moderna usando PyQt6 com arquitetura limpa
"""

__version__ = "3.0.0"
__author__ = "PDF Organizer Team"

from .main_window import PDFOrganizerWindow
from .pdf_card import PDFCard
from .pdf_processor import PDFProcessor

__all__ = ['PDFOrganizerWindow', 'PDFCard', 'PDFProcessor']