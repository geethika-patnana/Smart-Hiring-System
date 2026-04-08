"""
Generate Synthetic Resumes and Job Descriptions
Creates realistic PDF resumes for testing the Smart-Hiring pipeline
"""

import json
import random
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Load skills lexicon
with open(DATA_DIR / "skills_lexicon.json", 'r') as f:
    SKILLS_DATA = json.load(f)

ALL_SKILLS = []
for category in SKILLS_DATA.values():
    ALL_SKILLS.extend(category)

CANDIDATE_PROFILES = [
    {
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0101",
        "address": "New York, NY",
        "education": "Master in Computer Science",
        "experience_years": 5,
        "skills": ["Python", "Machine Learning", "TensorFlow", "AWS", "Docker", "SQL", "Data Analysis"],
        "job_history": [
            {"title": "Senior Data Scientist", "company": "Tech Corp", "duration": "2021-Present"},
            {"title": "Data Scientist", "company": "Analytics Inc", "duration": "2019-2021"}
        ]
    },
    {
        "name": "Sarah Johnson",
        "email": "sarah.j@email.com",
        "phone": "+1-555-0102",
        "address": "San Francisco, CA",
        "education": "Bachelor in Software Engineering",
        "experience_years": 3,
        "skills": ["JavaScript", "React", "Node.js", "MongoDB", "REST API", "Git", "Agile"],
        "job_history": [
            {"title": "Full Stack Developer", "company": "WebDev Solutions", "duration": "2022-Present"},
            {"title": "Frontend Developer", "company": "StartupXYZ", "duration": "2021-2022"}
        ]
    },
    {
        "name": "Michael Chen",
        "email": "m.chen@email.com",
        "phone": "+1-555-0103",
        "address": "Seattle, WA",
        "education": "PhD in Artificial Intelligence",
        "experience_years": 8,
        "skills": ["Deep Learning", "PyTorch", "NLP", "Computer Vision", "Python", "Research", "Publications"],
        "job_history": [
            {"title": "AI Research Scientist", "company": "AI Labs", "duration": "2020-Present"},
            {"title": "ML Engineer", "company": "Innovation Tech", "duration": "2016-2020"}
        ]
    },
    {
        "name": "Emily Davis",
        "email": "emily.davis@email.com",
        "phone": "+1-555-0104",
        "address": "Boston, MA",
        "education": "Master in Data Science",
        "experience_years": 4,
        "skills": ["Python", "R", "Statistical Analysis", "Tableau", "SQL", "Big Data", "Spark"],
        "job_history": [
            {"title": "Data Analyst", "company": "Finance Corp", "duration": "2021-Present"},
            {"title": "Junior Analyst", "company": "Consulting Group", "duration": "2020-2021"}
        ]
    },
    {
        "name": "David Martinez",
        "email": "d.martinez@email.com",
        "phone": "+1-555-0105",
        "address": "Austin, TX",
        "education": "Bachelor in Computer Science",
        "experience_years": 6,
        "skills": ["Java", "Spring Boot", "Microservices", "Kubernetes", "AWS", "CI/CD", "Docker"],
        "job_history": [
            {"title": "Senior Backend Engineer", "company": "Cloud Services Inc", "duration": "2020-Present"},
            {"title": "Backend Developer", "company": "Enterprise Solutions", "duration": "2018-2020"}
        ]
    },
    {
        "name": "Lisa Anderson",
        "email": "lisa.a@email.com",
        "phone": "+1-555-0106",
        "address": "Chicago, IL",
        "education": "Master in Software Engineering",
        "experience_years": 7,
        "skills": ["Python", "Django", "PostgreSQL", "Redis", "REST API", "Testing", "Leadership"],
        "job_history": [
            {"title": "Tech Lead", "company": "Digital Platform", "duration": "2022-Present"},
            {"title": "Senior Developer", "company": "Web Services", "duration": "2019-2022"}
        ]
    },
    {
        "name": "Robert Taylor",
        "email": "r.taylor@email.com",
        "phone": "+1-555-0107",
        "address": "Denver, CO",
        "education": "Bachelor in Information Technology",
        "experience_years": 2,
        "skills": ["JavaScript", "Vue.js", "HTML", "CSS", "Git", "Responsive Design", "UI/UX"],
        "job_history": [
            {"title": "Frontend Developer", "company": "Creative Agency", "duration": "2023-Present"},
            {"title": "Junior Developer", "company": "Design Studio", "duration": "2022-2023"}
        ]
    },
    {
        "name": "Jennifer Wilson",
        "email": "j.wilson@email.com",
        "phone": "+1-555-0108",
        "address": "Portland, OR",
        "education": "Master in Business Analytics",
        "experience_years": 5,
        "skills": ["Data Visualization", "Power BI", "SQL", "Python", "Excel", "Business Intelligence", "Analytics"],
        "job_history": [
            {"title": "Business Analyst", "company": "Retail Corp", "duration": "2021-Present"},
            {"title": "Data Analyst", "company": "Marketing Agency", "duration": "2019-2021"}
        ]
    }
]

