import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, json
import ppa
import sys
import shutil


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = 'random string'

@app.route('/random', methods=['POST'])
def random():
	return json.dumps(request.json)

@app.route('/getResponse', methods=['POST'])
def getResponseList():
    responseList=[]
    requestObj=request.json
    for t in requestObj["resumes"]:
        dictObj=ppa.getDictObj(t["text"])
        responseList.append(dictObj)
    return json.dumps(responseList)

@app.route('/')
def my_form():
    return render_template('choose_an_option.html')

@app.route("/recommendResumes", methods=['POST'])
def rec():
    perc=request.form['perc']
    jd=request.form['jd']
    if(len(jd)==0 or len(perc)==0):
        flash("Please fill the required fields")
        return render_template('query_and_per.html')
    try:
        perc=int(perc)
    except:
        return ('please enter integer value in percentage')
    ppa.recommend(jd,perc)
    final_file="/".join([APP_ROOT, 'Recommended.csv'])
    return send_file(final_file)


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'uploads/')
    final_file="/".join([APP_ROOT, 'allResumeData.csv'])
    #print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        #print(destination)
        file.save(destination)
    ppa.allToExcel(target)
    shutil.rmtree(target)
    return send_file(final_file, attachment_filename='All Resume Database.csv')



@app.route('/choiceMade', methods=['POST'])
def choice_a():
    selected_choice=request.form['choice']
    if(selected_choice=='compile'):
       return render_template('upload.html')
    if(selected_choice=='recommend'):
       return render_template('query_and_per.html')
    if(selected_choice=='exit'):
       return 'Thanks for visiting. Hope You get placed :)'


def getResponseObj(requestObj):
    return ppa.getDictObj(

if __name__ == '__main__':
   app.run()
