# Oregon Preschool & Child Care Grant Automation System
## Implementation Plan

---

## Executive Summary

This plan outlines the development of a local-first, beginner-friendly grant automation system for Oregon preschool and child care providers. The system will automatically discover grants, match them to user profiles, and generate human-quality grant applications using Google Gemini AI.

**Tech Stack:**
- **Backend:** Python 3.11+ with FastAPI
- **Frontend:** React 18+ with Vite
- **Database:** SQLite
- **LLM:** Google Gemini API
- **Deployment:** Local development server

---

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  (Dashboard, Grant Browser, Application Editor)         │
└─────────────────┬───────────────────────────────────────┘
                  │ REST API
┌─────────────────▼───────────────────────────────────────┐
│              FastAPI Backend                             │
│  ┌──────────────┬──────────────┬────────────────────┐  │
│  │ Auth Service │ Grant Service│ Application Service│  │
│  └──────────────┴──────────────┴────────────────────┘  │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┼───────────────────────────────────────┐
│                 │      Data Layer                        │
│  ┌──────────────▼──────────────┬────────────────────┐  │
│  │   SQLite Database           │  File Storage       │  │
│  │  (Users, Grants, Apps)      │  (PDFs, Uploads)    │  │
│  └─────────────────────────────┴────────────────────┘  │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┼───────────────────────────────────────┐
│                 │   External Services                    │
│  ┌──────────────▼──┬─────────────┬──────────────────┐  │
│  │ Grant Scrapers  │ Grants.gov  │ Google Gemini    │  │
│  │ (Weekly Cron)   │    API      │      API         │  │
│  └─────────────────┴─────────────┴──────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### User Profiles Table
```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    organization_name TEXT NOT NULL,
    organization_type TEXT, -- 'preschool', 'daycare', 'childcare_center'
    tax_id TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT DEFAULT 'OR',
    zip_code TEXT,
    county TEXT,
    phone TEXT,
    website TEXT,
    mission_statement TEXT,
    established_year INTEGER,
    current_enrollment INTEGER,
    max_capacity INTEGER,
    age_range_served TEXT, -- '0-3', '3-5', '0-5', etc.
    operating_budget REAL,
    staff_count INTEGER,
    licensed BOOLEAN,
    license_number TEXT,
    accreditations TEXT, -- JSON array
    populations_served TEXT, -- JSON array: low-income, disabilities, etc.
    rural_or_urban TEXT,
    additional_info TEXT, -- JSON for flexible fields
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Grants Table
```sql
CREATE TABLE grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL, -- 'Preschool Promise', 'CCIF', etc.
    source_url TEXT,
    source_type TEXT, -- 'state', 'federal', 'foundation', 'private'
    title TEXT NOT NULL,
    description TEXT,
    amount_min REAL,
    amount_max REAL,
    deadline TIMESTAMP,
    application_opens TIMESTAMP,
    eligibility_criteria TEXT, -- JSON
    required_documents TEXT, -- JSON array
    application_url TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    geographic_restriction TEXT, -- 'statewide', 'rural', specific counties
    target_populations TEXT, -- JSON array
    funding_priorities TEXT, -- JSON array
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active' -- 'active', 'closed', 'archived'
);
```

### Grant Matches Table
```sql
CREATE TABLE grant_matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    grant_id INTEGER NOT NULL,
    eligibility_score REAL, -- 0-100
    success_likelihood_score REAL, -- 0-100
    effort_score REAL, -- 0-100 (lower is better)
    overall_score REAL, -- weighted composite
    match_reasons TEXT, -- JSON array of why it matches
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (grant_id) REFERENCES grants(id),
    UNIQUE(user_id, grant_id)
);
```

### Applications Table
```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    grant_id INTEGER NOT NULL,
    status TEXT DEFAULT 'draft', -- 'draft', 'in_review', 'submitted', 'won', 'lost'
    generated_content TEXT, -- JSON with all generated sections
    user_edits TEXT, -- JSON tracking user modifications
    output_format TEXT, -- 'pdf', 'docx'
    file_path TEXT, -- path to generated document
    submitted_at TIMESTAMP,
    outcome TEXT, -- 'pending', 'awarded', 'rejected', NULL
    amount_awarded REAL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (grant_id) REFERENCES grants(id)
);
```

### Application Attachments Table
```sql
CREATE TABLE application_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT, -- 'budget', 'certificate', 'letter', 'other'
    file_path TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id)
);
```

### Success Templates Table
```sql
CREATE TABLE success_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_source_name TEXT, -- to match similar grants
    application_id INTEGER, -- reference to successful application
    winning_strategies TEXT, -- JSON: key elements that worked
    template_sections TEXT, -- JSON: reusable content templates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id)
);
```

### Scraper Jobs Table
```sql
CREATE TABLE scraper_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    status TEXT, -- 'success', 'failed', 'running'
    grants_found INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Grant Discovery Sources

