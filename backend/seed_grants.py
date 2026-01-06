"""
Seed the database with sample Oregon grants for testing
"""
import sys
from datetime import datetime, timedelta
from app.database import SessionLocal, init_db
from app.models.grant import Grant
import json

# Initialize database
init_db()

# Sample grants based on real Oregon programs
sample_grants = [
    {
        "source_name": "Oregon Department of Early Learning and Care",
        "source_url": "https://oregon.gov/delc/programs/Pages/preschool-promise.aspx",
        "source_type": "state",
        "title": "Preschool Promise Program (PSP) - 2026 Round 1",
        "description": "The Preschool Promise Program provides funding to early learning providers to offer free, high-quality preschool services to children from low-income families. Funding supports operational costs, staff professional development, and program quality improvements. Priority given to programs serving children from families at or below 200% of federal poverty level.",
        "amount_min": 50000.0,
        "amount_max": 250000.0,
        "deadline": datetime.now() + timedelta(days=45),
        "application_opens": datetime.now() - timedelta(days=7),
        "eligibility_criteria": json.dumps([
            "Licensed child care provider in Oregon",
            "Serve children ages 3-5",
            "Minimum 75% enrollment from low-income families",
            "Quality rating of 3+ stars in Oregon SPARK system (or commitment to achieve)",
            "Willingness to participate in professional development",
            "Ability to provide full-day programming"
        ]),
        "required_documents": json.dumps([
            "Current Oregon child care license",
            "Program budget for grant period",
            "Staff qualifications and background checks",
            "Enrollment demographics",
            "Quality improvement plan",
            "Parent engagement strategy"
        ]),
        "application_url": "https://oregon.gov/delc/programs/Pages/preschool-promise.aspx",
        "contact_email": "psp.program@delc.oregon.gov",
        "contact_phone": "503-947-1400",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Low-income families (at or below 200% FPL)",
            "Children ages 3-5",
            "Working families",
            "Families experiencing homelessness",
            "Children with disabilities"
        ]),
        "funding_priorities": json.dumps([
            "Equity and inclusion for historically underserved communities",
            "High-quality, culturally responsive programming",
            "Support for dual language learners",
            "Comprehensive services (health, nutrition, family support)",
            "Staff compensation and professional development"
        ]),
        "status": "active"
    },
    {
        "source_name": "Business Oregon",
        "source_url": "https://www.oregon.gov/biz/programs/child_care_infrastructure",
        "source_type": "state",
        "title": "Child Care Infrastructure Fund - Round 4 (Construction & Renovation)",
        "description": "The Child Care Infrastructure Fund provides grants and loans for child care facilities to expand capacity through property acquisition, construction, or major renovation. This round focuses on projects that will create at least 20 new child care slots. Funding can cover construction costs, equipment, playground development, and accessibility improvements.",
        "amount_min": 100000.0,
        "amount_max": 2000000.0,
        "deadline": datetime.now() + timedelta(days=60),
        "application_opens": datetime.now() - timedelta(days=14),
        "eligibility_criteria": json.dumps([
            "Licensed or license-ready child care provider",
            "Project creates minimum 20 new child care slots",
            "Located in Oregon",
            "Demonstrated community need for child care",
            "Financial capacity to operate expanded facility",
            "Site control or ownership",
            "All required permits obtainable"
        ]),
        "required_documents": json.dumps([
            "Detailed project budget and timeline",
            "Site plans and architectural drawings",
            "Proof of site control or ownership",
            "Community needs assessment",
            "Financial statements (last 2 years)",
            "Business plan for expanded operations",
            "Letters of support from community partners",
            "Environmental and zoning documentation"
        ]),
        "application_url": "https://www.oregon.gov/biz/programs/child_care_infrastructure/pages/default.aspx",
        "contact_email": "childcare.infrastructure@biz.oregon.gov",
        "contact_phone": "503-986-0123",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Infants and toddlers (0-3)",
            "Preschool children (3-5)",
            "School-age children",
            "Rural communities",
            "Child care deserts"
        ]),
        "funding_priorities": json.dumps([
            "Projects in child care deserts",
            "Infant and toddler care expansion",
            "Rural and underserved communities",
            "Culturally specific providers",
            "Projects serving low-income families",
            "Energy-efficient and sustainable design"
        ]),
        "status": "active"
    },
    {
        "source_name": "Oregon SPARK",
        "source_url": "https://oregonspark.org/early-educators/grants/",
        "source_type": "state",
        "title": "Quality Improvement Grants - Spring 2026",
        "description": "Oregon SPARK Quality Improvement Grants support child care providers in achieving or maintaining higher quality ratings. Funds can be used for classroom materials, curriculum development, facility improvements, technology, outdoor learning spaces, and staff training. Grants are available to programs at all quality levels seeking to improve.",
        "amount_min": 5000.0,
        "amount_max": 25000.0,
        "deadline": datetime.now() + timedelta(days=30),
        "application_opens": datetime.now() - timedelta(days=3),
        "eligibility_criteria": json.dumps([
            "Licensed child care provider in Oregon",
            "Enrolled or willing to enroll in Oregon SPARK",
            "Serve children ages 0-5",
            "Committed to quality improvement",
            "Complete quality improvement plan",
            "Participate in SPARK coaching and assessment"
        ]),
        "required_documents": json.dumps([
            "Current Oregon license",
            "SPARK enrollment confirmation",
            "Quality improvement plan",
            "Budget for proposed improvements",
            "Current quality rating (if applicable)",
            "Photos of areas to be improved"
        ]),
        "application_url": "https://oregonspark.org/early-educators/grants/",
        "contact_email": "grants@oregonspark.org",
        "contact_phone": "503-415-4702",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Infants and toddlers",
            "Preschool children",
            "Children with special needs",
            "Dual language learners"
        ]),
        "funding_priorities": json.dumps([
            "Learning environment improvements",
            "Evidence-based curriculum adoption",
            "Inclusive practices for children with disabilities",
            "Culturally responsive materials",
            "Outdoor learning environments",
            "STEM and literacy materials"
        ]),
        "status": "active"
    },
    {
        "source_name": "Collins Foundation",
        "source_url": "https://collinsfoundation.org",
        "source_type": "foundation",
        "title": "Early Childhood Education Initiative - 2026",
        "description": "The Collins Foundation supports early childhood education programs in Oregon that demonstrate commitment to racial equity and inclusion. Funding priorities include programs serving communities of color, rural areas, and families facing economic hardship. Multi-year grants available for comprehensive program development.",
        "amount_min": 25000.0,
        "amount_max": 100000.0,
        "deadline": datetime.now() + timedelta(days=75),
        "application_opens": datetime.now() - timedelta(days=21),
        "eligibility_criteria": json.dumps([
            "Nonprofit organization or fiscal sponsor",
            "Serving Oregon communities",
            "Focus on children ages 0-5",
            "Demonstrated commitment to racial equity",
            "Strong community partnerships",
            "Sustainable program model",
            "Clear outcomes and evaluation plan"
        ]),
        "required_documents": json.dumps([
            "501(c)(3) determination letter",
            "Program narrative (5-10 pages)",
            "Detailed budget and budget narrative",
            "Board of Directors list",
            "Most recent financial statements",
            "Letters of support (minimum 3)",
            "Equity statement and action plan",
            "Evaluation and sustainability plan"
        ]),
        "application_url": "https://collinsfoundation.org/apply",
        "contact_email": "info@collinsfoundation.org",
        "contact_phone": "503-227-7171",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Communities of color",
            "Low-income families",
            "Rural communities",
            "Immigrant and refugee families",
            "Families experiencing homelessness"
        ]),
        "funding_priorities": json.dumps([
            "Racial equity and inclusion",
            "Culturally specific programming",
            "Community-based approaches",
            "Family engagement and support",
            "Staff diversity and training",
            "Trauma-informed practices",
            "Two-generation approaches"
        ]),
        "status": "active"
    },
    {
        "source_name": "Ford Family Foundation",
        "source_url": "https://tfff.org/grants",
        "source_type": "foundation",
        "title": "Rural Child Care Capacity Building - 2026",
        "description": "Supporting rural Oregon child care providers to expand capacity, improve quality, and increase sustainability. The Ford Family Foundation recognizes the unique challenges of rural child care and provides flexible funding for staffing, facilities, equipment, transportation, and program development. Technical assistance included.",
        "amount_min": 15000.0,
        "amount_max": 75000.0,
        "deadline": datetime.now() + timedelta(days=50),
        "application_opens": datetime.now() - timedelta(days=10),
        "eligibility_criteria": json.dumps([
            "Located in rural Oregon (population <30,000)",
            "Licensed or license-ready child care provider",
            "Serve children ages 0-5",
            "Demonstrated community need",
            "Financially stable or path to stability",
            "Commitment to quality improvement",
            "Willingness to participate in technical assistance"
        ]),
        "required_documents": json.dumps([
            "Current license or license application",
            "Community needs assessment",
            "Program budget and financial statements",
            "Capacity expansion or quality improvement plan",
            "Letters of community support",
            "Staff qualifications",
            "Sustainability plan"
        ]),
        "application_url": "https://tfff.org/grants/apply",
        "contact_email": "grants@tfff.org",
        "contact_phone": "541-957-5574",
        "geographic_restriction": "rural",
        "target_populations": json.dumps([
            "Rural families",
            "Working families",
            "Low-income families",
            "Agricultural workers",
            "Families with limited child care options"
        ]),
        "funding_priorities": json.dumps([
            "Increasing child care slots in rural areas",
            "Infant and toddler care",
            "Non-traditional hours care",
            "Transportation solutions",
            "Staff recruitment and retention",
            "Business sustainability",
            "Community partnerships"
        ]),
        "status": "active"
    },
    {
        "source_name": "Meyer Memorial Trust",
        "source_url": "https://mmt.org/apply",
        "source_type": "foundation",
        "title": "Equity and Inclusion in Early Learning - 2026",
        "description": "Meyer Memorial Trust supports innovative approaches to advancing equity and inclusion in Oregon early learning settings. Funding available for programs that center the voices and needs of historically marginalized communities, including Black, Indigenous, Latino/a/x, Asian, Pacific Islander, immigrant, refugee, and LGBTQ+ families.",
        "amount_min": 30000.0,
        "amount_max": 150000.0,
        "deadline": datetime.now() + timedelta(days=90),
        "application_opens": datetime.now() - timedelta(days=5),
        "eligibility_criteria": json.dumps([
            "Oregon-based nonprofit or tribal organization",
            "Early learning or child care focus",
            "Community-led or culturally specific program",
            "Clear equity goals and outcomes",
            "Meaningful community engagement",
            "Leadership from impacted communities",
            "Collaboration and partnership approach"
        ]),
        "required_documents": json.dumps([
            "Organizational background and mission",
            "Program description and theory of change",
            "Equity framework and implementation plan",
            "Community engagement strategy",
            "Detailed budget and budget narrative",
            "Outcomes and evaluation approach",
            "Letters of partnership/support",
            "Board and leadership demographics"
        ]),
        "application_url": "https://mmt.org/apply",
        "contact_email": "mmt@mmt.org",
        "contact_phone": "503-228-5512",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Black, Indigenous, and people of color",
            "Immigrant and refugee families",
            "LGBTQ+ families",
            "Families with disabilities",
            "Low-income families",
            "Tribal communities"
        ]),
        "funding_priorities": json.dumps([
            "Community-led and culturally specific programs",
            "Anti-racist and inclusive practices",
            "Leadership development from impacted communities",
            "Systemic change and advocacy",
            "Healing-centered approaches",
            "Parent and family leadership",
            "Cross-sector collaboration"
        ]),
        "status": "active"
    },
    {
        "source_name": "Oregon Community Foundation",
        "source_url": "https://oregoncf.org/grants-and-scholarships",
        "source_type": "foundation",
        "title": "Early Childhood Development Fund - 2026",
        "description": "Supporting Oregon organizations that provide high-quality early learning experiences for children birth to age 5. Funding available for program operations, capacity building, and special projects. Preference for programs demonstrating innovation, collaboration, and measurable outcomes for children and families.",
        "amount_min": 10000.0,
        "amount_max": 50000.0,
        "deadline": datetime.now() + timedelta(days=40),
        "application_opens": datetime.now() - timedelta(days=7),
        "eligibility_criteria": json.dumps([
            "501(c)(3) nonprofit in Oregon",
            "Early learning or child care programming",
            "Serve children ages 0-5",
            "Track record of program quality",
            "Strong organizational capacity",
            "Clear program outcomes",
            "Financial stability"
        ]),
        "required_documents": json.dumps([
            "Letter of intent (2 pages)",
            "Full proposal (if invited)",
            "Program budget",
            "Organizational budget",
            "501(c)(3) letter",
            "Board list and demographics",
            "Financial statements",
            "Program evaluation data"
        ]),
        "application_url": "https://oregoncf.org/grants-and-scholarships/apply",
        "contact_email": "grants@oregoncf.org",
        "contact_phone": "503-802-2335",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Children ages 0-5",
            "Low to moderate income families",
            "Underserved communities",
            "Children at risk of poor outcomes"
        ]),
        "funding_priorities": json.dumps([
            "Evidence-based programming",
            "School readiness outcomes",
            "Family engagement and support",
            "Quality improvement",
            "Collaborative approaches",
            "Innovation and best practices",
            "Sustainability and impact"
        ]),
        "status": "active"
    },
    {
        "source_name": "PNC Foundation",
        "source_url": "https://pnc.com/about-pnc/corporate-responsibility",
        "source_type": "private",
        "title": "Grow Up Great - Oregon 2026",
        "description": "PNC's Grow Up Great program supports high-quality early childhood education with a focus on preparing children for success in school and life. Grants available for curriculum development, teacher training, educational materials, STEM programming, and family engagement. Multi-year funding possible for demonstrated impact.",
        "amount_min": 5000.0,
        "amount_max": 35000.0,
        "deadline": datetime.now() + timedelta(days=55),
        "application_opens": datetime.now() - timedelta(days=12),
        "eligibility_criteria": json.dumps([
            "Nonprofit organization serving Oregon",
            "Focus on children ages 3-5",
            "Evidence-based curriculum or approach",
            "Qualified teaching staff",
            "Parent and family engagement component",
            "Outcomes measurement plan",
            "Sustainable program model"
        ]),
        "required_documents": json.dumps([
            "Program description and goals",
            "Budget and budget narrative",
            "Curriculum overview",
            "Staff qualifications",
            "Outcomes and evaluation plan",
            "Family engagement strategy",
            "Letters of support",
            "Photos or videos of program (optional)"
        ]),
        "application_url": "https://pnc.com/about-pnc/corporate-responsibility/philanthropic-investments/grow-up-great.html",
        "contact_email": "growupgreat@pnc.com",
        "contact_phone": "877-762-2968",
        "geographic_restriction": "statewide",
        "target_populations": json.dumps([
            "Preschool children (ages 3-5)",
            "Low to moderate income families",
            "Children in underserved communities",
            "Children at risk of school failure"
        ]),
        "funding_priorities": json.dumps([
            "School readiness skills",
            "STEM and early literacy",
            "Social-emotional development",
            "Teacher professional development",
            "Family engagement in learning",
            "Technology and innovation",
            "Measurable outcomes"
        ]),
        "status": "active"
    }
]

def seed_grants():
    db = SessionLocal()
    try:
        # Check if grants already exist
        existing = db.query(Grant).count()
        if existing > 0:
            print(f"Database already has {existing} grants.")
            response = input("Do you want to delete existing grants and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("Seeding cancelled.")
                return

            # Delete existing grants
            db.query(Grant).delete()
            db.commit()
            print("Existing grants deleted.")

        # Add sample grants
        for grant_data in sample_grants:
            grant = Grant(**grant_data)
            db.add(grant)

        db.commit()
        print(f"\n✅ Successfully added {len(sample_grants)} sample Oregon grants!")
        print("\nGrants added:")
        for i, grant in enumerate(sample_grants, 1):
            print(f"{i}. {grant['title']}")
            print(f"   Source: {grant['source_name']}")
            print(f"   Amount: ${grant['amount_min']:,.0f} - ${grant['amount_max']:,.0f}")
            print(f"   Deadline: {grant['deadline'].strftime('%B %d, %Y')}")
            print()

        print("🎉 Database seeded successfully! You can now test grant browsing and applications.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_grants()
