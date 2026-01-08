#!/bin/bash

# Create data directories if they don't exist
mkdir -p data/uploads data/generated

# Initialize database and seed grants
python -c "from app.database import init_db; init_db()"
python seed_grants.py

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