### Primary Sources (from research):

#### State Government
1. **Oregon Department of Early Learning and Care (DELC)**
   - Preschool Promise (PSP)
   - Baby Promise
   - Early Child Equity Fund (ECEF)
   - Employment Related Day Care (ERDC)
   - Child Care Development Fund (CCDF)
   - URL: oregon.gov/delc/programs

2. **Business Oregon - Child Care Infrastructure Fund**
   - $50M lottery bond funding
   - Property acquisition, construction, renovation grants
   - URL: oregon.gov/biz/programs/child_care_infrastructure

3. **Oregon SPARK**
   - Quality improvement grants
   - URL: oregonspark.org/early-educators/grants

#### Federal
4. **Grants.gov API**
   - Filter: Oregon + Child Care + Education
   - Head Start/Early Head Start
   - URL: grants.gov/search

5. **USDA Rural Development**
   - Community Facilities Direct Loan and Grant
   - Rural areas ≤20,000 residents
   - URL: rd.usda.gov/programs-services

#### Foundations
6. **Collins Foundation** - collinsfoundation.org
7. **Ford Family Foundation** - tfff.org/grants
8. **Meyer Memorial Trust** - mmt.org/apply
9. **Oregon Community Foundation** - oregoncf.org/grants-and-scholarships
10. **PNC Foundation (Grow Up Great)** - pnc.com/about-pnc/corporate-responsibility

#### Support Organizations
11. **Oregon Child Care Alliance (OCCA)** - oregonchildcarealliance.org
12. **Child Care Resource & Referrals** - 15 regional offices

---

## Project Structure

```
grants/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration & environment vars
│   │   ├── database.py                # SQLite connection & models
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── grant.py
│   │   │   ├── application.py
│   │   │   └── profile.py
│   │   ├── schemas/                   # Pydantic schemas for validation
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── grant.py
│   │   │   ├── application.py
│   │   │   └── profile.py
│   │   ├── routers/                   # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Login, register, JWT
│   │   │   ├── grants.py              # Grant CRUD & search
│   │   │   ├── applications.py        # Application generation & management
│   │   │   ├── profile.py             # User profile management
│   │   │   └── analytics.py           # Success rate reporting
│   │   ├── services/                  # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── grant_matcher.py       # Scoring & matching algorithm
│   │   │   ├── llm_service.py         # Gemini API integration
│   │   │   ├── document_generator.py  # PDF/DOCX generation
│   │   │   ├── humanizer.py           # AI detection avoidance
│   │   │   └── compliance_checker.py  # Grant requirement validation
│   │   ├── scrapers/                  # Grant discovery
│   │   │   ├── __init__.py
│   │   │   ├── base_scraper.py        # Abstract base class
│   │   │   ├── delc_scraper.py        # Oregon DELC
│   │   │   ├── business_oregon_scraper.py
│   │   │   ├── grants_gov_scraper.py  # Grants.gov API
│   │   │   ├── foundation_scrapers.py # Private foundations
│   │   │   ├── rss_scraper.py         # RSS feed monitor
│   │   │   └── scheduler.py           # Weekly cron jobs
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py            # Password hashing, JWT
│   │       ├── email.py               # Future: email notifications
│   │       └── logger.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_scrapers.py
│   │   ├── test_matcher.py
│   │   └── test_llm.py
│   ├── data/                          # SQLite DB & uploads
│   │   ├── grants.db
│   │   ├── uploads/
│   │   └── generated/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.jsx                   # Entry point
│   │   ├── App.jsx                    # Root component
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── GrantsList.jsx
│   │   │   │   ├── GrantCard.jsx
│   │   │   │   └── StatsOverview.jsx
│   │   │   ├── profile/
│   │   │   │   ├── ProfileForm.jsx
│   │   │   │   └── ProfileView.jsx
│   │   │   ├── applications/
│   │   │   │   ├── ApplicationEditor.jsx
│   │   │   │   ├── ApplicationList.jsx
│   │   │   │   ├── DocumentPreview.jsx
│   │   │   │   └── AttachmentUploader.jsx
│   │   │   ├── analytics/
│   │   │   │   ├── SuccessRates.jsx
│   │   │   │   └── GrantHistory.jsx
│   │   │   └── common/
│   │   │       ├── Navbar.jsx
│   │   │       ├── Sidebar.jsx
│   │   │       ├── Button.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useGrants.js
│   │   │   └── useApplications.js
│   │   ├── services/
│   │   │   └── api.js                 # Axios configuration
│   │   ├── utils/
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   ├── styles/
│   │   │   └── index.css              # Tailwind or basic CSS
│   │   └── config.js
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── README.md
│
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── .gitignore
└── README.md
```

