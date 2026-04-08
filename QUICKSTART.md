# 🚀 Quick Start Guide - Smart-Hiring Project

Follow any one of the two methods to get started

Method 1: One-Command Setup

## ⚡ One-Command Setup

Please be in project directory i.e SMART HIRING Folder

Run python setup.py


This will automatically:
1. Install all dependencies
2. Download NLP models
3. Generate sample resumes
4. Parse resumes
5. Run job matching

Method 2: Manual Setup
## 📝 Manual Setup (Step by Step)

### 1. Install Dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm


### 2. Generate Sample Data


python src/generate_synthetic_data.py


This creates:
- 8 synthetic resume PDFs in `data/raw/resumes/`
- 3 job descriptions in `data/raw/jobs/`

### 3. Parse Resumes


python src/resume_parser.py


Extracts structured information from PDFs:
- Names, contact info
- Skills (fuzzy matched against lexicon)
- Education level
- Years of experience

Output: `data/processed/parsed_resumes.json`

### 4. Run Job Matching


python src/job_matcher.py


Matches candidates to jobs using:
- Semantic similarity (transformer embeddings)
- Weighted scoring across multiple criteria
- Explainable results

Output: `results/matches/*.json`

### 5. Launch Web Application


streamlit run app.py

Opens interactive dashboard at `http://localhost:8501`

## 🎯 Using the Web Interface

### Home Page
- Overview of system capabilities
- Quick start guide

### Parse Resume
- Upload PDF resumes
- View extracted information
- Export parsed data

### Job Matching
- Select job description
- Run semantic matching
- View top candidates

### Candidate Ranking
- Compare all candidates
- Interactive visualizations
- Export results (CSV/JSON)

### Explainability
- Select candidate to explain
- View score breakdowns
- Skills overlap analysis
- Detailed rationale

## 📊 Understanding the Results

### Match Score Components

1. **Skills (50% weight)**
   - Semantic similarity between candidate and job skills
   - Uses transformer embeddings (all-MiniLM-L6-v2)

2. **Experience (20% weight)**
   - Years of experience vs. required
   - 100% if meets or exceeds requirement

3. **Education (15% weight)**
   - Highest degree vs. required
   - PhD > Master/Engineer > Bachelor > Associate

4. **Location (15% weight)**
   - Geographic compatibility
   - Remote jobs match all candidates

### Score Interpretation

- **80-100%**: Excellent match - Highly recommended
- **65-79%**: Good match - Recommended for consideration
- **50-64%**: Moderate match - May require evaluation
- **<50%**: Weak match - Not recommended

## 🔧 Customization

### Modify Skills Lexicon

Edit `data/skills_lexicon.json` to add/remove skills:

```json
{
  "programming_languages": ["Python", "Java", "..."],
  "frameworks": ["React", "Django", "..."]
}
```

### Adjust Matching Weights

In `src/job_matcher.py`, modify:

```python
self.weights = {
    'skills': 0.50,      # Adjust these values
    'experience': 0.20,
    'education': 0.15,
    'location': 0.15
}
```

### Add Custom Job Descriptions

Edit `data/raw/jobs/job_descriptions.json`:

```json
{
  "title": "Your Job Title",
  "company": "Company Name",
  "location": "Location",
  "experience_required": 3,
  "education_required": "Bachelor",
  "required_skills": ["Skill1", "Skill2"],
  "preferred_skills": ["Skill3", "Skill4"]
}
```

## 🐛 Troubleshooting

### spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

### Transformer Model Download Issues

The first run will download `all-MiniLM-L6-v2` (~90MB). Ensure internet connection.

### PDF Parsing Errors

- Ensure PDFs are text-based (not scanned images)
- For scanned PDFs, OCR would be needed (not included in MVP)

### Import Errors

```bash
pip install -r requirements.txt --upgrade
```

## 📚 Project Structure

```
2. Smart Hiring/
├── app.py                    # Streamlit web interface
├── setup.py                  # Automated setup script
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── QUICKSTART.md            # This file
│
├── data/
│   ├── skills_lexicon.json   # Skills database
│   ├── education_levels.json # Education degrees
│   ├── raw/
│   │   ├── resumes/          # PDF resumes
│   │   └── jobs/             # Job descriptions
│   └── processed/
│       └── parsed_resumes.json
│
├── src/
│   ├── generate_synthetic_data.py  # Create sample data
│   ├── resume_parser.py            # Resume extraction
│   ├── job_matcher.py              # Semantic matching
│   └── explainability.py           # Visualizations
│
└── results/
    └── matches/              # Matching results
```

## 💡 Tips for Students

1. **Start Simple**: Run the automated setup first
2. **Explore Modules**: Run each Python script individually to understand
3. **Modify Data**: Try adding your own skills or job descriptions
4. **Experiment**: Adjust weights and see how rankings change
5. **Read Code**: Each module is well-commented and ~200-300 lines

## 🎓 Learning Objectives

- **NLP**: Text extraction, entity recognition, embeddings
- **Machine Learning**: Semantic similarity, cosine distance
- **Explainable AI**: Transparent scoring, feature importance
- **Web Development**: Interactive dashboards with Streamlit
- **Software Engineering**: Modular design, clean code

## 📖 Further Reading

- Sentence Transformers: https://www.sbert.net/
- spaCy NER: https://spacy.io/usage/linguistic-features#named-entities
- Fuzzy String Matching: https://github.com/seatgeek/fuzzywuzzy
- Streamlit: https://docs.streamlit.io/


