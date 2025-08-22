# 📄 PDF Organizer v3.0 - Plataforma Moderna para Manipulação de PDFs

> **🚀 PROJETO COMPLETAMENTE RENOVADO!** Transformado de aplicação desktop para uma plataforma web moderna e profissional.

Uma plataforma web completa e moderna para organizar, mesclar, comprimir e manipular arquivos PDF com interface responsiva, funcionalidades avançadas e arquitetura profissional.

## ✨ Funcionalidades Principais

### 🎯 **Funcionalidades Core**
- ✅ **Interface Web Moderna**: Design responsivo com Material-UI e animações fluidas
- ✅ **Upload em Lote**: Drag-and-drop para múltiplos arquivos com progress bar
- ✅ **Preview Inteligente**: Visualização da primeira página de cada PDF
- ✅ **Organização Visual**: Reordenação por drag-and-drop com feedback visual
- ✅ **Mesclagem Avançada**: Combine PDFs com controle total da ordem
- ✅ **Gerenciamento de Projetos**: Organize seus trabalhos em projetos

### 🔧 **Funcionalidades Avançadas**
- ✅ **Compressão Inteligente**: Reduza o tamanho mantendo a qualidade
- ✅ **OCR Integrado**: Extração de texto com reconhecimento óptico
- ✅ **Marca d'Água**: Adicione proteção e identificação aos documentos
- ✅ **Assinatura Digital**: Segurança e autenticidade para seus PDFs
- ✅ **Divisão de PDFs**: Separe documentos grandes em arquivos menores
- ✅ **Histórico de Operações**: Rastreamento completo de todas as ações

### 👥 **Sistema de Usuários**
- ✅ **Autenticação Segura**: Login/registro com JWT e criptografia
- ✅ **Perfis Personalizados**: Gerenciamento de conta e preferências
- ✅ **Dashboard Intuitivo**: Visão geral de projetos e estatísticas
- ✅ **Controle de Acesso**: Projetos públicos e privados

## 🏗️ Arquitetura Moderna

### **Backend (FastAPI)**
```
backend/
├── app/
│   ├── api/           # Rotas da API REST
│   ├── core/          # Configurações e segurança
│   ├── models/        # Modelos de banco de dados
│   ├── services/      # Lógica de negócio
│   └── utils/         # Utilitários e helpers
├── requirements.txt   # Dependências Python
└── README.md
```

### **Frontend (React + TypeScript)**
```
frontend/
├── src/
│   ├── components/    # Componentes reutilizáveis
│   ├── pages/         # Páginas da aplicação
│   ├── hooks/         # Custom hooks
│   ├── services/      # Integração com API
│   ├── store/         # Gerenciamento de estado
│   ├── types/         # Definições TypeScript
│   └── utils/         # Utilitários frontend
├── package.json       # Dependências Node.js
└── README.md
```

## 🚀 Instalação e Execução

### **Pré-requisitos**
- Python 3.8+ (para backend)
- Node.js 16+ (para frontend)
- Git

### **1. Clone o Repositório**
```bash
git clone https://github.com/aajunior43/organizador-pdf.git
cd organizador-pdf
```

### **2. Configurar Backend**
```bash
cd backend
pip install -r requirements.txt

# Configurar variáveis de ambiente (opcional)
cp .env.example .env

# Executar servidor de desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **3. Configurar Frontend**
```bash
cd frontend
npm install

