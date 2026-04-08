"""
Resume Parser Module
Extracts structured information from PDF resumes using NLP techniques
"""

import re
import json
import pdfplumber
from pathlib import Path
from fuzzywuzzy import fuzz, process
import spacy

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Load resources
with open(DATA_DIR / "skills_lexicon.json", 'r') as f:
    SKILLS_DATA = json.load(f)

with open(DATA_DIR / "education_levels.json", 'r') as f:
    EDUCATION_DATA = json.load(f)

# Flatten skills list
ALL_SKILLS = []
for category in SKILLS_DATA.values():
    ALL_SKILLS.extend(category)

# Load spaCy model for NER
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None


class ResumeParser:
    """Parse resumes and extract structured information"""
    
    def __init__(self):
        self.skills_list = ALL_SKILLS
        self.education_degrees = EDUCATION_DATA['degrees']
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for password-protected PDFs
            if 'password' in error_msg or 'encrypted' in error_msg:
                raise ValueError(f"Password-protected PDF - File not supported")
            
            # Check for corrupted or invalid PDFs
            elif 'invalid' in error_msg or 'corrupt' in error_msg or 'damaged' in error_msg:
                raise ValueError(f"Corrupted or invalid PDF file")
            
            # Check for unsupported PDF features
            elif 'unsupported' in error_msg or 'not supported' in error_msg:
                raise ValueError(f"Unsupported PDF format")
            
            # Generic error for other cases
            else:
                raise ValueError(f"Unable to read PDF - File may be corrupted or in an unsupported format")
        
        if not text.strip():
            raise ValueError(f"PDF appears to be empty or contains no readable text")
        
        return text
    
    def normalize_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@.+\-(),:]', '', text)
        return text.strip()
    
    def extract_name(self, text):
        """Extract candidate name using spaCy NER"""
        if not nlp:
            # Fallback: take first line as name
            lines = text.split('\n')
            name = lines[0].strip() if lines else "Unknown"
            # Remove email if present
            name = re.sub(r'\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '', name)
            return name.strip()
        
        # Use first few lines where name typically appears
        first_lines = '\n'.join(text.split('\n')[:3])
        doc = nlp(first_lines)
        
        # Look for PERSON entities
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                # Remove email if it got included in the entity
                name = re.sub(r'\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '', name)
                return name.strip()
        
        # Fallback
        name = text.split('\n')[0].strip() if text else "Unknown"
        # Remove email if present
        name = re.sub(r'\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', '', name)
        return name.strip()
    
    def extract_email(self, text):
        """Extract email using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone number using regex"""
        # Matches formats: +1-555-0101, (555) 555-5555, 555-555-5555, etc.
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        return phones[0].strip() if phones else None
    
    def extract_address(self, text):
        """Extract address/location using spaCy NER"""
        if not nlp:
            return None
        
        doc = nlp(text[:500])  # Check first 500 chars
        
        # Look for GPE (Geopolitical Entity) or LOC (Location)
        locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
        return locations[0] if locations else None
    
    def extract_skills(self, text, threshold=80):
        """Extract skills using fuzzy matching against skills lexicon"""
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.skills_list:
            skill_lower = skill.lower()
            
            # Exact match
            if skill_lower in text_lower:
                found_skills.add(skill)
            else:
                # Fuzzy match for slight variations
                words = text_lower.split()
                for word in words:
                    if fuzz.ratio(skill_lower, word) >= threshold:
                        found_skills.add(skill)
                        break
        
        return list(found_skills)
    
    def extract_education(self, text):
        """Extract highest education level using fuzzy matching"""
        text_lower = text.lower()
        best_match = None
        highest_level = -1
        
        for degree in self.education_degrees:
            # Check degree name and aliases
            all_terms = [degree['name']] + degree['aliases']
            
            for term in all_terms:
                if term.lower() in text_lower:
                    if degree['level'] > highest_level:
                        highest_level = degree['level']
                        best_match = degree['name']
                    break
        
        return best_match if best_match else "Not Specified"
    
    def extract_experience_years(self, text):
        """Extract years of experience from text"""
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+in',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        
        # Try to count date ranges in experience section
        # Look for patterns like "2020-2023", "2020-Present"
        date_pattern = r'(20\d{2})\s*[-–]\s*(20\d{2}|Present|Current)'
        date_ranges = re.findall(date_pattern, text)
        
        if date_ranges:
            total_years = 0
            current_year = 2026
            
            for start, end in date_ranges:
                start_year = int(start)
                end_year = current_year if end in ['Present', 'Current'] else int(end)
                total_years += (end_year - start_year)
            
            return total_years
        
        return 0
    
    def parse_resume(self, pdf_path):
        """Complete parsing pipeline for a single resume"""
        print(f"\nParsing: {pdf_path.name}")
        
        # Extract text
        raw_text = self.extract_text_from_pdf(pdf_path)
        text = self.normalize_text(raw_text)
        
        # Extract all entities
        parsed_data = {
            'filename': pdf_path.name,
            'name': self.extract_name(raw_text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'address': self.extract_address(raw_text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'experience_years': self.extract_experience_years(text),
            'raw_text': text[:500]  # Store first 500 chars for reference
        }
        
        print(f"   Name: {parsed_data['name']}")
        print(f"   Skills: {len(parsed_data['skills'])} found")
        print(f"   Education: {parsed_data['education']}")
        print(f"   Experience: {parsed_data['experience_years']} years")
        
        return parsed_data
    
    def parse_all_resumes(self, resumes_dir):
        """Parse all PDF resumes in a directory"""
        resumes_dir = Path(resumes_dir)
        pdf_files = list(resumes_dir.glob("*.pdf"))
        
        print(f"\nFound {len(pdf_files)} resumes to parse")
        print("="*60)
        
        parsed_resumes = []
        errors = []
        
        for pdf_file in pdf_files:
            try:
                parsed_data = self.parse_resume(pdf_file)
                parsed_resumes.append(parsed_data)
            except ValueError as e:
                # Specific errors (password-protected, corrupted, etc.)
                error_msg = f"{pdf_file.name}: {str(e)}"
                print(f"   {error_msg}")
                errors.append({'file': pdf_file.name, 'error': str(e)})
            except Exception as e:
                # Unexpected errors
                error_msg = f"{pdf_file.name}: Unexpected error - {str(e)}"
                print(f"   {error_msg}")
                errors.append({'file': pdf_file.name, 'error': f"Unexpected error: {str(e)}"})
        
        return parsed_resumes, errors
    
    '''def save_parsed_data(self, parsed_resumes, output_path, errors=None):
        """Save parsed resumes to JSON (overwrites existing file)"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Always overwrite the file (not append)
        with open(output_path, 'w') as f:
            json.dump(parsed_resumes, f, indent=2)
        
        print(f"\nSaved {len(parsed_resumes)} parsed resumes to: {output_path}")
        
        # Save errors to separate file if any
        if errors:
            error_path = output_path.parent / "parsing_errors.json"
            with open(error_path, 'w') as f:
                json.dump(errors, f, indent=2)
            print(f"Saved {len(errors)} parsing errors to: {error_path}")'''
            
    def save_parsed_data(self, parsed_resumes, output_path, errors=None):
        """Save parsed resumes to JSON (overwrites existing file)"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Always overwrite parsed resumes file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_resumes, f, indent=2, ensure_ascii=False)

        print(f"\nSaved {len(parsed_resumes)} parsed resumes to: {output_path}")

        # Always overwrite parsing_errors.json too
        error_path = output_path.parent / "parsing_errors.json"
        with open(error_path, 'w', encoding='utf-8') as f:
            json.dump(errors if errors else [], f, indent=2, ensure_ascii=False)

        print(f"Saved {len(errors) if errors else 0} parsing errors to: {error_path}")


def main():
    """Main execution"""
    print("="*60)
    print("RESUME PARSING MODULE")
    print("="*60)
    
    parser = ResumeParser()
    
    # Parse all resumes (regenerates from scratch)
    resumes_dir = DATA_DIR / "raw" / "resumes"
    parsed_resumes, errors = parser.parse_all_resumes(resumes_dir)
    
    # Save results (overwrites existing JSON)
    output_path = DATA_DIR / "processed" / "parsed_resumes.json"
    parser.save_parsed_data(parsed_resumes, output_path, errors)
    
    print("\n" + "="*60)
    print(f"PARSING COMPLETE!")
    print(f"Successfully parsed: {len(parsed_resumes)} resumes")
    if errors:
        print(f"Failed to parse: {len(errors)} resumes")
    print("="*60)


if __name__ == "__main__":
    main()
