from flask import Flask, request ,jsonify,render_template
import os
from  extractdatapdf import extract_data_from_resume
import nltk
import json
#from condidatmatcher import matchers,preprocess_text

#from matcher  import Matchercondidat


from functools import reduce

import mysql.connector


mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="myarticles"
)
#Function to remove white space
def remove(string):
    string  = str(string)
    return reduce(lambda x, y: (x+y) if (y != " ") else x, string, "")











    



def  getkeysjobs(id):
    db=mysql.connector.connect(host="localhost", user="root", password="root",database="db_benz")

    cursor=db.cursor()
    offres = []

    query="SELECT  id, mots_cles  FROM emploi "
    cur = cursor.execute(query)
  

    for row in cursor:
        print(row[1])
        row =  list(row[1])
        det = " ".join(row[1])
        offres.append(det)

    return offres



app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('upload.html')



@app.route('/match_jobs', methods=['POST'])
def match_jobs():
    data = request.json

    job_title = data['job_title']
    job_skills = data['job_skills']
    cursor = mysql_conn.cursor()

    cursor.execute("SELECT name, skills FROM candidate_skills")
    candidates = cursor.fetchall()

    matched_candidates = []

    for candidate in candidates:
        candidate_name, candidate_skills = candidate
        candidate_skill_tokens = nltk.word_tokenize(candidate_skills)
        job_skill_tokens = nltk.word_tokenize(job_skills)

        # Calculate similarity between job skills and candidate skills
        common_skills = set(candidate_skill_tokens) & set(job_skill_tokens)
        similarity_score = len(common_skills) / len(job_skill_tokens)

        if similarity_score >= 0.5:  # You can adjust the threshold as needed
            matched_candidates.append(candidate_name)

    return jsonify({'matched_candidates': matched_candidates})

@app.route('/upload', methods=['POST'])
def upload():
    nltk.download('averaged_perceptron_tagger')
    if 'resume' not in request.files:
        return "No file part"

    resume_file = request.files['resume']
    if resume_file.filename == '':
        return "No selected file"
    
    resumefilename=remove(resume_file.filename)
    
    # Save the uploaded file
    resume_path = os.path.join('uploads',resumefilename )
    resume_file.save(resume_path)

    # Call the function to extract data from the uploaded resume
    extracted_data = extract_data_from_resume(resume_path)
    print (extracted_data["skills"])

    
    # matcher_ = Matchercondidat(  ["java"],skills=extracted_data["skills"].split(','))
    # cv_file=  resumefilename.split(".")[0]
    # print(cv_file)

    # matcher_.chckmatch(extracted_data,f"http://localhost:5000/show/PDFs/{cv_file}")




   
    

 
    
    
    return jsonify( {'data':extracted_data}  )


import  os 
from flask import send_from_directory

@app.route('/show/PDFs/<filename>')
def send_pdf(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], f'{filename}.pdf')


@app.route("/files")
def   myfiles():


    ls_ =  os.listdir(os.getcwd() + "/uploads")

    return jsonify({'cv':ls_})



if __name__ == '__main__':
    app.run(debug=True)
