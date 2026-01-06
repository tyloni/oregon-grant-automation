# Oregon Grant Automation System - Project Documentation

## Project Overview

This is a web application designed to help preschools and child care owners in Oregon find and apply for grants. The system automates grant discovery and uses AI to generate professional grant applications.

**Target Users**: Preschool and child care center owners/operators in Oregon who are not technical users.

## Current Status: Phase 4 - AI Application Generation ✅

### What We've Built

#### Phase 1: Foundation (Complete)
- **Backend**: FastAPI with SQLAlchemy ORM, SQLite database
- **Frontend**: React 18 with Vite, Tailwind CSS
- **Authentication**: JWT-based auth with bcrypt password hashing
- **Database**: 8 tables including users, grants, applications, attachments

#### Phase 2: Sample Data (Complete)
- 8 realistic Oregon grants seeded into the database
- Grants include: Preschool Promise Program, Child Care Infrastructure Fund, Quality Improvement Grants, foundation grants

#### Phase 3: Grant Browsing (Complete)
- Beautiful grant cards with deadline countdown timers
- Color-coded deadlines (urgent, soon, plenty of time)
- Grant details with funding amounts, eligibility, priorities
- Clean navigation between Dashboard and Grants pages

#### Phase 4: AI Application Generation (Complete)
- **Template-based application generator** (no API costs!)
- Generates 7 complete sections:
  - Executive Summary
  - Organizational Background
  - Statement of Need
  - Project Description
  - Expected Outcomes
  - Budget Justification
  - Sustainability Plan
- Applications are customized based on:
  - Organization details (name, type, mission, enrollment, budget, staff)
  - Grant details (title, funding amount, priorities, eligibility)
- Applications can be viewed, edited, and saved

### Technology Stack

**Backend**:
- FastAPI (Python 3.9+)
- SQLAlchemy ORM
- SQLite database
- JWT authentication with bcrypt
- Pydantic for data validation

**Frontend**:
- React 18
- Vite (build tool)
- Tailwind CSS
- React Router v6
- Axios for API calls
- Lucide React (icons)

**Key Features**:
- No external AI API required (template-based generation)
- Works offline
- Free to run
- Instant application generation

## Design System & UI Rules

### Color Palette - New England Patriots Inspired 🏈

**Primary Colors**:
- **Navy**: `#002244` (Patriots navy) - Primary buttons, active states
- **Red**: `#C60C30` (Patriots red) - Accents, highlights, success states

**Supporting Colors**:
- **Dark Navy**: `#00172E` - Hover states, dark text
- **Light Navy**: `#E8EAF0` - Backgrounds, subtle highlights
- **Deep Red**: `#B00B2A` - Alternative accent for important elements
- **Neutral Grays**: For text and backgrounds

### UI/UX Principles

**Critical Rule**: Our users are NOT technical. The interface must be:

1. **Simple & Intuitive**
   - No technical jargon
   - Clear labels and instructions
   - Obvious next steps
   - One primary action per screen

2. **Modern but Not Complex**
   - Clean, spacious layouts
   - Large, tappable buttons
   - Clear visual hierarchy
   - Avoid overwhelming with options

3. **Refined & Professional**
   - Polished, consistent spacing
   - Subtle shadows and borders
   - Professional typography
   - High-contrast text for readability

4. **Minimal Learning Curve**
   - Self-explanatory interfaces
   - Helpful tooltips when needed
   - Progressive disclosure (show advanced features only when needed)
   - Consistent patterns throughout

**Examples of Good UX**:
- ✅ Big "Apply Now" buttons in Patriots navy
- ✅ Clear deadline countdown with color coding
- ✅ Simple form with just 7 fields for org info
- ✅ One-click application generation
- ✅ Plain language labels like "Organization Name" not "Entity Designation"

**Examples to Avoid**:
- ❌ Technical database terms in the UI
- ❌ Multi-step wizards with unclear progress
- ❌ Dense tables of data
- ❌ Acronyms without explanation
- ❌ Hidden features that require discovery

## File Structure

