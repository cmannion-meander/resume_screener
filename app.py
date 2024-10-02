from flask import Flask, render_template, jsonify
import json

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

    return render_template('index.html', opportunities=opportunities)

if __name__ == '__main__':
    app.run(debug=True)
