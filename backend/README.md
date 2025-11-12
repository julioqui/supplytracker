# SupplyTracker - Backend

The backend for SupplyTracker, an inventory management system built with FastAPI and PostgreSQL.

## 🚀 Technologies

- **FastAPI** - Modern, high-performance web framework for Python
- **SQLAlchemy** - ORM for database management
- **Alembic** - Database migrations
- **Pydantic** - Data validation and serialization
- **PostgreSQL** - Relational database
- **Docker** - Containerized development environment
- **Uvicorn** - ASGI server for FastAPI
- **Supabase** - Authentication and database services
- **Pytest** - Testing framework

## 📁 Project Structure

```
backend/
├── alembic/                 # Database migrations
├── app/
│   ├── core/               # Core configurations and settings
│   │   ├── __init__.py
│   │   ├── config.py       # Application settings
│   │   └── security.py     # Security utilities
│   │
│   ├── db/                 # Database setup and models
│   │   ├── __init__.py
│   │   ├── base.py         # Base model and session
│   │   ├── models/         # SQLAlchemy models
│   │   └── session.py      # Database session management
│   │
│   └── main.py             # FastAPI application entry point
│
├── tests/                  # Test files
├── .env.example           # Example environment variables
├── .env.test              # Test environment variables
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Docker Compose for local development
└── requirements.txt       # Python dependencies
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Docker (optional, for containerized development)
- Supabase CLI (for local development)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/supplytracker.git
cd supplytracker/backend
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
.\venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your configuration:
   ```env
    # Local development
    SUPABASE_URL=http://localhost:54321
    SUPABASE_KEY=supabase-secret-key
    SUPABASE_JWT_SECRET=super-secret-jwt-token-with-at-least-32-characters-long
    SUPABASE_DB_URL=postgresql://postgres:postgres@127.0.0.1:54322/postgres

    #Test DB
    TEST_DB_URL=postgresql://postgres:password@localhost:54332/supplytracker_test

    # APP
    APP_ENV=development
   ```

### 5. Set up Supabase for local development

1. Install Supabase CLI:
   ```bash
   npm install -g supabase
   ```

2. Start Supabase services:
   ```bash
   supabase start
   ```
   This will start PostgreSQL and other Supabase services. Update your `.env` with the provided connection details.

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the development server

```bash
uvicorn app.main:app --reload
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)

## 🚀 Available Commands

### Using Makefile (recommended)

```bash
# Run database migrations
make migrate

# Run tests
make test

# Reset and seed test database
make reset_test_db

# Start development server
make dev

# View all available commands
make help
```

### Manual Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Start production server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## 📦 Dependencies

### Main Dependencies

- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `alembic` - Database migrations
- `pydantic` - Data validation
- `python-jose` - JWT authentication
- `python-dotenv` - Environment variable management
- `psycopg2-binary` - PostgreSQL adapter

### Development Dependencies

- `pytest` - Testing framework
- `httpx` - HTTP client for testing
- `black` - Code formatter
- `isort` - Import sorter
- `mypy` - Static type checking

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Endpoints that require authentication will expect a valid JWT in the `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

## 🐳 Docker Setup

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Run migrations:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

The API will be available at `http://localhost:8000`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.