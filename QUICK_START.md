# 🚀 Quick Start Guide - PDF Organizer v3.0

## ⚡ Execução Rápida (Desenvolvimento)

### 1. Pré-requisitos
```bash
# Verificar versões
python --version  # 3.8+
node --version    # 16+
npm --version     # 8+
```

### 2. Clone e Setup
```bash
git clone https://github.com/aajunior43/organizador-pdf.git
cd organizador-pdf
```

### 3. Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 5. Acessar
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

---

## 🐳 Execução com Docker

### Desenvolvimento
```bash
docker-compose up --build
```

### Produção
```bash
docker-compose --profile production up --build
```

---

## 🎯 Funcionalidades Principais

1. **Registro/Login** → Criar conta ou entrar
2. **Dashboard** → Visão geral dos projetos
3. **Novo Projeto** → Criar projeto PDF
4. **Upload** → Arrastar PDFs para o projeto
5. **Organizar** → Reordenar por drag-and-drop
6. **Mesclar** → Gerar PDF final organizado

---

## 🔧 Comandos Úteis

### Backend
```bash
# Testes
pytest tests/ -v

# Linting
black app/
flake8 app/

# Migrações
alembic upgrade head
```

### Frontend
```bash
# Testes
npm test

# Build produção
npm run build

# Linting
npm run lint
npm run format
```

---

## 📁 Estrutura do Projeto

```
pdf-organizer/
├── backend/           # FastAPI + Python
│   ├── app/
│   │   ├── api/       # Rotas REST
│   │   ├── core/      # Config + Auth
│   │   ├── models/    # DB Models
│   │   ├── services/  # Business Logic
│   │   └── utils/     # Helpers
│   └── requirements.txt
├── frontend/          # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── store/
│   │   └── utils/
│   └── package.json
├── docs/              # Documentação
├── tests/             # Testes
└── docker-compose.yml # Container setup
```

---

## 🚨 Solução de Problemas

### Backend não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar porta
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

### Frontend não carrega
```bash
# Limpar cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Erro de CORS
- Verificar se backend está rodando na porta 8000
- Verificar ALLOWED_HOSTS no backend/.env

### Erro de upload
- Verificar tamanho do arquivo (máx 50MB)
- Verificar se é arquivo PDF válido
- Verificar permissões de escrita

---

## 📞 Suporte

- **Issues**: https://github.com/aajunior43/organizador-pdf/issues
- **Docs**: http://localhost:8000/docs
- **Email**: suporte@pdforganizer.com

---

**🎉 Pronto! Seu PDF Organizer v3.0 está funcionando!**