---

## Core Features & Implementation Details

### 1. Authentication System

**Technology:** JWT (JSON Web Tokens)

**Implementation:**
- Password hashing with bcrypt
- Access token (15min expiry) + Refresh token (7 day expiry)
- Protected routes middleware

**Files:**
- `backend/app/routers/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/utils/security.py`

### 2. Grant Discovery & Scraping

**Weekly Scheduled Jobs:**
- APScheduler for cron-like scheduling
- Run every Sunday at 2 AM
- Each scraper as independent task

**Scraper Types:**

**A. HTML/JavaScript Scrapers (Beautiful Soup + Selenium)**
- Oregon DELC website
- Business Oregon
- Foundation websites
- Handles dynamic JavaScript content

**B. API Integrations**
- Grants.gov API (official REST API)
- Any foundation APIs if available

**C. RSS/Atom Feed Monitors**
- Parse XML feeds
- Track new entries by GUID/pubDate

**Data Extraction:**
- Title, description, deadline
- Eligibility criteria (text parsing + LLM extraction)
- Amount ranges
- Contact information
- Application URLs

**Storage:**
- Deduplicate by URL + title hash
- Update existing grants if changed
- Mark as inactive if no longer available

**Files:**
- `backend/app/scrapers/scheduler.py`
- Individual scraper files for each source

### 3. Grant Matching & Scoring Algorithm

**Eligibility Score (0-100):**
```python
def calculate_eligibility_score(user_profile, grant):
    score = 0

    # Geographic match (30 points)
    if grant.geographic_restriction == 'statewide':
        score += 30
    elif user_profile.county in grant.allowed_counties:
        score += 30
    elif grant.rural_requirement and user_profile.rural_or_urban == 'rural':
        score += 30

    # Population served match (25 points)
    if overlap(user_profile.populations_served, grant.target_populations):
        score += 25 * (overlap_percentage)

    # Organization type match (20 points)
    if user_profile.organization_type in grant.eligible_org_types:
        score += 20

    # Licensing/accreditation (15 points)
    if grant.requires_license and user_profile.licensed:
        score += 10
    if grant.requires_accreditation and user_profile.accreditations:
        score += 5

    # Financial capacity (10 points)
    budget_ratio = user_profile.operating_budget / grant.amount_max
    if 0.1 <= budget_ratio <= 2.0:  # Sweet spot
        score += 10

    return score
```