```
/Users/tyler.hall/Desktop/grants/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (User, Grant, Application)
│   │   ├── routers/         # API endpoints (auth, grants, applications)
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic (llm_service.py, auth_service.py)
│   │   ├── utils/           # Utilities (security.py)
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app entry point
│   ├── data/
│   │   └── grants.db        # SQLite database
│   ├── .env                 # Environment variables
│   ├── requirements.txt     # Python dependencies
│   └── seed_grants.py       # Sample data seeder
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/        # Login, Register
│   │   │   ├── grants/      # GrantsList
│   │   │   ├── applications/# ApplicationForm, ApplicationViewer
│   │   │   ├── dashboard/   # Dashboard
│   │   │   └── common/      # Layout, ProtectedRoute
│   │   ├── hooks/           # useAuth.jsx
│   │   ├── services/        # api.js
│   │   ├── App.jsx          # Main app with routing
│   │   └── main.jsx         # React entry point
│   ├── index.html
│   ├── package.json
│   └── tailwind.config.js
└── CLAUDE.md               # This file
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Login and get JWT tokens
- `GET /auth/me` - Get current user info
- `POST /auth/refresh` - Refresh access token

### Grants
- `GET /grants` - List all grants (paginated)
- `GET /grants/{id}` - Get specific grant details

### Applications
- `POST /applications/generate` - Generate new application for a grant
- `GET /applications` - List user's applications
- `GET /applications/{id}` - Get specific application
- `PUT /applications/{id}` - Update application sections
- `POST /applications/{id}/refine` - Refine a section with feedback
- `DELETE /applications/{id}` - Delete application

## Database Schema

### Users Table
- id, email, password_hash, created_at, last_login

### User Profiles Table
- id, user_id, organization_name, organization_type, city, county, mission_statement, etc.

### Grants Table
- id, source_name, source_url, source_type, title, description
- amount_min, amount_max, deadline, application_opens
- eligibility_criteria (JSON), funding_priorities (JSON)
- geographic_restriction, target_populations (JSON)

### Applications Table
- id, user_id, grant_id, status, sections (JSON)
- output_format, file_path, submitted_at, outcome, amount_awarded
- created_at, updated_at

## Running the Application

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

Access at:
- Frontend: http://localhost:5174
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Test Account
- Email: test@test.com
- Password: password123

## Known Issues & Solutions

### Issue 1: CORS Errors
**Problem**: Frontend can't access backend API
**Solution**: Ensure `.env` has both ports: `CORS_ORIGINS=http://localhost:5173,http://localhost:5174`

### Issue 2: Database Schema Mismatch
**Problem**: "table applications has no column named sections"
**Solution**: Run migration to add column (already completed)

### Issue 3: Login Not Working
**Problem**: CORS preflight requests fail
**Solution**: Backend CORS middleware is configured, ensure both services running

## Future Phases (Not Yet Built)

### Phase 5: Grant Discovery Automation
- Web scraping Oregon grant sources
- RSS feed integration
- Scheduled weekly discovery jobs
- Email notifications for new grants

### Phase 6: Advanced Features
- PDF/DOCX export
- Grant match scoring
- Success rate tracking
- Template library from successful applications

### Phase 7: Enhancements
- Email integration for submissions
- Document attachment management
- Collaborative editing
- Admin dashboard

## Development Notes

### Adding New Colors
When adding UI elements, use the Oregon Ducks color scheme:
- Primary actions: Green (`bg-green-700 hover:bg-green-800`)
- Success states: Yellow (`bg-yellow-400`)
- Warnings: Gold (`bg-yellow-600`)
- Keep it simple and consistent

### Adding New Features
1. Keep user simplicity in mind
2. Test with non-technical users
3. Use clear, plain language
4. Provide helpful feedback messages
5. Maintain Oregon Ducks color scheme

### Code Style
- Backend: Follow PEP 8
- Frontend: Use functional components with hooks
- Keep components small and focused
- Comment complex logic
- Use TypeScript-style JSDoc for key functions

## Support & Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- Tailwind CSS: https://tailwindcss.com
- SQLAlchemy: https://docs.sqlalchemy.org

---

**Last Updated**: January 5, 2026
**Current Version**: Phase 4 Complete
**Status**: ✅ Application Generation Working with Template System
