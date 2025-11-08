# Makefile for backend with Supabase + FastAPI + Alembic + Pytest

# -----------------------------------
# Load environment variables
# -----------------------------------
include .env
export $(shell sed 's/=.*//' .env)

# Variables
DB_URL ?= $(SUPABASE_DB_URL)
TEST_DB ?= supplytracker_test
ALEMBIC ?= alembic
PYTHON ?= python3
SEED_DIR ?= ./supabase/seeds
SEED_FILE ?= ./supabase/seed.sql

# -----------------------------------
# Database management
# -----------------------------------

# Create test database
create_test_db:
	@echo "🧱 Creating test database $(TEST_DB)..."
	psql "$(DB_URL)" -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$(TEST_DB)' AND pid <> pg_backend_pid();" || true
	psql "$(DB_URL)" -c "DROP DATABASE IF EXISTS $(TEST_DB);" || true
	psql "$(DB_URL)" -c "CREATE DATABASE $(TEST_DB) OWNER postgres;"


# Run migrations on main database
migrate:
	@echo "🚀 Running migrations on main database..."
	$(ALEMBIC) upgrade head

# Run migrations on test database
migrate_test:
	APP_ENV=test alembic upgrade head

# Import seeds on main database
seed:
	@echo "🌱 Importing seeds into main database..."
	psql "$(DB_URL)" -f $(SEED_FILE)

# Reset test database (drop + create + migrations + seed)
reset_test_db: create_test_db migrate_test
	@echo "🌾 Importing all seeds into test database..."
	for f in $(SEED_DIR)/*.sql; do \
	  echo "Running $$f"; \
	  APP_ENV=test psql "postgresql://postgres:postgres@127.0.0.1:54322/$(TEST_DB)" -f "$$f"; \
	done
	@echo "✅ Test database reset complete!"

# -----------------------------------
# Testing
# -----------------------------------

# Run tests (quiet mode)
test:
	@echo "🧩 Running tests with pytest..."
	pytest -q

# Run tests with verbose output
test-verbose:
	@echo "🧪 Running verbose tests..."
	pytest -v

# Run tests with coverage
test-cov:
	@echo "📊 Running tests with coverage..."
	pytest --cov=app --cov-report=term-missing

# -----------------------------------
# Utility
# -----------------------------------

# Clean caches or temporary files
clean:
	@echo "🧹 Cleaning caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf *.pyc .pytest_cache .coverage

# Show available commands
help:
	@echo "📘 Makefile targets:"
	@echo "  make create_test_db  -> Creates or recreates the test database"
	@echo "  make migrate         -> Applies migrations to the main database"
	@echo "  make migrate_test    -> Applies migrations to the test database"
	@echo "  make seed            -> Imports seed to the main database"
	@echo "  make reset_test_db   -> Resets the test database (migrations + seed)"
	@echo "  make test            -> Runs all tests (pytest)"
	@echo "  make test-verbose    -> Runs tests with detailed output"
	@echo "  make test-cov        -> Runs tests with coverage report"
	@echo "  make clean           -> Removes cache and temporary files"
