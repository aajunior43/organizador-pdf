# 📄 Organizador de PDFs para Impressão

Um programa profissional e intuitivo para organizar múltiplos arquivos PDF na ordem desejada antes de imprimir.

## ✨ Funcionalidades

- ✅ **Adicionar múltiplos PDFs**: Selecione vários arquivos PDF de uma vez ou arraste para a interface
- ✅ **Drag-and-drop para reordenar**: Arraste os cards dos PDFs para reorganizar a ordem
- ✅ **Preview visual**: Veja a primeira página de cada PDF em cards elegantes
- ✅ **Interface profissional**: Interface nativa com PyQt6, toolbar e painel de estatísticas
- ✅ **Mesclar PDFs**: Gere um único arquivo PDF com todos os documentos na ordem escolhida
- ✅ **Estatísticas em tempo real**: Veja total de PDFs e páginas no painel lateral

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passos para instalação

1. **Clone ou baixe este projeto**
   ```bash
   # Se você tem git instalado
   git clone <url-do-repositorio>
   cd organizador-pdf
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o programa**
   ```bash
   python organizador_pdf.py
   ```

## 📋 Como usar

### Passo a passo

1. **Inicie o programa**
   - Execute `python organizador_pdf.py`
   - A interface profissional será aberta

2. **Adicione seus PDFs**
   - Clique no botão "📁 Adicionar PDFs" na toolbar
   - **OU** arraste arquivos PDF diretamente para a interface
   - Os arquivos aparecerão como cards visuais com preview

3. **Organize a ordem**
   - **Método 1**: Arraste os cards dos PDFs para reordenar (drag-and-drop)
   - **Método 2**: Clique em um card para selecioná-lo e use os botões "⬆️ Subir" e "⬇️ Descer"
   - Veja as estatísticas atualizadas no painel lateral

4. **Gere o PDF final**
   - Clique em "📄 Gerar PDF" na toolbar
   - Escolha onde salvar o arquivo final
   - Pronto! Seu PDF organizado está criado

### 🎯 Funcionalidades Avançadas

- **Atalhos de teclado**: 
  - `Ctrl+O` - Adicionar PDFs
  - `Ctrl+S` - Gerar PDF final
  - `Delete` - Remover PDF selecionado
  - `Ctrl+L` - Limpar lista
  - `F5` - Atualizar previews
  - `Ctrl+↑/↓` - Mover PDFs
  - `Ctrl+Q` - Sair
- **Tooltips informativos**: Passe o mouse sobre os botões para ver dicas
- **Status bar inteligente**: Mensagens temporárias com feedback visual
- **Interface responsiva**: Redimensione janelas e painéis conforme necessário
- **Ícone personalizado**: Ícone PDF customizado na barra de tarefas

## Exemplo de uso

1. Você tem 5 PDFs: `documento1.pdf`, `documento2.pdf`, etc.
2. Adicione todos os PDFs ao programa
3. Reordene conforme necessário (ex: documento3, documento1, documento5, documento2, documento4)
4. Gere o PDF final
5. Imprima o arquivo gerado - as páginas sairão na ordem que você organizou!

## Solução de problemas

### Erro ao instalar dependências
```bash
# Tente atualizar o pip primeiro
python -m pip install --upgrade pip

# Depois instale as dependências
pip install -r requirements.txt
```

### Erro "Módulo não encontrado"
- Certifique-se de que instalou todas as dependências
- Verifique se está usando a versão correta do Python

### PDFs não carregam
- Verifique se os arquivos PDF não estão corrompidos
- Certifique-se de que os arquivos não estão protegidos por senha

### Preview não aparece
- Alguns PDFs podem não gerar preview corretamente
- Isso não afeta a funcionalidade de mesclagem

## Dependências

- **PyPDF2**: Para manipulação e mesclagem de PDFs
- **Pillow**: Para processamento de imagens
- **PyMuPDF**: Para geração de previews dos PDFs
- **tkinter**: Interface gráfica (já incluído no Python)

## Compatibilidade

- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux
- ✅ Python 3.7+

## Dicas de uso

1. **Para impressão em lote**: Organize todos os documentos que precisa imprimir e gere um único PDF
2. **Backup**: Sempre mantenha os PDFs originais como backup
3. **Nomes descritivos**: Use nomes claros nos seus PDFs para facilitar a organização
4. **Teste primeiro**: Faça um teste com poucos PDFs antes de processar muitos arquivos

## Suporte

Se encontrar algum problema:
1. Verifique se seguiu todos os passos de instalação
2. Confirme que tem todas as dependências instaladas
3. Teste com PDFs diferentes para isolar o problema

---

**Desenvolvido para facilitar a organização de documentos PDF antes da impressão!** 📄✨