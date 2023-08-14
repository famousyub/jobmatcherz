import os
import sys

from flask import Flask, request,render_template
from flask_restful import Api
from werkzeug.utils import secure_filename

from flask import jsonify

sys.path.insert(1, '/parser/resumeparse.py')
sys.path.insert(1, '/matcher/candidate_matcher.py')
sys.path.insert(1,'/matcher/job_matcher.py')
from parserr.resumeparse import resumeparse
from matcher.candidate_matcher import recommend_candidates
from matcher.job_matcher import recommend_jobs
app = Flask(__name__)
api = Api(app)
from functools import reduce



def remove(string):
    string  = str(string)
    return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "");


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST', 'GET'])
def users():
    file = request.files["resume"]
    if file.filename == "":
        return "No file selected"
    filename = secure_filename(file.filename)
    if file.filename == '':
        return "No selected file"
    
    resumefilename=remove(file.filename)
    
    # Save the uploaded file
    resume_path = os.path.join('uploads',resumefilename )
    file.save(resume_path)
    file.save("./uploads/" + filename)
    data = resumeparse.read_file(filename)
    os.remove(filename)
    return data


@app.route('/api/recommend/<int:job_id>/<int:number_of_candidates>', methods=['GET'])
def recommend_candidates_for_job(job_id, number_of_candidates):
    return jsonify(recommend_candidates(job_id, number_of_candidates))


@app.route('/api/recommend_job/<int:candidate_id>/<int:number_of_jobs>', methods=['GET'])
def recommend_jobs_for_candidates(candidate_id, number_of_jobs):
    return jsonify(recommend_jobs(candidate_id, number_of_jobs))


if __name__ == "__main__":
    app.run(port=5000, host='localhost')
