# Makefile for backend with Supabase + FastAPI + Alembic

# Load backend .env
include .env
export $(shell sed 's/=.*//' .env)

# Variables
DB_URL ?= $(SUPABASE_DB_URL)
TEST_DB ?= supplytracker_test
ALEMBIC ?= alembic
PYTHON ?= python3
SEED_FILE ?= ./supabase/seed.sql

# -----------------------
# Main targets
# -----------------------

# Create test database
create_test_db:
	@echo "Creating test database $(TEST_DB)..."
	psql "$(DB_URL)" -c "DROP DATABASE IF EXISTS $(TEST_DB);"
	psql "$(DB_URL)" -c "CREATE DATABASE $(TEST_DB) OWNER postgres;"

# Run migrations on main database
migrate:
	@echo "Running migrations on main database..."
	$(ALEMBIC) upgrade head

# Run migrations on test database
migrate_test:
	@echo "Running migrations on test database..."
	APP_ENV=test $(ALEMBIC) upgrade head

# Import seed on main database
seed:
	@echo "Importing seed on main database..."
	psql "$(DB_URL)" -f $(SEED_FILE)

# Reset test database (drop + create + migrations + seed)
reset_test_db: create_test_db migrate_test
	@echo "Importing seed on test database..."
	APP_ENV=test psql "postgresql://postgres:postgres@127.0.0.1:54322/$(TEST_DB)" -f $(SEED_FILE)
	@echo "Test database reset!"

# Run tests
test: reset_test_db
	@echo "Running tests..."
	$(PYTHON) -m pytest tests --env-file .env

# Clean caches or temporary files
clean:
	@echo "Cleaning caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf *.pyc

# -----------------------
# Help
# -----------------------
help:
	@echo "Makefile targets:"
	@echo "  make create_test_db  -> Creates or recreates the test database"
	@echo "  make migrate         -> Applies migrations to the main database"
	@echo "  make migrate_test    -> Applies migrations to the test database"
	@echo "  make seed            -> Imports seed to the main database"
	@echo "  make reset_test_db   -> Resets the test database (migrations + seed)"
	@echo "  make test            -> Runs all tests (uses test database)"
	@echo "  make clean           -> Cleans __pycache__ and .pyc files"
