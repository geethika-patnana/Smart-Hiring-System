"""
Quick Setup Script for Smart-Hiring Project
Automates the complete setup process
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}...")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}")
        print(e.stderr)
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           SMART-HIRING PROJECT SETUP                      ║
    ║     Explainable NLP Pipeline for Resume Matching          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    base_dir = Path(__file__).parent
    
    # Step 1: Install dependencies
    print("\nStep 1: Installing Dependencies")
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    ):
        print("\nWarning: Some packages may have failed to install")
        print("You can continue, but some features may not work")
    
    # Step 2: Download spaCy model
    print("\nStep 2: Downloading NLP Model")
    run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    )
    
    # Step 3: Generate synthetic data
    print("\nStep 3: Generating Synthetic Resumes")
    run_command(
        f"{sys.executable} src/generate_synthetic_data.py",
        "Creating sample resumes and job descriptions"
    )
    
    # Step 4: Parse resumes
    print("\nStep 4: Parsing Resumes")
    run_command(
        f"{sys.executable} src/resume_parser.py",
        "Extracting information from resumes"
    )
    
    # Step 5: Run matching
    print("\nStep 5: Running Job Matching")
    run_command(
        f"{sys.executable} src/job_matcher.py",
        "Computing candidate-job matches"
    )
    
    print(f"\n{'='*60}")
    print("SETUP COMPLETE!")
    print(f"{'='*60}")
    print("\nTo launch the web application, run:")
    print(f"   streamlit run app.py")
    print("\nOr explore individual modules:")
    print(f"   python src/resume_parser.py")
    print(f"   python src/job_matcher.py")
    print("\nCheck README.md for more information")

if __name__ == "__main__":
    main()
