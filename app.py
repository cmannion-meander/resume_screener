from flask import Flask, jsonify, request, render_template
import os
import json

app = Flask(__name__)

# Set path for data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Load the job description JSON
def get_job_description():
    with open(os.path.join(DATA_DIR, 'job_description.json')) as f:
        return json.load(f)

# Load the resume JSON
def get_resumes():
    with open(os.path.join(DATA_DIR, 'resume.json')) as f:
        return json.load(f)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Simulate the scoring and render the results page
@app.route('/api/score_resumes', methods=['POST'])
def score_resumes():
    resumes = get_resumes()
    job_description = get_job_description()
    
    scored_resumes = []

    for resume in resumes:
        score = 0
        # Scoring based on required skills
        for skill in job_description['required_skills']:
            if skill in resume['skills']:
                score += 1

        # Bonus for preferred skills
        for skill in job_description['preferred_skills']:
            if skill in resume['skills']:
                score += 0.5

        # Experience scoring
        if resume['years_of_experience'] >= job_description['min_experience']:
            score += 1

        # Education scoring
        if resume['education'] == job_description['min_education']:
            score += 1

        scored_resumes.append({
            'candidate_id': resume['candidate_id'],
            'name': resume['name'],
            'email': resume['email'],
            'score': score
        })

    # Sort resumes by score
    scored_resumes = sorted(scored_resumes, key=lambda x: x['score'], reverse=True)

    # Pass job title and company from the job description
    return render_template('results.html', candidates=scored_resumes, job_title=job_description['title'], company=job_description['company'])

if __name__ == '__main__':
    app.run(debug=True)