JOB_DESCRIPTIONS = [
    {
        "title": "Senior Machine Learning Engineer",
        "company": "AI Innovations Inc",
        "location": "San Francisco, CA",
        "experience_required": 5,
        "education_required": "Master",
        "description": "We are seeking an experienced ML Engineer to develop and deploy machine learning models at scale.",
        "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "AWS", "Docker", "Kubernetes"],
        "preferred_skills": ["Deep Learning", "NLP", "MLOps", "Spark"]
    },
    {
        "title": "Full Stack Developer",
        "company": "WebTech Solutions",
        "location": "Remote",
        "experience_required": 3,
        "education_required": "Bachelor",
        "description": "Join our team to build modern web applications using cutting-edge technologies.",
        "required_skills": ["JavaScript", "React", "Node.js", "MongoDB", "REST API", "Git"],
        "preferred_skills": ["TypeScript", "GraphQL", "Docker", "AWS"]
    },
    {
        "title": "Data Scientist",
        "company": "Analytics Pro",
        "location": "New York, NY",
        "experience_required": 4,
        "education_required": "Master",
        "description": "Looking for a Data Scientist to extract insights from complex datasets and build predictive models.",
        "required_skills": ["Python", "R", "Machine Learning", "SQL", "Statistical Analysis", "Data Visualization"],
        "preferred_skills": ["Big Data", "Spark", "Tableau", "Deep Learning"]
    }
]


def create_resume_pdf(candidate, output_path):
    """Generate a PDF resume for a candidate"""
    doc = SimpleDocTemplate(str(output_path), pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=6,
        alignment=1  # Center
    )
    
    # Section heading style
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=6,
        spaceBefore=12
    )
    
    # Name
    story.append(Paragraph(candidate['name'], title_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Contact Info
    contact_text = f"{candidate['email']} | {candidate['phone']} | {candidate['address']}"
    story.append(Paragraph(contact_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", section_style))
    story.append(Paragraph(candidate['education'], styles['Normal']))
    story.append(Spacer(1, 0.15*inch))
    
    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
    story.append(Paragraph(f"Total Experience: {candidate['experience_years']} years", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    for job in candidate['job_history']:
        job_text = f"<b>{job['title']}</b> - {job['company']} ({job['duration']})"
        story.append(Paragraph(job_text, styles['Normal']))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.15*inch))
    
    # Skills
    story.append(Paragraph("SKILLS", section_style))
    skills_text = ", ".join(candidate['skills'])
    story.append(Paragraph(skills_text, styles['Normal']))
    
    doc.build(story)
    print(f" Generated resume: {candidate['name']}")


def save_job_descriptions():
    """Save job descriptions as JSON"""
    jobs_dir = DATA_DIR / "raw" / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    
    with open(jobs_dir / "job_descriptions.json", 'w') as f:
        json.dump(JOB_DESCRIPTIONS, f, indent=2)
    
    print(f"\n Saved {len(JOB_DESCRIPTIONS)} job descriptions")


def main():
    """Generate all synthetic data"""
    print("="*60)
    print("GENERATING SYNTHETIC DATA")
    print("="*60)
    
    # Create directories
    resumes_dir = DATA_DIR / "raw" / "resumes"
    resumes_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate resumes
    print(f"\nGenerating {len(CANDIDATE_PROFILES)} resumes...")
    for candidate in CANDIDATE_PROFILES:
        filename = candidate['name'].replace(" ", "_") + ".pdf"
        output_path = resumes_dir / filename
        create_resume_pdf(candidate, output_path)
    
    # Save job descriptions
    save_job_descriptions()
    
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE!")
    print("="*60)
    print(f"Resumes: {resumes_dir}")
    print(f"Jobs: {DATA_DIR / 'raw' / 'jobs'}")


if __name__ == "__main__":
    main()