**Success Likelihood Score (0-100):**
```python
def calculate_success_likelihood(user_profile, grant, historical_data):
    score = 50  # baseline

    # Check past similar applications
    similar_grants = find_similar_grants(grant, historical_data)
    if similar_grants:
        win_rate = sum(g.outcome == 'awarded' for g in similar_grants) / len(similar_grants)
        score += (win_rate - 0.5) * 40  # Adjust ±20 points

    # Grant competitiveness (estimated by amount and restrictions)
    if grant.amount_max > 100000:
        score -= 10  # More competitive
    if grant.eligibility_criteria_count < 5:
        score -= 10  # Less targeted, more applicants

    # User profile completeness
    profile_completeness = count_filled_fields(user_profile) / total_fields
    score += profile_completeness * 20

    # Alignment with funding priorities
    priority_match = calculate_text_similarity(
        user_profile.mission_statement,
        grant.funding_priorities
    )
    score += priority_match * 20

    return min(max(score, 0), 100)
```

**Effort Score (0-100, lower is better):**
```python
def calculate_effort_score(grant):
    score = 0

    # Number of required documents
    score += len(grant.required_documents) * 5

    # Application complexity (estimated from description length)
    if len(grant.description) > 2000:
        score += 20

    # Time until deadline
    days_until_deadline = (grant.deadline - now()).days
    if days_until_deadline < 14:
        score += 30  # Rushed = more effort
    elif days_until_deadline > 90:
        score += 10  # Too far = less urgent

    # Form vs narrative application
    if 'narrative' in grant.application_url.lower():
        score += 15

    return min(score, 100)
```

**Overall Score:**
```python
overall_score = (
    eligibility_score * 0.50 +
    success_likelihood * 0.35 +
    (100 - effort_score) * 0.15
)
```

**Files:**
- `backend/app/services/grant_matcher.py`

### 4. LLM Integration (Google Gemini)

**Model:** `gemini-1.5-pro` or `gemini-1.5-flash` (faster, cheaper)

**Use Cases:**
1. Grant eligibility extraction from unstructured text
2. Application narrative generation
3. Content humanization

**API Configuration:**
```python
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Safety settings to allow all content
safety_settings = {
    'HARASSMENT': 'block_none',
    'HATE_SPEECH': 'block_none',
    'SEXUALLY_EXPLICIT': 'block_none',
    'DANGEROUS_CONTENT': 'block_none'
}
```

**Prompt Template for Application Generation:**
```python
GRANT_APPLICATION_PROMPT = """
You are writing a grant application on behalf of {organization_name}, a {organization_type} in {city}, Oregon.

GRANT DETAILS:
- Grant Name: {grant_title}
- Funding Amount: {grant_amount}
- Purpose: {grant_description}
- Eligibility Criteria: {eligibility_criteria}
- Funding Priorities: {funding_priorities}

ORGANIZATION PROFILE:
{profile_data}

INSTRUCTIONS:
Write a compelling, professional grant application narrative that:
1. Addresses all eligibility criteria explicitly
2. Demonstrates clear alignment with funding priorities
3. Uses specific data from the organization profile
4. Maintains a {tone} tone (professional/passionate/community-focused)
5. Varies sentence structure and length naturally
6. Includes occasional minor stylistic imperfections to sound human-written
7. Answers these specific questions: {application_questions}

STRUCTURE:
1. Executive Summary (2-3 paragraphs)
2. Organizational Background (3-4 paragraphs)
3. Need Statement (4-5 paragraphs)
4. Project Description (5-6 paragraphs)
5. Expected Outcomes (3-4 paragraphs)
6. Budget Justification (2-3 paragraphs)
7. Sustainability Plan (2-3 paragraphs)

Write in a way that feels authentic and human, not AI-generated.
"""
```

**Files:**
- `backend/app/services/llm_service.py`

### 5. AI Humanization Techniques

**Post-processing to avoid AI detection:**

