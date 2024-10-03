from flask import Flask, render_template, jsonify
import json
import random

app = Flask(__name__)

# Load opportunities JSON data
def get_opportunities():
    with open('data/lever_opportunities.json') as f:
        return json.load(f)

# Load resumes JSON data
def get_resumes():
    with open('data/lever_resumes.json') as f:
        return json.load(f)

@app.route('/')
def home():
    opportunities = get_opportunities()['data']  # Extract opportunities data
    resumes = get_resumes()['data']  # Extract resume data

    # Merge opportunities with corresponding resumes
    for opp in opportunities:
        for resume in resumes:
            if opp['id'] == resume['id']:  # Match opportunity and resume by ID
                opp['resume'] = resume['file']['downloadUrl'] if resume.get('file') else None
                opp['positions'] = resume.get('parsedData', {}).get('positions', [])
                opp['schools'] = resume.get('parsedData', {}).get('schools', [])

        # Generate random scores for the match factors
        opp['skill_match'] = round(random.uniform(3, 5), 1)  # Random skill match score (between 3 and 5)
        opp['experience_fit'] = round(random.uniform(3, 5), 1)  # Random experience fit score (between 3 and 5)
        opp['career_trajectory'] = round(random.uniform(3, 5), 1)  # Random career trajectory score (between 3 and 5)

    return render_template('index.html', opportunities=opportunities)

def calculate_match_score(opportunity, resume):
    # Simulated scoring logic
    score = 0

    # Skill Matching (example logic)
    required_skills = ["Java", "Python", "SQL", "Agile"]
    candidate_skills = ["Java", "Python", "SQL"]  # Example candidate skills (this should come from resume)

    matched_skills = set(candidate_skills) & set(required_skills)
    skill_score = len(matched_skills) / len(required_skills) * 5  # Score out of 5

    # Experience Matching (example logic)
    positions = resume.get('parsedData', {}).get('positions', [])
    if positions:
        experience_score = 4.5  # Assuming good experience match for now
    else:
        experience_score = 2  # Lower score for no relevant experience

    # Education Matching (example logic)
    schools = resume.get('parsedData', {}).get('schools', [])
    if schools:
        education_score = 4  # Higher if education matches role requirements
    else:
        education_score = 2

    # Final score is an average of all components
    final_score = (skill_score + experience_score + education_score) / 3
    return round(final_score, 1)


if __name__ == '__main__':
    app.run(debug=True)
