# Setup Guide - Oregon Grant Automation System

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.11 or higher**
   - Download from https://www.python.org/downloads/
   - Verify: `python3 --version`

2. **Node.js 18 or higher**
   - Download from https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **Google Gemini API Key**
   - Get free API key from https://ai.google.dev/
   - You'll need this for AI application generation

4. **macOS Users**: Install Xcode Command Line Tools
   ```bash
   xcode-select --install
   ```

---

## Backend Setup

### Step 1: Navigate to Backend Directory
```bash
cd /Users/tyler.hall/Desktop/grants/backend
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- SQLAlchemy (database ORM)
- Pydantic (data validation)
- Google Gemini AI SDK
- BeautifulSoup4 & Selenium (web scraping)
- ReportLab & python-docx (document generation)
- And more...

### Step 5: Configure Environment Variables

The `.env` file has been created with a secure secret key. You need to:

1. Open `backend/.env` in a text editor
2. Replace `your-gemini-api-key-here` with your actual Gemini API key

```bash
# Example:
GEMINI_API_KEY=AIzaSyB...your-actual-key-here
```

### Step 6: Initialize Database
```bash
python -m app.database
```

You should see: "Database tables created successfully!"

This creates `backend/data/grants.db` with all necessary tables.

### Step 7: Start Backend Server
```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Test the backend:**
- Open browser to http://localhost:8000
- You should see: `{"message": "Oregon Grant Automation System API", ...}`
- API docs: http://localhost:8000/docs

**Keep this terminal window open!**

---

## Frontend Setup

### Step 1: Open New Terminal Window

Navigate to frontend directory:
```bash
cd /Users/tyler.hall/Desktop/grants/frontend
```

### Step 2: Install Node Dependencies
```bash
npm install
```

This will install:
- React 18
- React Router (navigation)
- Axios (API calls)
- Tailwind CSS (styling)
- Vite (build tool)
- And more...

Installation may take 2-3 minutes.

### Step 3: Start Frontend Development Server
```bash
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Test the frontend:**
- Open browser to http://localhost:5173
- You should see the login page

**Keep this terminal window open too!**

---

## Testing the System

### Test 1: User Registration

1. Open http://localhost:5173 in your browser
2. Click "Register here"
3. Enter:
   - Email: `test@example.com`
   - Password: `testpassword123` (min 8 characters)
   - Confirm Password: `testpassword123`
4. Click "Create account"
5. You should be redirected to the Dashboard

### Test 2: Logout and Login

1. Click "Logout" button in top right
2. You should be redirected to login page
3. Login with:
   - Email: `test@example.com`
   - Password: `testpassword123`
4. You should see the Dashboard again

### Test 3: API Documentation

1. Open http://localhost:8000/docs
2. You'll see interactive API documentation (Swagger UI)
3. Try the `/auth/register` and `/auth/login` endpoints

---

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'app'"**
- Make sure you're in the `backend/` directory
- Make sure virtual environment is activated (you see `(venv)`)
- Try: `pip install -r requirements.txt` again

**"Database error" or "Table doesn't exist"**
- Run: `python -m app.database` to recreate tables
- Delete `backend/data/grants.db` and run the command again

**"Cannot import name 'get_settings'"**
- Make sure `.env` file exists in `backend/` directory
- Check that `SECRET_KEY` and `GEMINI_API_KEY` are set

**Port 8000 already in use**
- Another process is using port 8000
- Kill it: `lsof -ti:8000 | xargs kill -9`
- Or use different port: `uvicorn app.main:app --reload --port 8001`

### Frontend Issues

**"npm: command not found"**
- Node.js is not installed
- Install from https://nodejs.org/

**"Failed to fetch"** or **"Network Error"** when logging in
- Backend is not running
- Check that backend is running on http://localhost:8000
- Check browser console for errors (F12 → Console tab)

**Port 5173 already in use**
- Kill the process: `lsof -ti:5173 | xargs kill -9`
- Or Vite will prompt you to use a different port

**Blank page / White screen**
- Open browser console (F12)
- Look for JavaScript errors
- Make sure `npm install` completed successfully

### XCode Tools (macOS)

If you see "xcode-select: error: tool 'git' requires Xcode":
```bash
xcode-select --install
```

Then retry the setup steps.

---

## Development Workflow

### Daily Development

1. **Terminal 1 - Backend:**
   ```bash
   cd /Users/tyler.hall/Desktop/grants/backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd /Users/tyler.hall/Desktop/grants/frontend
   npm run dev
   ```

3. **Browser:**
   - Frontend: http://localhost:5173
   - API Docs: http://localhost:8000/docs

### Making Changes

- Backend changes auto-reload (thanks to `--reload` flag)
- Frontend changes auto-reload (Vite hot module replacement)
- Database changes require restart: `python -m app.database`

---

## Next Steps

Once Phase 1 is working (authentication), you can proceed with:

1. **Phase 2**: Grant Discovery & Scraping
2. **Phase 3**: User Profiles & Matching Algorithm
3. **Phase 4**: LLM Integration & Application Generation
4. **Phase 5**: Document Generation & Compliance
5. **Phase 6**: Success Tracking & Analytics
6. **Phase 7**: Testing & Polish

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed roadmap.

---

## Useful Commands

### Backend

```bash
# Activate venv
source venv/bin/activate

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
pytest

# Check database
sqlite3 data/grants.db
.tables
.schema users
.quit

# Reset database
rm data/grants.db
python -m app.database
```

### Frontend

```bash
# Install new package
npm install package-name

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Support

If you encounter issues:

1. Check this troubleshooting section
2. Review error messages carefully
3. Check [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for architecture details
4. Ensure all prerequisites are installed

## Phase 1 Completion Checklist

- [ ] Backend runs without errors
- [ ] Frontend runs without errors
- [ ] Can register a new user
- [ ] Can login with credentials
- [ ] Dashboard shows after login
- [ ] Logout works
- [ ] Protected routes redirect to login when not authenticated
- [ ] API documentation accessible at /docs

Once all checked, Phase 1 is complete! 🎉