```python
class ApplicationHumanizer:

    def humanize(self, text: str) -> str:
        """Apply multiple techniques to make AI text undetectable"""

        # 1. Vary sentence structure
        text = self.vary_sentence_structure(text)

        # 2. Add intentional minor imperfections
        text = self.add_subtle_imperfections(text)

        # 3. Adjust vocabulary diversity
        text = self.adjust_vocabulary(text)

        # 4. Remove AI-typical patterns
        text = self.remove_ai_patterns(text)

        return text

    def vary_sentence_structure(self, text: str) -> str:
        """Ensure mix of short, medium, and long sentences"""
        sentences = nltk.sent_tokenize(text)

        # Calculate sentence length distribution
        lengths = [len(s.split()) for s in sentences]

        # If too uniform, request regeneration with specific guidance
        # Or manually break/combine sentences

        return text

    def add_subtle_imperfections(self, text: str) -> str:
        """Add human-like variations"""

        # Occasionally split compound sentences
        text = re.sub(
            r'(, and |; )',
            lambda m: '. ' if random.random() < 0.1 else m.group(0),
            text
        )

        # Replace some formal transitions with casual ones
        replacements = {
            'Furthermore,': ['Additionally,', 'Moreover,', 'Also,'],
            'Therefore,': ['Thus,', 'So,', 'As a result,'],
            'In conclusion,': ['To sum up,', 'Ultimately,', 'In short,']
        }

        for formal, casual_options in replacements.items():
            if formal in text and random.random() < 0.3:
                text = text.replace(formal, random.choice(casual_options), 1)

        return text

    def remove_ai_patterns(self, text: str) -> str:
        """Remove common AI tells"""

        ai_phrases = [
            'delve into',
            'dive deep',
            'it is important to note that',
            'in today\'s rapidly changing world',
            'leverage',
            'robust',
            'cutting-edge',
            'state-of-the-art',
            'game-changer',
            'revolutionize'
        ]

        for phrase in ai_phrases:
            # Replace with simpler alternatives
            text = text.replace(phrase, self.get_alternative(phrase))

        return text

    def adjust_tone(self, text: str, tone: str) -> str:
        """Modify text to match desired tone"""

        if tone == 'professional':
            # Keep formal, reduce contractions
            text = text.replace("we're", "we are")
            text = text.replace("don't", "do not")

        elif tone == 'passionate':
            # Add emotive language (carefully)
            # Request LLM to regenerate with passion
            pass

        return text
```

**Files:**
- `backend/app/services/humanizer.py`

### 6. Document Generation

**PDF Generation:** ReportLab
**DOCX Generation:** python-docx

**Template Structure:**
```python
def generate_application_pdf(application_data):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate(f"application_{application_data.id}.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Header
    story.append(Paragraph(f"<b>{grant.title}</b>", styles['Title']))
    story.append(Spacer(1, 12))

    # Organization info
    story.append(Paragraph(f"<b>Applicant:</b> {profile.organization_name}", styles['Normal']))

    # Generated content sections
    for section_name, section_content in application_data.generated_content.items():
        story.append(Paragraph(f"<b>{section_name}</b>", styles['Heading2']))
        story.append(Paragraph(section_content, styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)

    return doc.filename
```

**Files:**
- `backend/app/services/document_generator.py`

### 7. Compliance Checker

**Validates applications against grant requirements:**

```python
class ComplianceChecker:

    def check_compliance(self, application, grant):
        issues = []

        # Check required sections present
        required_sections = self.extract_required_sections(grant)
        for section in required_sections:
            if section not in application.generated_content:
                issues.append(f"Missing required section: {section}")

        # Check word count limits
        if grant.max_words:
            total_words = sum(len(content.split()) for content in application.generated_content.values())
            if total_words > grant.max_words:
                issues.append(f"Exceeds word limit: {total_words}/{grant.max_words}")

        # Check eligibility criteria addressed
        for criterion in grant.eligibility_criteria:
            if not self.criterion_addressed(criterion, application.generated_content):
                issues.append(f"Eligibility criterion not addressed: {criterion}")

        # Check required attachments
        for required_doc in grant.required_documents:
            if not self.has_attachment(application, required_doc):
                issues.append(f"Missing required document: {required_doc}")

        # Check deadline
        if grant.deadline < datetime.now():
            issues.append("Grant deadline has passed")

        return {
            'compliant': len(issues) == 0,
            'issues': issues
        }
```

