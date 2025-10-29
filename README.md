# 🧾 SupplyTracker

An inventory management system web application.  
Built with **FastAPI** and **Next.js**.

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
├── backend/
│   ├── alembic/                 # Database migrations
│   ├── app/
│   │   ├── core/               # Core configurations and settings
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Application settings
│   │   │   └── security.py     # Security utilities
│   │   │
│   │   ├── db/                 # Database setup and models
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base model and session
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   │   ├── __init__.py
│   │   │   │   └── user.py     # User and role models
│   │   │   └── session.py      # Database session management
│   │   │
│   │   ├── tests/              # Test files
│   │   │   └── conftest.py     # Test configurations
│   │   │
│   │   └── main.py             # FastAPI application entry point
│   │
│   ├── .env.example           # Example environment variables
│   ├── .env.test              # Test environment variables
│   ├── .gitignore
│   ├── alembic.ini            # Alembic configuration
│   ├── docker-compose.yml     # Docker Compose for local development
│   ├── Dockerfile             # Dockerfile for production
│   └── requirements.txt       # Python dependencies
│
└── frontend/                  # Frontend application
    ├── app/
    ├── components/
    ├── package.json
    ├── next.config.js
    └── .env.local
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

### 4. Set up environment variables

1. Copy the example environment file and update the values:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your configuration:
   ```env
   # Local development database
   DEV_DB_URL=postgresql://user:password@localhost:5432/mydb

   # Supabase configuration (production)
   SUPABASE_URL=https://xxxx.supabase.co
   SUPABASE_KEY=your_supabase_key
   SUPABASE_DB_URL=postgresql://user:password@host:port/dbname

   # JWT Configuration
   JWT_SECRET=supersecretkey
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   # Application environment (development | production)
   APP_ENV=development
   ```

3. For testing, there's a separate `.env.test` file that will be used when running tests.

### 5. Start the development environment with Supabase

1. **Install Supabase CLI** (if not already installed):
   ```bash
   npm install -g supabase
   ```

2. **Start Supabase services** (PostgreSQL, Auth, Storage, etc.):
   ```bash
   supabase start
   ```
   This will start all Supabase services and provide connection details. Make sure to update your `.env` file with the provided credentials.

3. **Set up environment variables** (if not already done):
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with the Supabase connection details from the previous step.

4. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   ```

5. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

7. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Access the services**:
   - **API**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`
   - **Supabase Dashboard**: `http://localhost:54323` (default credentials: `postgres:postgres`)
   - **Supabase Studio**: `http://localhost:54323/project/default` (for database management)

### 6. Using Makefile (optional)

We provide a `Makefile` with useful commands for development:

```bash
# Run database migrations
make migrate

# Reset test database and run tests
make test

# Create and seed test database
make reset_test_db

# View all available commands
make help
```

### 7. Stopping the environment

When you're done, you can stop Supabase services with:
```bash
supabase stop
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
| Database | Supabase DB + PostgreSQL | Persistent storage |
| Auth | Supabase Auth | Google Sign-In and user management |

---

