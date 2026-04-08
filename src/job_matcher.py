"""
Job Matching Module
Semantic matching between resumes and job descriptions using transformer embeddings
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"


class JobMatcher:
    """Match candidates to jobs using semantic similarity"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize with sentence transformer model"""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully")
        
        # Weights for different matching criteria
        self.weights = {
            'skills': 0.50,        # Most important
            'experience': 0.20,
            'education': 0.15,
            'location': 0.15
        }
    
    def encode_skills(self, skills_list):
        """Encode skills using sentence transformer"""
        if not skills_list:
            return np.zeros((1, 384))  # Return zero vector
        
        # Join skills into a single text for encoding
        skills_text = ", ".join(skills_list)
        embedding = self.model.encode([skills_text])
        return embedding
    
    def compute_skills_similarity(self, resume_skills, job_skills):
        """Compute semantic similarity between resume and job skills"""
        if not resume_skills or not job_skills:
            return 0.0
        
        # Encode both skill sets
        resume_embedding = self.encode_skills(resume_skills)
        job_embedding = self.encode_skills(job_skills)
        
        # Compute cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return float(similarity)
    
    def compute_experience_match(self, candidate_years, required_years):
        """Score experience match"""
        if candidate_years >= required_years:
            # Perfect match or overqualified
            return 1.0
        elif candidate_years >= required_years * 0.7:
            # Close enough (70% of required)
            return 0.8
        elif candidate_years >= required_years * 0.5:
            # Somewhat qualified
            return 0.5
        else:
            # Under-qualified
            return 0.3
    
    def compute_education_match(self, candidate_edu, required_edu):
        """Score education match"""
        # Education level mapping
        edu_levels = {
            'PhD': 5, 'Master': 4, 'Engineer': 4,
            'Bachelor': 3, 'Associate': 2, 'Diploma': 1,
            'High School': 0, 'Not Specified': 0
        }
        
        candidate_level = edu_levels.get(candidate_edu, 0)
        required_level = edu_levels.get(required_edu, 0)
        
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level >= required_level - 1:
            return 0.7
        else:
            return 0.4
    
    def compute_location_match(self, candidate_location, job_location):
        """Score location match"""
        if not candidate_location or not job_location:
            return 0.5  # Neutral if missing
        
        # Remote jobs match everyone
        if 'remote' in job_location.lower():
            return 1.0
        
        # Simple string matching (can be enhanced with geocoding)
        candidate_lower = candidate_location.lower()
        job_lower = job_location.lower()
        
        if candidate_lower in job_lower or job_lower in candidate_lower:
            return 1.0
        else:
            return 0.3
    
    def match_candidate_to_job(self, candidate, job):
        """
        Compute overall match score between candidate and job
        
        Returns:
            dict with overall score and component scores
        """
        # Compute individual scores
        skills_score = self.compute_skills_similarity(
            candidate.get('skills', []),
            job.get('required_skills', []) + job.get('preferred_skills', [])
        )
        
        experience_score = self.compute_experience_match(
            candidate.get('experience_years', 0),
            job.get('experience_required', 0)
        )
        
        education_score = self.compute_education_match(
            candidate.get('education', 'Not Specified'),
            job.get('education_required', 'Bachelor')
        )
        
        location_score = self.compute_location_match(
            candidate.get('address', ''),
            job.get('location', '')
        )
        
        # Weighted overall score
        overall_score = (
            self.weights['skills'] * skills_score +
            self.weights['experience'] * experience_score +
            self.weights['education'] * education_score +
            self.weights['location'] * location_score
        )
        
        return {
            'candidate_name': candidate.get('name', 'Unknown'),
            'overall_score': round(overall_score * 100, 2),  # Convert to percentage
            'component_scores': {
                'skills': round(skills_score * 100, 2),
                'experience': round(experience_score * 100, 2),
                'education': round(education_score * 100, 2),
                'location': round(location_score * 100, 2)
            },
            'candidate_data': {
                'email': candidate.get('email'),
                'phone': candidate.get('phone'),
                'skills': candidate.get('skills', []),
                'education': candidate.get('education'),
                'experience_years': candidate.get('experience_years')
            }
        }
    
    def rank_candidates(self, candidates, job):
        """
        Rank all candidates for a job
        
        Returns:
            List of match results sorted by score (highest first)
        """
        print(f"\nMatching candidates for: {job.get('title', 'Unknown Job')}")
        print("="*60)
        
        matches = []
        for candidate in candidates:
            match_result = self.match_candidate_to_job(candidate, job)
            matches.append(match_result)
            print(f"  {match_result['candidate_name']}: {match_result['overall_score']}%")
        
        # Sort by overall score (descending)
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return matches
    
    def save_results(self, matches, job_title, output_path):
        """Save matching results to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = {
            'job_title': job_title,
            'total_candidates': len(matches),
            'ranked_candidates': matches
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n Results saved to: {output_path}")


def main():
    """Main execution"""
    print("="*60)
    print("JOB MATCHING MODULE")
    print("="*60)
    
    # Load parsed resumes
    parsed_resumes_path = DATA_DIR / "processed" / "parsed_resumes.json"
    with open(parsed_resumes_path, 'r') as f:
        candidates = json.load(f)
    
    # Load job descriptions
    jobs_path = DATA_DIR / "raw" / "jobs" / "job_descriptions.json"
    with open(jobs_path, 'r') as f:
        jobs = json.load(f)
    
    print(f"\nLoaded {len(candidates)} candidates and {len(jobs)} jobs")
    
    # Initialize matcher
    matcher = JobMatcher()
    
    # Match candidates to each job
    for i, job in enumerate(jobs):
        print(f"\n{'='*60}")
        print(f"JOB {i+1}: {job['title']}")
        print(f"{'='*60}")
        
        matches = matcher.rank_candidates(candidates, job)
        
        # Save results
        job_filename = job['title'].replace(' ', '_').lower()
        output_path = RESULTS_DIR / "matches" / f"{job_filename}_matches.json"
        matcher.save_results(matches, job['title'], output_path)
        
        # Print top 3 candidates
        print(f"\n Top 3 Candidates:")
        for idx, match in enumerate(matches[:3], 1):
            print(f"  {idx}. {match['candidate_name']} - {match['overall_score']}%")
    
    print("\n" + "="*60)
    print("MATCHING COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