# Executar servidor de desenvolvimento
npm run dev
```

### **4. Acessar a Aplicação**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## 🎨 Interface e Experiência

### **Design System**
- **Material-UI**: Componentes modernos e acessíveis
- **Framer Motion**: Animações fluidas e profissionais
- **Responsive Design**: Funciona perfeitamente em desktop, tablet e mobile
- **Dark/Light Mode**: Temas adaptativos para melhor experiência

### **Funcionalidades UX**
- **Drag & Drop**: Interface intuitiva para upload e organização
- **Progress Feedback**: Indicadores visuais para todas as operações
- **Error Handling**: Mensagens claras e ações de recuperação
- **Keyboard Shortcuts**: Atalhos para usuários avançados
- **Auto-save**: Salvamento automático de projetos

## 🔧 Stack Tecnológico

### **Backend**
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **PyPDF2 + PyMuPDF**: Manipulação de PDFs
- **Pillow**: Processamento de imagens
- **Pytesseract**: OCR (Reconhecimento óptico)
- **ReportLab**: Geração de PDFs

### **Frontend**
- **React 18**: Biblioteca UI moderna
- **TypeScript**: Tipagem estática
- **Material-UI**: Sistema de design
- **React Router**: Roteamento SPA
- **Zustand**: Gerenciamento de estado
- **React Query**: Cache e sincronização de dados
- **Axios**: Cliente HTTP
- **React Hook Form**: Formulários performáticos
- **Framer Motion**: Animações

### **Ferramentas de Desenvolvimento**
- **Vite**: Build tool rápido
- **ESLint + Prettier**: Qualidade de código
- **Alembic**: Migrações de banco
- **Pytest**: Testes automatizados

## 📊 Funcionalidades Detalhadas

### **Gerenciamento de Projetos**
- Criação e organização de projetos
- Upload múltiplo com drag-and-drop
- Reordenação visual de arquivos
- Preview em tempo real
- Configurações personalizadas por projeto

### **Processamento de PDFs**
- **Mesclagem**: Combine múltiplos PDFs
- **Compressão**: Otimização de tamanho
- **Divisão**: Separe páginas ou intervalos
- **OCR**: Extração de texto de imagens
- **Marca d'água**: Proteção e branding
- **Metadados**: Edição de propriedades

### **Segurança e Privacidade**
- Autenticação JWT segura
- Criptografia de senhas
- Upload seguro de arquivos
- Validação rigorosa de dados
- Limpeza automática de arquivos temporários

## 🔐 API Documentation

A API REST completa está documentada com Swagger/OpenAPI:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **Principais Endpoints**
- `POST /api/auth/login` - Autenticação
- `POST /api/auth/register` - Registro de usuário
- `GET /api/projects/` - Listar projetos
- `POST /api/projects/` - Criar projeto
- `POST /api/projects/{id}/upload` - Upload de arquivos
- `POST /api/projects/{id}/merge` - Mesclar PDFs
- `POST /api/pdf/compress` - Comprimir PDF
- `POST /api/pdf/watermark` - Adicionar marca d'água

## 🧪 Testes e Qualidade

### **Backend**
```bash
cd backend
pytest tests/ -v
```

### **Frontend**
```bash
cd frontend
npm test
npm run test:coverage
```

### **Linting e Formatação**
```bash
# Backend
black app/
flake8 app/

# Frontend
npm run lint
npm run format
```

## 🚀 Deploy e Produção

### **Docker (Recomendado)**
```bash
# Build e execução com Docker Compose
docker-compose up --build
```

### **Deploy Manual**
- **Backend**: Gunicorn + Nginx
- **Frontend**: Build estático + CDN
- **Banco**: PostgreSQL para produção
- **Cache**: Redis para sessões

## 📈 Roadmap Futuro

- [ ] **Integração Cloud**: Google Drive, Dropbox, OneDrive
- [ ] **Colaboração**: Compartilhamento e edição colaborativa
- [ ] **Templates**: Modelos pré-definidos para documentos
- [ ] **API Pública**: SDK para integrações externas
- [ ] **Mobile App**: Aplicativo nativo iOS/Android
- [ ] **AI Features**: Classificação automática e sugestões

## 🤝 Contribuição

Contribuições são muito bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade open source pelas excelentes bibliotecas
- Contribuidores que ajudaram a melhorar o projeto
- Usuários que forneceram feedback valioso

---

**🎯 Desenvolvido com paixão para revolucionar o trabalho com PDFs!**

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**