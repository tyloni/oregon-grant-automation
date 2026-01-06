from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db
from app.routers import auth, profile, grants, applications

settings = get_settings()

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Oregon Grant Automation System",
    description="Automated grant discovery and application system for Oregon preschools and child care providers",
    version="1.0.0"
)

# CORS middleware
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(grants.router)
app.include_router(applications.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Oregon Grant Automation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
