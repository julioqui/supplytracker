# 🧾 SupplyTracker

An inventory management system web application.  
Built with **FastAPI** on the backend and **Next.js** on the frontend.

---

## 🚀 Technologies

### Backend
- **FastAPI** — Modern, high-performance web framework for Python  
- **SQLAlchemy** — ORM for database management  
- **Pydantic** — Data validation and serialization  
- **PostgreSQL** — Relational database  
- **Docker** — Containerized development environment  
- **Uvicorn** — ASGI server for FastAPI  
- **python-dotenv** — Environment variable management  

### Frontend
- **Next.js 15** — React framework with App Router  
- **React 19 + React Compiler**  
- **TypeScript** — Type-safe development  
- **Tailwind CSS** — Utility-first styling  

---

## 🧩 Project Structure

```
supplytracker/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  ├─ auth/
│  │  ├─ products/
│  ├─ requirements.txt
│  ├─ docker-compose.yml
│  ├─ Dockerfile
│  └─ .env
│
└─ frontend/
   ├─ app/
   ├─ components/
   ├─ package.json
   ├─ next.config.js
   └─ .env.local
```

---

## ⚙️ Backend Setup (FastAPI)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/supplytracker.git
cd supplytracker/backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file
Inside the `backend/` directory, create a `.env` file based on the example below:

```env
# ========================
# DATABASE CONFIG
# ========================
DATABASE_URL=postgresql://user:password@localhost:5432/supplytracker

# For remote tests or production with Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your_supabase_api_key

# ========================
# JWT CONFIG
# ========================
JWT_SECRET=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ========================
# APP CONFIG
# ========================
APP_ENV=development
```

### 5. Start PostgreSQL using Docker
```bash
docker-compose up -d db
```

### 6. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```

Access:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## ⚙️ Frontend Setup (Next.js)

### 1. Navigate to the frontend directory
```bash
cd ../frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Create a `.env.local` file
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Start the development server
```bash
npm run dev
```

Access:
👉 [http://localhost:3000](http://localhost:3000)

---

## 🧠 Useful Commands

**Run only the database:**
```bash
docker-compose up -d db
```

**Run backend and database together:**
```bash
docker-compose up --build
```

**Stop all containers:**
```bash
docker-compose down
```

**View backend logs:**
```bash
docker logs backend -f
```

---

## 📘 Environment Overview

| Component | Tech | Description |
|------------|------|-------------|
| Frontend | Next.js 15 + React 19 | UI and client-side logic |
| Backend | FastAPI | REST API and business logic |
| Database | PostgreSQL | Persistent storage |
| Auth | Supabase Auth | Google Sign-In and user management |
| Infrastructure | Docker | Containerized local setup |

---