**Files:**
- `backend/app/services/compliance_checker.py`

### 8. Frontend Components

**Dashboard View:**
- Summary stats: Total grants found, Applications in progress, Success rate
- Quick actions: New application, View profile, Browse grants
- Recent activity feed

**Grant Browser:**
- List of matched grants sorted by overall score
- Filters: Deadline range, Amount range, Status
- Grant cards showing:
  - Title, source, amount
  - Deadline countdown
  - Match scores (eligibility, success, effort)
  - "Apply Now" button

**Application Editor:**
- Left panel: Grant details and requirements
- Main panel: Generated content by section
- Edit directly in rich text editor
- Right panel: Compliance checklist
- Bottom: Save draft, Generate PDF, Generate DOCX, Submit

**Profile Management:**
- Form with all organization fields
- Dynamic additional fields (user can add custom info)
- Save and reuse across applications

**Analytics Dashboard:**
- Success rate chart (won/lost/pending)
- Historical grants applied to
- Average time to complete applications
- Most successful grant types

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Use Claude Code Agents:**
- General-purpose agent for project scaffolding
- Plan agent for architecture decisions

**Tasks:**
1. Set up project structure
2. Initialize FastAPI backend with basic routes
3. Set up React + Vite frontend
4. Configure SQLite database and create all tables
5. Implement authentication (register, login, JWT)
6. Basic frontend routing and navbar

**Deliverables:**
- Working auth system
- Empty dashboard
- Database schema implemented

### Phase 2: Grant Discovery (Week 2)
**Use Claude Code Agents:**
- Explore agent to understand grant website structures
- General-purpose agent for scraper implementation

**Tasks:**
1. Build base scraper class
2. Implement Grants.gov API scraper
3. Implement Oregon DELC web scraper
4. Implement Business Oregon scraper
5. Set up APScheduler for weekly jobs
6. Create grant CRUD endpoints
7. Build grant browser UI

**Deliverables:**
- At least 3 working scrapers
- Weekly scheduled grant discovery
- Grant browsing interface

### Phase 3: User Profiles & Matching (Week 3)
**Use Claude Code Agents:**
- General-purpose agent for business logic

**Tasks:**
1. Build user profile form and API
2. Implement grant matching algorithm
3. Calculate all three scores (eligibility, success, effort)
4. Create grant match endpoint
5. Display match scores in UI
6. Add filtering and sorting to grant browser

**Deliverables:**
- Complete profile management
- Working matching algorithm
- Scored grant recommendations

### Phase 4: LLM Integration & Application Generation (Week 4)
**Use Claude Code Agents:**
- General-purpose agent for Gemini integration
- Test iterations with real grant data

**Tasks:**
1. Set up Google Gemini API integration
2. Build prompt templates for application generation
3. Implement humanization post-processing
4. Create application generation endpoint
5. Build application editor UI
6. Implement revision workflow

**Deliverables:**
- Working LLM application generation
- Human-quality output
- Editable drafts

### Phase 5: Document Generation & Compliance (Week 5)
**Use Claude Code Agents:**
- General-purpose agent for document generation

**Tasks:**
1. Implement PDF generation with ReportLab
2. Implement DOCX generation with python-docx
3. Build compliance checker
4. Create file upload for attachments
5. Build document preview in UI
6. Add export buttons

**Deliverables:**
- PDF and DOCX export
- Attachment management
- Compliance validation

### Phase 6: Success Tracking & Analytics (Week 6)
**Use Claude Code Agents:**
- General-purpose agent for analytics implementation

**Tasks:**
1. Build application status tracking
2. Create success templates from won grants
3. Implement analytics endpoints
4. Build analytics dashboard UI
5. Add success rate calculations
6. Knowledge base of successful applications

**Deliverables:**
- Complete application lifecycle tracking
- Analytics dashboard
- Success template system

