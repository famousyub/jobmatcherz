from flask import request, jsonify
from app import app, db, ml_model, resume_parser
from smartmatch import Job, Candidate

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    job_list = [{'id': job.id, 'title': job.title, 'description': job.description} for job in jobs]
    return jsonify(job_list)

@app.route('/apply', methods=['POST'])
def apply():
    data = request.json
    job_id = data.get('job_id')
    name = data.get('name')
    email = data.get('email')
    resume = data.get('resume')

    job = Job.query.get(job_id)
    if not job:
        return jsonify({'message': 'Job not found'}), 404

    skills = resume_parser.extract_skills(resume)
    candidate = Candidate(name=name, email=email, job_id=job_id, skills=' '.join(skills))
    db.session.add(candidate)
    db.session.commit()

    match_score = ml_model.job_match(job.description, skills)
    return jsonify({'message': 'Application submitted successfully', 'match_score': match_score}), 201
