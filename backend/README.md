# Oregon Grant Automation - Backend

FastAPI backend for the Oregon Grant Automation System.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Edit `.env` and add your configuration:
   - Generate a SECRET_KEY: `openssl rand -hex 32`
   - Add your GEMINI_API_KEY

5. Initialize the database:
```bash
python -m app.database
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

## Project Structure

- `app/` - Main application code
  - `models/` - SQLAlchemy database models
  - `schemas/` - Pydantic validation schemas
  - `routers/` - API endpoint routes
  - `services/` - Business logic
  - `scrapers/` - Grant discovery scrapers
  - `utils/` - Utility functions
- `data/` - SQLite database and file storage
- `tests/` - Test files

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login user
- GET `/auth/me` - Get current user
- POST `/auth/refresh` - Refresh access token

### Profile
- GET `/profile` - Get user profile
- POST `/profile` - Create user profile
- PUT `/profile` - Update user profile

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black app/
```
