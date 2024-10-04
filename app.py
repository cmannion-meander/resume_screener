from flask import Flask, render_template, jsonify
import json
import random

app = Flask(__name__)

# List of possible industries
industries = ['Technology', 'Healthcare', 'Finance']

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
    return render_template('dashboard.html')

@app.route('/candidates')
def candidates():
    opportunities = get_opportunities()['data']  # Extract opportunities data
    resumes = get_resumes()['data']  # Extract resume data

    # Merge opportunities with corresponding resumes and generate match scores
    for opp in opportunities:
        for resume in resumes:
            if opp['id'] == resume['id']:  # Match opportunity and resume by ID
                opp['resume'] = resume.get('parsedData', {})
                opp['positions'] = resume['parsedData'].get('positions', [])
                opp['schools'] = resume['parsedData'].get('schools', [])

        # Generate random scores for the match factors
        opp['work_experience'] = round(random.uniform(3, 5), 1)  # Random work experience score
        opp['technical_skills'] = round(random.uniform(3, 5), 1)  # Random technical skills score
        opp['soft_skills'] = round(random.uniform(3, 5), 1)  # Random soft skills score
        opp['industry'] = random.choice(industries)  # Randomly assign an industry

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
