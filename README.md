# UntungKu (Untung-Ku) 📈

**UntungKu** is an offline-first Progressive Web Application (PWA) tailored for micro-enterprises, hawkers, and small stall vendors in Malaysia. It simplifies daily cash float management, automates receipt digital sales ingestion via OCR, calculates accurate net daily profit, and exports structured tax/audit compliance reports.

---

## 🏗️ Tech Stack

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) + Tailwind CSS | Fast, component-based, responsive UI |
| **PWA** | Workbox + IndexedDB | Offline capability for unstable internet connections |
| **Backend** | Python FastAPI (3.13+) | High performance, async execution, smooth OCR integration |
| **Database** | PostgreSQL (Production) / SQLite (Dev) | ACID compliance for financial integrity; JSONB support |
| **OCR Engine** | PaddleOCR | Multi-language receipt text recognition (English, Malay, Chinese) |
| **Reports** | ReportLab / WeasyPrint | Professional PDF financial layout generation |
| **Deployment** | Vercel (Frontend) + Render (Backend) + Supabase (DB) | Scalable, free-tier friendly cloud hosting |

---

## 📁 Repository Structure

```text
untungku/
├── frontend/             # React (Vite) + Tailwind CSS frontend application
└── backend/              # FastAPI backend application
    ├── app/
    │   ├── api/          # API routers (v1 endpoints)
    │   ├── core/         # App configuration, database engine, security
    │   ├── models/       # SQLAlchemy database ORM models
    │   ├── schemas/      # Pydantic validation models
    │   ├── services/     # Business logic layer
    │   └── ocr/          # OCR processing module (PaddleOCR)
    ├── .dockerignore     # Docker context build exclusion rule
    ├── Dockerfile        # Multi-stage production container setup
    ├── pyproject.toml    # Local editable package discovery declaration
    └── requirements.txt  # Python dependency manifest
```

---

## 🚀 Quick Start (Backend Local Development)

### 1. Setup Virtual Environment
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies & Register Local Package
```powershell
pip install -r requirements.txt
pip install -e .
```

### 3. Launch Development Server
```powershell
uvicorn app.main:app --reload --port 8000
```
- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

## 🐳 Docker Execution

```powershell
cd backend
docker build -t untungku-backend .
docker run -d -p 8000:8000 --name untungku-backend untungku-backend
```