### Phase 7: Polish & Testing (Week 7)
**Use Claude Code Agents:**
- General-purpose agent for testing

**Tasks:**
1. Write unit tests for critical functions
2. Integration tests for scrapers
3. End-to-end testing of application flow
4. UI/UX improvements
5. Error handling and validation
6. Documentation

**Deliverables:**
- Tested, production-ready system
- User documentation
- Deployment guide

---

## Technology Dependencies

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4  # Password hashing
python-multipart==0.0.6  # File uploads
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0

# LLM
google-generativeai==0.3.1

# Web scraping
beautifulsoup4==4.12.2
selenium==4.15.2
requests==2.31.0
feedparser==6.0.10

# Document generation
reportlab==4.0.7
python-docx==1.1.0
Pillow==10.1.0

# NLP for humanization
nltk==3.8.1

# Scheduling
apscheduler==3.10.4

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "react-hook-form": "^7.48.2",
    "date-fns": "^2.30.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

---

## Configuration

### Environment Variables (.env)

**Backend:**
```bash
# Database
DATABASE_URL=sqlite:///./data/grants.db

# Security
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Grants.gov API
GRANTS_GOV_API_KEY=your-grants-gov-key  # Optional, public API available

# Scraping
SCRAPER_USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
SCRAPER_SCHEDULE_CRON=0 2 * * 0  # Every Sunday at 2 AM

# File Storage
UPLOAD_DIR=./data/uploads
GENERATED_DIR=./data/generated
MAX_UPLOAD_SIZE_MB=10

# Development
DEBUG=True
CORS_ORIGINS=http://localhost:5173  # Vite dev server
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

---

## API Endpoints Overview

### Authentication
- `POST /auth/register` - Create new user
- `POST /auth/login` - Login and get JWT
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user

### User Profile
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `POST /profile/additional-field` - Add custom field

### Grants
- `GET /grants` - List all grants (with filters)
- `GET /grants/{id}` - Get grant details
- `GET /grants/matched` - Get grants matched to user profile
- `POST /grants/search` - Search grants by criteria

### Applications
- `GET /applications` - List user's applications
- `GET /applications/{id}` - Get application details
- `POST /applications/generate` - Generate new application from grant
- `PUT /applications/{id}` - Update application content
- `POST /applications/{id}/regenerate` - Regenerate section with LLM
- `POST /applications/{id}/export/pdf` - Export as PDF
- `POST /applications/{id}/export/docx` - Export as DOCX
- `PUT /applications/{id}/status` - Update application status
- `POST /applications/{id}/attachments` - Upload attachment
- `DELETE /applications/{id}/attachments/{attachment_id}` - Remove attachment

### Analytics
- `GET /analytics/success-rate` - Get overall success statistics
- `GET /analytics/history` - Get application history
- `GET /analytics/templates` - Get successful application templates

### Admin/Scraping
- `POST /admin/scrape/run` - Manually trigger scraper
- `GET /admin/scrape/status` - Get scraper job status

---

## Success Metrics

**System Performance:**
- Grant discovery: Find 50+ active Oregon grants
- Matching accuracy: 85%+ user satisfaction with recommendations
- Application quality: Undetectable by AI detection tools (GPTZero, etc.)
- Generation speed: < 30 seconds for full application

**User Experience:**
- Time to first application: < 15 minutes (profile setup + generation)
- Application win rate: Track and optimize
- User retention: Multi-use profile system encourages reuse

---

## Security Considerations

1. **Authentication:**
   - Secure password hashing (bcrypt)
   - JWT with short expiry
   - HTTP-only cookies for refresh tokens (optional)

2. **Data Protection:**
   - SQLite with file permissions (600)
   - Sensitive data (tax ID) encrypted at rest (optional)
   - API key stored in environment variables only

3. **Input Validation:**
   - Pydantic schemas for all API inputs
   - File upload size limits
   - Sanitize user input before LLM prompts

4. **Rate Limiting:**
   - Limit LLM API calls per user (prevent abuse)
   - Scraper rate limiting to avoid IP bans

5. **CORS:**
   - Restrict to frontend origin only
   - No wildcard in production

---

## Future Enhancements (Post-MVP)

1. **Email notifications** for deadlines (SendGrid/Mailgun)
2. **Multi-LLM support** (fallback to Claude/GPT if Gemini fails)
3. **Collaborative applications** (multiple users, one org)
4. **Mobile app** (React Native)
5. **Grant recommendation engine** using ML (TensorFlow)
6. **Automated submission** where possible (form filling with Selenium)
7. **Integration with accounting software** (QuickBooks API)
8. **Advanced analytics** (grant ROI, time-to-award)
9. **Public deployment** (Docker + AWS/Railway)
10. **Paid tiers** (more LLM calls, priority support)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scrapers break due to website changes | Implement health checks, alerts, fallback to manual entry |
| LLM API costs too high | Use Gemini Flash (cheaper), implement caching, rate limits |
| AI detection evolves | Continuously update humanization techniques, A/B test |
| Grant eligibility mismatches | Manual review workflow, compliance checker |
| Data loss | Regular SQLite backups, export functionality |
| Slow scraping | Async scrapers, parallel execution |

---

## Getting Started (Quick Start Guide)

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Google Gemini API key

**Setup Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Gemini API key
python -m app.database  # Initialize DB
uvicorn app.main:app --reload
```

