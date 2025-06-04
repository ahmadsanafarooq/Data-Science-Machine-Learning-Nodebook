from flask import Flask, render_template, request
import os
import re
from utils.parse_cv import extract_text_from_file
from utils.ats_score import get_ats_score
from utils.improve_cv import suggest_improvements
from utils.job_suggest import suggest_jobs

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def clean_result(text):
    # Remove double asterisks **text**
    return re.sub(r'\*\*(.*?)\*\*', r'\1', text)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['cv']
        action = request.form.get('action')
        job_pref = request.form.get('job_pref', '')

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            cv_text = extract_text_from_file(filepath)

            result = ""
            if action == 'ats':
                result = get_ats_score(cv_text)
            elif action == 'improve':
                result = suggest_improvements(cv_text)
            elif action == 'jobs':
                result = suggest_jobs(cv_text, job_pref)

            # Clean the result before rendering
            result = clean_result(result)

            return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
