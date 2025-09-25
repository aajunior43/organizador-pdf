#!/usr/bin/env python3
"""
PDF Organizer v3.0 - Aplicação Desktop Moderna
Organizador de PDFs com interface PyQt6 elegante e funcionalidades avançadas

Autor: PDF Organizer Team
Versão: 3.0.0
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Adicionar o diretório do projeto ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from pdf_organizer import PDFOrganizerWindow
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que todas as dependências estão instaladas:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def setup_application():
    """Configura a aplicação PyQt6"""
    app = QApplication(sys.argv)

    # Configurações da aplicação
    app.setApplicationName("PDF Organizer")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("PDF Organizer Team")
    app.setOrganizationDomain("pdf-organizer.local")

    # Configurar atributos Qt
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    # Definir ícone da aplicação (se existir)
    icon_path = project_root / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    return app


def check_dependencies():
    """Verifica se todas as dependências necessárias estão instaladas"""
    required_modules = [
        ('PyQt6', 'PyQt6'),
        ('PyPDF2', 'PyPDF2'),
        ('PIL', 'Pillow'),
        ('fitz', 'PyMuPDF')
    ]

    missing_modules = []

    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing_modules.append(package_name)

    if missing_modules:
        error_msg = (
            "Dependências não encontradas:\n\n"
            f"• {', '.join(missing_modules)}\n\n"
            "Para instalar, execute:\n"
            f"pip install {' '.join(missing_modules)}"
        )

        # Tentar mostrar erro na interface gráfica
        try:
            app = QApplication([])
            QMessageBox.critical(None, "Dependências Faltando", error_msg)
        except:
            # Fallback para terminal
            print("❌ ERRO: Dependências faltando")
            print(error_msg)

        return False

    return True


def main():
    """Função principal da aplicação"""
    print("🚀 Iniciando PDF Organizer v3.0...")

    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)

    try:
        # Configurar aplicação
        app = setup_application()

        # Criar e mostrar janela principal
        window = PDFOrganizerWindow()
        window.show()

        print("✅ Aplicação iniciada com sucesso!")
        print("📋 Interface pronta para organizar PDFs")

        # Executar loop da aplicação
        sys.exit(app.exec())

    except Exception as e:
        error_msg = f"Erro crítico ao iniciar a aplicação: {str(e)}"

        # Tentar mostrar erro na interface gráfica
        try:
            QMessageBox.critical(None, "Erro Crítico", error_msg)
        except:
            # Fallback para terminal
            print(f"❌ ERRO CRÍTICO: {error_msg}")

        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()