**Setup Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Claude Code Agent Usage Plan

### When Building This Project:

1. **Initial Scaffolding:**
   - Use **general-purpose agent** to create project structure
   - Generate boilerplate FastAPI and React apps

2. **Database Design:**
   - Use **Plan agent** to review database schema
   - Ensure optimal relationships and indexing

3. **Scraper Development:**
   - Use **Explore agent** to analyze grant website structures
   - Use **general-purpose agent** to implement scrapers
   - Test each scraper independently

4. **LLM Integration:**
   - Use **general-purpose agent** for Gemini API setup
   - Iteratively test prompts with real grant data
   - Use **general-purpose agent** for humanization refinement

5. **Frontend Components:**
   - Use **general-purpose agent** to build React components
   - Follow design system (simple, clean UI as requested)

6. **Testing:**
   - Use **general-purpose agent** to write unit tests
   - Integration testing for end-to-end flows

7. **Documentation:**
   - Use **general-purpose agent** to generate API docs
   - Create user guide

---

## Support & Resources

**Brightwheel Oregon Grants Blog:**
- [Navigating Childcare Grants in Oregon](https://mybrightwheel.com/blog/grants-for-childcare-providers-in-oregon)

**Government Resources:**
- [Oregon Department of Early Learning and Care](https://www.oregon.gov/delc)
- [Business Oregon Child Care Infrastructure Fund](https://www.oregon.gov/biz/programs/child_care_infrastructure)
- [Grants.gov](https://www.grants.gov)
- [Oregon SPARK](https://oregonspark.org)

**Foundation Resources:**
- [Collins Foundation](https://collinsfoundation.org)
- [Ford Family Foundation](https://tfff.org/grants)
- [Meyer Memorial Trust](https://mmt.org/apply)
- [Oregon Community Foundation](https://oregoncf.org/grants-and-scholarships)

---

## Conclusion

This implementation plan provides a complete roadmap for building a fully functional, beginner-friendly grant automation system. The tech stack (Python/FastAPI + React + SQLite + Gemini) is free/cheap, well-documented, and easy to learn.

The system will:
- Automatically discover 50+ Oregon grants weekly
- Match grants to user profiles with 85%+ accuracy
- Generate human-quality applications in under 30 seconds
- Support multi-user authentication
- Track success rates and build a knowledge base

By following the phased approach and leveraging Claude Code agents, you can build this system efficiently while maintaining clean architecture and best practices.

**Total Estimated Development Time:** 7 weeks (can be accelerated with focused effort)

**Total Estimated Cost:**
- Development: $0 (your time)
- APIs: ~$10-50/month (Gemini API usage)
- Hosting (future): $0 (local) or $5-20/month (cloud)

Ready to start building!
