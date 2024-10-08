from flask import Flask, render_template, jsonify
import json
import random

app = Flask(__name__)

# List of possible industries
industries = ['Technology', 'Healthcare', 'Finance']

# Load opportunities JSON data
def get_opportunities():
    with open('data/candidates.json') as f:
        return json.load(f)

# Load resumes JSON data
def get_resumes():
    with open('data/resume.json') as f:
        return json.load(f)
    
# Load technical skills JSON data
def get_technical_skills():
    with open('data/technical_skills.json') as f:
        return json.load(f)
    
# Load soft skills JSON data
def get_soft_skills():
    with open('data/soft_skills.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/candidates')
def candidates():
    opportunities = get_opportunities()['data']  # Extract opportunities data
    resumes = get_resumes()['data']  # Extract resume data
    technical_skills = get_technical_skills()['data']  # Extract technical skills data
    soft_skills = get_soft_skills()['data']  # Extract soft skills data

    # Merge opportunities with corresponding resumes and generate match scores
    for opp in opportunities:
        matching_resume = next((resume for resume in resumes if resume['id'] == opp['id']), None)
        if matching_resume:
            opp['positions'] = matching_resume.get('positions', [])  # Get positions for work experience
            opp['schools'] = matching_resume.get('schools', [])  # Get schools for education
            opp['work_experience'] = matching_resume.get('work_experience_rating', 3)  # Default to 3 if not found
        else:
            opp['work_experience'] = 3  # Default work experience if no resume found

        # Extract technical skills
        opp['technical_skills_data'] = next(
            (ts['skills_details'] for ts in technical_skills if ts['id'] == opp['id']), []
        )

        # Extract soft skills
        opp['soft_skills_data'] = next(
            (ss['skills_details'] for ss in soft_skills if ss['id'] == opp['id']), []
        )

        # Generate random skill scores
        opp['technical_skills_score'] = round(random.uniform(3, 5), 1)  # Random score between 3 and 5
        opp['soft_skills_score'] = round(random.uniform(3, 5), 1)  # Random score between 3 and 5

         # Calculate total score as a weighted average
        opp['total_score'] = round((opp['work_experience'] + opp['technical_skills_score'] + opp['soft_skills_score']) / 3, 1)
        
        opp['industry'] = random.choice(industries)  # Randomly assign an industry (to be updated lated)

    return render_template('candidates.html', opportunities=opportunities)


@app.route('/jobs')
def jobs():
    # Example job data
    jobs = [
        {'id': 1, 'title': 'Senior Product Manager', 'location': 'New York', 'industry': 'Technology', 'created_on': '2024-10-04', 'status': 'Open'},
        {'id': 2, 'title': 'Software Engineer', 'location': 'San Francisco', 'industry': 'Technology', 'created_on': '2024-09-22', 'status': 'Closed'}
    ]
    return render_template('jobs.html', jobs=jobs)

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
