# Oregon Preschool & Child Care Grant Automation System

An intelligent grant discovery and application automation system for Oregon preschool and child care providers.

## Features

- 🔍 **Automated Grant Discovery**: Weekly scraping of 50+ Oregon grant sources
- 🎯 **Smart Matching**: AI-powered grant scoring based on eligibility, success likelihood, and effort
- ✍️ **AI Application Generation**: Generate human-quality grant applications using Google Gemini
- 📊 **Success Tracking**: Track application outcomes and build knowledge base
- 📄 **Document Export**: Generate PDF and DOCX formatted applications
- 👥 **Multi-User Support**: Secure authentication and user profiles

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18 with Vite
- **Database**: SQLite
- **LLM**: Google Gemini API
- **Document Generation**: ReportLab (PDF), python-docx (DOCX)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
python -m app.database  # Initialize database
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000
API docs available at: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend will run at: http://localhost:5173

## Project Structure

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed architecture and implementation details.

## Documentation

- [Implementation Plan](IMPLEMENTATION_PLAN.md) - Complete system architecture and development roadmap
- [API Documentation](docs/API.md) - API endpoint reference
- [User Guide](docs/USER_GUIDE.md) - How to use the system

## Grant Sources

The system monitors these Oregon grant sources:

- Oregon Department of Early Learning and Care (DELC)
- Business Oregon - Child Care Infrastructure Fund
- Oregon SPARK
- Grants.gov (Oregon filtered)
- Collins Foundation, Ford Family Foundation, Meyer Memorial Trust
- Oregon Community Foundation
- And more...

## Development Status

Currently in Phase 1: Foundation
- [x] Project structure
- [ ] Backend API
- [ ] Database setup
- [ ] Authentication
- [ ] Frontend components

## License

MIT License - See LICENSE file for details

## Support

For questions or issues, please see the [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed guidance.
