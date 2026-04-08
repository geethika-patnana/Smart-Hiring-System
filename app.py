"""
Smart-Hiring: Explainable NLP Pipeline for Resume Matching
Academic Research Implementation

Features:
- Resume parsing and information extraction
- Semantic job matching using transformers
- Explainable AI with score breakdowns
- Interactive candidate ranking
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
import time
import tempfile

from src.resume_parser import ResumeParser
from src.job_matcher import JobMatcher
from src.explainability import (
    create_score_breakdown_chart,
    create_radar_chart,
    create_skills_overlap_chart,
    create_ranking_chart,
    create_comparison_heatmap,
    generate_explanation_text,
    get_matching_keywords
)

from src.utils.styles import apply_custom_styles
from src.utils.streamlit_components import (
    ContentSections, DataTable, MetricCard, 
    InfoBox, create_sidebar_navigation, display_feature_card
)

import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Smart-Hiring System",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

@st.cache_resource
def load_parser():
    """Load resume parser"""
    return ResumeParser()

@st.cache_resource
def load_matcher():
    """Load job matcher with transformer model"""
    return JobMatcher()

def load_parsed_resumes():
    """Load parsed resumes from JSON (no caching to reflect current state)"""
    parsed_path = DATA_DIR / "processed" / "parsed_resumes.json"
    if parsed_path.exists():
        with open(parsed_path, 'r') as f:
            return json.load(f)
    return []

def load_parsing_errors():
    """Load parsing errors if any"""
    errors_path = DATA_DIR / "processed" / "parsing_errors.json"
    if errors_path.exists():
        with open(errors_path, 'r') as f:
            return json.load(f)
    return []

def count_resumes_in_folder():
    """Count actual PDF files in resume folder"""
    resumes_dir = DATA_DIR / "raw" / "resumes"
    if resumes_dir.exists():
        return len(list(resumes_dir.glob("*.pdf")))
    return 0

def rescan_resumes():
    """Re-parse all resumes from folder"""
    parser = load_parser()
    resumes_dir = DATA_DIR / "raw" / "resumes"
    parsed_resumes, errors = parser.parse_all_resumes(resumes_dir)
    output_path = DATA_DIR / "processed" / "parsed_resumes.json"
    parser.save_parsed_data(parsed_resumes, output_path, errors)
    return len(parsed_resumes), len(errors)

@st.cache_data
def load_job_descriptions():
    """Load job descriptions"""
    jobs_path = DATA_DIR / "raw" / "jobs" / "job_descriptions.json"
    if jobs_path.exists():
        with open(jobs_path, 'r') as f:
            return json.load(f)
    return []

def check_login():
    """Check if user is logged in"""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    return st.session_state['logged_in']

def login_page():
    """Display login page"""
    apply_custom_styles()
    
    st.markdown(
        '<h1 class="styled-title">Smart-Hiring System</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">Please login to continue</p>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        st.markdown("")
        
        if st.button("Login", type="primary", use_container_width=True):
            # Hardcoded credentials
            if username == "admin" and password == "admin123":
                st.session_state['logged_in'] = True
                st.success("Login successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("---")
        # st.info(" **Demo Credentials:**\n\nUsername: `admin`\n\nPassword: `admin123`")

def main():
    # Check login status
    if not check_login():
        login_page()
        return
    
    apply_custom_styles()
    
    st.markdown(
        '<h1 class="styled-title">Smart-Hiring System</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">Explainable NLP Pipeline for Resume Matching</p>',
        unsafe_allow_html=True
    )
    
    pages = [
        "Home",
        "Parse Resume",
        "Job Matching",
        "Candidate Ranking",
        "Explainability",
        "About Project",
        "Logout"
    ]
    
    current_page = create_sidebar_navigation(pages)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Settings")
    
    # Count actual resumes in folder
    folder_count = count_resumes_in_folder()
    
    # Load data (fresh, no cache)
    parsed_resumes = load_parsed_resumes()
    parsing_errors = load_parsing_errors()
    jobs = load_job_descriptions()
    
    # Check if folder and JSON are in sync
    json_count = len(parsed_resumes)
    is_synced = folder_count == json_count
    
    st.sidebar.info(f"**Data Status**\n\n"
                   f"Resumes in folder: {folder_count}\n\n"
                   f"Parsed in JSON: {json_count}\n\n"
                   f"Jobs: {len(jobs)}")
    
    if not is_synced:
        st.sidebar.warning(f"Out of sync!\n\nFolder has {folder_count} PDFs but JSON has {json_count} entries.")
        if st.sidebar.button("Re-scan Resumes", use_container_width=True):
            with st.spinner("Re-parsing resumes..."):
                success_count, error_count = rescan_resumes()
            st.sidebar.success(f"Parsed {success_count} resumes!")
            if error_count > 0:
                st.sidebar.error(f"{error_count} errors")
            time.sleep(1)
            st.rerun()
    
    if parsing_errors:
        st.sidebar.warning(f"{len(parsing_errors)} parsing errors")
    
    st.sidebar.markdown("---")
    
    if current_page == "Home":
        st.markdown("### Welcome to Smart-Hiring System")
        
        # col1, col2, col3, col4 = st.columns(4)
        
        # with col1:
        #     MetricCard.display("Parsed Resumes", str(len(parsed_resumes)), icon="📄")
        # with col2:
        #     MetricCard.display("Job Openings", str(len(jobs)), icon="💼")
        # with col3:
        #     MetricCard.display("NLP Model", "MiniLM-L6-v2", icon="🤖")
        # with col4:
        #     MetricCard.display("Match Engine", "Active", icon="✅")
        
        st.markdown("""
        ### About Smart-Hiring
        
        Smart-Hiring is an **end-to-end NLP pipeline** that automates resume screening and candidate matching.
        The system combines:
        
        - **Resume Parsing**: Extract structured information from PDF resumes
        - **Semantic Matching**: Use transformer embeddings for intelligent matching
        - **Explainability**: Transparent scoring with detailed breakdowns
        - **Ranking**: Data-driven candidate prioritization
        
        ###  How It Works
        
        1. **Parse Resumes** → System extracts name, skills, education, experience from folder
        2. **Define Job** → Specify requirements and preferred qualifications
        3. **Match & Rank** → AI computes semantic similarity scores
        4. **Explain Results** → View detailed rationale for each match
        """)
        
        st.markdown("---")
    
    elif current_page == "Parse Resume":
        st.header("Resume Parser")
        
        st.markdown("""
        This page shows all parsed resumes from the `data/raw/resumes/` folder.
        The system automatically extracts:
        - **Name** (using Named Entity Recognition)
        - **Contact Info** (email, phone, address)
        - **Skills** (fuzzy matching against skills lexicon)
        - **Education** (highest degree)
        - **Experience** (years of experience)
        """)
        
        st.markdown("---")
        
        # Show folder status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("PDFs in Folder", folder_count)
        with col2:
            st.metric("Parsed in JSON", json_count)
        with col3:
            if is_synced:
                st.metric("Status", "Synced")
            else:
                st.metric("Status", "Out of Sync")
        
        st.markdown("---")
        
        # Re-parse button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Re-scan & Parse All Resumes", type="primary", use_container_width=True):
                with st.spinner("Parsing all resumes from folder..."):
                    success_count, error_count = rescan_resumes()
                
                if success_count > 0:
                    InfoBox.success(f"Successfully parsed {success_count} resumes!")
                if error_count > 0:
                    InfoBox.error(f"Failed to parse {error_count} resumes (see errors below)")
                
                time.sleep(1)
                st.rerun()
        
        st.markdown("---")
        
        # Show parsed resumes
        if parsed_resumes:
            st.markdown(f"### Parsed Resumes ({len(parsed_resumes)} total)")
            
            for idx, resume in enumerate(parsed_resumes, 1):
                with st.expander(f"#{idx} - {resume['name']} ({resume['filename']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Personal Information**")
                        st.write(f"**Name:** {resume['name']}")
                        st.write(f"**Email:** {resume['email'] or 'Not found'}")
                        st.write(f"**Phone:** {resume['phone'] or 'Not found'}")
                        st.write(f"**Location:** {resume['address'] or 'Not found'}")
                        
                        st.markdown("**Education & Experience**")
                        st.write(f"**Education:** {resume['education']}")
                        st.write(f"**Experience:** {resume['experience_years']} years")
                    
                    with col2:
                        st.markdown("**Skills Extracted**")
                        if resume['skills']:
                            skills_df = pd.DataFrame({
                                'Skill': resume['skills']
                            })
                            st.dataframe(skills_df, use_container_width=True, height=250)
                        else:
                            st.info("No skills found")
        else:
            InfoBox.warning("No parsed resumes found. Click 'Re-scan & Parse All Resumes' to parse PDFs from the folder.")
        
        # Show parsing errors if any
        if parsing_errors:
            st.markdown("---")
            st.markdown("### Parsing Errors")
            with st.expander(f"View {len(parsing_errors)} failed resumes"):
                for error in parsing_errors:
                    st.error(f"**{error['file']}**: {error['error']}")
    
    elif current_page == "Job Matching":
        st.header("Job Matching")
        
        if not parsed_resumes:
            InfoBox.warning("No parsed resumes found. Please parse resumes first or run: `python src/resume_parser.py`")
            return
        
        st.markdown("Select a job description to match against all candidates")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Job Description")
            
            if jobs:
                job_titles = [job['title'] for job in jobs]
                selected_job_idx = st.selectbox(
                    "Select Job",
                    range(len(jobs)),
                    format_func=lambda x: job_titles[x]
                )
                selected_job = jobs[selected_job_idx]
                
                st.markdown(f"**Company:** {selected_job['company']}")
                st.markdown(f"**Location:** {selected_job['location']}")
                st.markdown(f"**Experience Required:** {selected_job['experience_required']} years")
                st.markdown(f"**Education Required:** {selected_job['education_required']}")
                
                st.markdown("**Required Skills:**")
                st.write(", ".join(selected_job['required_skills']))
                
                if selected_job.get('preferred_skills'):
                    st.markdown("**Preferred Skills:**")
                    st.write(", ".join(selected_job['preferred_skills']))
            else:
                st.warning("No job descriptions found")
                selected_job = None
        
        with col2:
            st.subheader("👥 Candidates")
            st.metric("Total Candidates", len(parsed_resumes))
            
            if parsed_resumes:
                candidate_names = [r['name'] for r in parsed_resumes]
                st.write("**Available Candidates:**")
                for name in candidate_names:
                    st.write(f"- {name}")
        
        st.markdown("---")
        
        if selected_job and st.button("Run Matching", type="primary", use_container_width=True):
            with st.spinner("Computing semantic similarity..."):
                # Clear old results from session state
                if 'matches' in st.session_state:
                    del st.session_state['matches']
                if 'selected_job' in st.session_state:
                    del st.session_state['selected_job']
                
                # Run fresh matching
                matcher = load_matcher()
                matches = matcher.rank_candidates(parsed_resumes, selected_job)
                
                # Store new results in session state
                st.session_state['matches'] = matches
                st.session_state['selected_job'] = selected_job
            
            InfoBox.success(f"Matching completed! Ranked {len(matches)} candidates.")
            
            st.markdown("### Top Candidates")
            
            for idx, match in enumerate(matches[:5], 1):
                with st.expander(f"#{idx} - {match['candidate_name']} - Score: {match['overall_score']}%"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Contact:**")
                        st.write(f"Email: {match['candidate_data']['email']}")
                        st.write(f"Phone: {match['candidate_data']['phone']}")
                        st.write(f"Education: {match['candidate_data']['education']}")
                        st.write(f"Experience: {match['candidate_data']['experience_years']} years")
                    
                    with col2:
                        st.markdown("**Component Scores:**")
                        for component, score in match['component_scores'].items():
                            st.progress(score / 100, text=f"{component.title()}: {score}%")
            
            st.markdown("---")
            st.info("Go to 'Candidate Ranking' page to see detailed comparisons")
    
    elif current_page == "Candidate Ranking":
        st.header("Candidate Ranking & Comparison")
        
        if 'matches' not in st.session_state:
            InfoBox.warning("No matching results found. Please run job matching first.")
            return
        
        matches = st.session_state['matches']
        selected_job = st.session_state['selected_job']
        
        st.markdown(f"### Job: {selected_job['title']}")
        st.markdown(f"**Total Candidates Evaluated:** {len(matches)}")
        
        st.markdown("---")
        
        # Ranking chart
        st.markdown("### Candidate Rankings")
        ranking_chart = create_ranking_chart(matches, top_n=min(10, len(matches)))
        st.plotly_chart(ranking_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Comparison heatmap
        st.markdown("### Comparison Heatmap")
        heatmap = create_comparison_heatmap(matches)
        if heatmap:
            st.plotly_chart(heatmap, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed table
        st.markdown("### Detailed Results")
        
        results_data = []
        for match in matches:
            results_data.append({
                'Rank': matches.index(match) + 1,
                'Name': match['candidate_name'],
                'Overall Score': f"{match['overall_score']}%",
                'Skills': f"{match['component_scores']['skills']}%",
                'Experience': f"{match['component_scores']['experience']}%",
                'Education': f"{match['component_scores']['education']}%",
                'Location': f"{match['component_scores']['location']}%",
                'Email': match['candidate_data']['email']
            })
        
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, height=400)
        
        st.markdown("---")
        
        # Export results
        st.markdown("### Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Download as JSON",
                data=json.dumps(matches, indent=2),
                file_name=f"{selected_job['title'].replace(' ', '_')}_results.json",
                mime="application/json"
            )
        
        with col2:
            st.download_button(
                label="Download as CSV",
                data=results_df.to_csv(index=False),
                file_name=f"{selected_job['title'].replace(' ', '_')}_results.csv",
                mime="text/csv"
            )
    
    elif current_page == "Explainability":
        st.header("🔍 Explainability Dashboard")
        
        if 'matches' not in st.session_state:
            st.warning("No matching results found.")
            
            st.markdown("""
            ### How to Use Explainability
            
            To view explainability insights, you need to:
            
            1. **Go to "Job Matching" page**
            2. **Select a job description** from the dropdown
            3. **Click "Run Matching"** button
            4. **Come back to this page** to see detailed explanations
            
            ---
            
            ###  What You'll See Here
            
            Once you run matching, this page will show:
            
            - **Overall Score & Rank** for each candidate
            - **Score Breakdown** (Skills, Experience, Education, Location)
            - **Radar Chart** showing candidate profile
            - **Skills Analysis** (Matched, Missing, Additional skills)
            - **Detailed Explanation** with recommendations
            
            """)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Go to Job Matching", type="primary", use_container_width=True):
                    st.info("Use the sidebar to navigate to 'Job Matching' page")
            
            return
        
        matches = st.session_state['matches']
        selected_job = st.session_state['selected_job']
        
        st.markdown(f"### Job: {selected_job['title']}")
        st.markdown("Understand why candidates were ranked the way they were")
        
        st.markdown("---")
        
        # Select candidate to explain
        candidate_names = [m['candidate_name'] for m in matches]
        selected_candidate_name = st.selectbox(
            "Select Candidate to Explain",
            candidate_names
        )
        
        selected_match = next(m for m in matches if m['candidate_name'] == selected_candidate_name)
        
        st.markdown("---")
        
        # Overall assessment
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{selected_match['overall_score']}%")
        with col2:
            rank = matches.index(selected_match) + 1
            st.metric("Rank", f"#{rank} of {len(matches)}")
        with col3:
            if selected_match['overall_score'] >= 80:
                st.metric("Assessment", "Excellent Match", delta="Recommended")
            elif selected_match['overall_score'] >= 65:
                st.metric("Assessment", "Good Match", delta="Consider")
            else:
                st.metric("Assessment", "Moderate Match", delta="Review")
        
        st.markdown("---")
        
        # Score breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Score Breakdown")
            weights = {'skills': 0.50, 'experience': 0.20, 'education': 0.15, 'location': 0.15}
            breakdown_chart = create_score_breakdown_chart(selected_match['component_scores'], weights)
            st.plotly_chart(breakdown_chart, use_container_width=True)
        
        with col2:
            st.markdown("### Profile Radar")
            radar_chart = create_radar_chart(selected_match['component_scores'])
            st.plotly_chart(radar_chart, use_container_width=True)
        
        st.markdown("---")
        
        # Skills overlap
        st.markdown("### Skills Analysis")
        
        candidate_skills = selected_match['candidate_data']['skills']
        job_skills = selected_job['required_skills'] + selected_job.get('preferred_skills', [])
        
        summary, skills_data = create_skills_overlap_chart(candidate_skills, job_skills)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Matched Skills", summary['matched'], delta="")
        with col2:
            st.metric("Missing Skills", summary['missing'], delta="", delta_color="inverse")
        with col3:
            st.metric("Additional Skills", summary['additional'], delta="")
        with col4:
            st.metric("Match %", f"{summary['match_percentage']}%")
        
        st.markdown("**Skill Details:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Matched Skills**")
            matched = [s for s, c in zip(skills_data['skills'], skills_data['categories']) if c == 'Matched']
            if matched:
                for skill in matched:
                    st.write(f"- {skill}")
            else:
                st.info("None")
        
        with col2:
            st.markdown("**Missing Skills**")
            missing = [s for s, c in zip(skills_data['skills'], skills_data['categories']) if c == 'Missing']
            if missing:
                for skill in missing[:5]:
                    st.write(f"- {skill}")
            else:
                st.info("None")
        
        with col3:
            st.markdown("**Additional Skills**")
            additional = [s for s, c in zip(skills_data['skills'], skills_data['categories']) if c == 'Additional']
            if additional:
                for skill in additional[:5]:
                    st.write(f"- {skill}")
            else:
                st.info("None")
        
        st.markdown("---")
        
        # Detailed explanation
        st.markdown("### Detailed Explanation")
        explanation = generate_explanation_text(selected_match, selected_job)
        st.markdown(explanation)
    
    elif current_page == "Logout":
        st.header("Logout")
        
        st.markdown("### Are you sure you want to logout?")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("Yes, Logout", type="primary", use_container_width=True):
                st.session_state['logged_in'] = False
                # Reset to home page
                st.session_state['page'] = "Home"
                # Clear all session state
                if 'matches' in st.session_state:
                    del st.session_state['matches']
                if 'selected_job' in st.session_state:
                    del st.session_state['selected_job']
                st.success("Logged out successfully!")
                time.sleep(0.5)
                st.rerun()
            
            if st.button("Cancel", use_container_width=True):
                st.info("Logout cancelled")
    
    elif current_page == "About Project":
        st.header("About Smart-Hiring Project")
        
        st.markdown("""
        ### Research Paper
        
        **Title:** SMART-HIRING: AN EXPLAINABLE END-TO-END PIPELINE FOR RESUME MATCHING
        
        **Abstract:**
        
        Hiring processes often involve the manual screening of hundreds of resumes for each job, 
        a task that is time and effort consuming, error-prone, and subject to human bias.
        
        This project presents Smart-Hiring, an end-to-end Natural Language Processing (NLP) pipeline 
        designed to automatically extract structured information from unstructured resumes and to 
        semantically match candidates with job descriptions.
        
        ### 🔬 Methodology
        
        **Stage 1: Resume Information Extraction**
        - PDF text extraction using `pdfplumber`
        - Text normalization and cleaning
        - Named Entity Recognition for personal information
        - Fuzzy matching for skills extraction (against LinkedIn skills lexicon)
        - Education level detection
        - Experience years calculation from date parsing
        
        **Stage 2: Semantic Job Matching**
        - Sentence embeddings using `all-MiniLM-L6-v2` transformer model
        - Cosine similarity computation between resume and job skills
        - Multi-dimensional scoring:
          - Skills similarity (50% weight)
          - Experience match (20% weight)
          - Education match (15% weight)
          - Location compatibility (15% weight)
        - Weighted aggregation for overall match score
        
        **Stage 3: Explainability Layer**
        - Component score breakdowns
        - Skills overlap visualization
        - Matching keyword highlighting
        - Human-readable explanations
        
        ### 🛠️ Technical Stack
        
        - **NLP**: sentence-transformers, spaCy
        - **PDF Processing**: pdfplumber
        - **Fuzzy Matching**: fuzzywuzzy
        - **Web Interface**: Streamlit
        - **Visualization**: Plotly
        - **Data Processing**: pandas, numpy
        
        ### 📊 Key Features
        
        ✅ Automated resume parsing from PDFs  
        ✅ Semantic similarity using transformer embeddings  
        ✅ Multi-criteria weighted scoring  
        ✅ Explainable AI with transparent decisions  
        ✅ Interactive web dashboard  
        ✅ Candidate ranking and comparison  
        ✅ Export results (JSON/CSV)
        
        ### 🎯 Use Cases
        
        - **HR Departments**: Automate initial resume screening
        - **Recruitment Agencies**: Scale candidate evaluation
        - **Job Portals**: Intelligent candidate-job matching
        - **Research**: Study bias in hiring algorithms
        
        ### 📚 Dataset
        
        This implementation uses synthetic resumes generated for demonstration purposes.
        The system can be adapted to work with real-world resume datasets.
        
        """)
        
        st.markdown("---")
        
#         st.markdown("### � Getting Started")
        
#         with st.expander("📦 Installation"):
#             st.code("""
# # Install dependencies
# pip install -r requirements.txt

# # Download spaCy model
# python -m spacy download en_core_web_sm
#             """, language="bash")
        
#         with st.expander("🏃 Quick Start"):
#             st.code("""
# # 1. Generate synthetic data
# python src/generate_synthetic_data.py

# # 2. Parse resumes
# python src/resume_parser.py

# # 3. Run matching
# python src/job_matcher.py

# # 4. Launch web app
# streamlit run app.py
#             """, language="bash")
        
#         with st.expander("📖 Documentation"):
#             st.markdown("""
#             **Key Modules:**
            
#             - `resume_parser.py`: Resume information extraction
#             - `job_matcher.py`: Semantic matching engine
#             - `explainability.py`: Visualization and explanations
#             - `generate_synthetic_data.py`: Sample data generation
            
#             **Configuration:**
            
#             - Skills lexicon: `data/skills_lexicon.json`
#             - Education levels: `data/education_levels.json`
#             - Matching weights: Configurable in `job_matcher.py`
#             """)

if __name__ == "__main__":
    main()
