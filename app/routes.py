from app import app
from flask import render_template
from flask import url_for
from flask import redirect
from app.models import Jobs
from flask import request
import pdb
from Analysis.Analysis import Analysis


@app.route('/')
def base():
    #return render_template('base.html')
    return (url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/jobs', methods=['POST', 'GET'])
def jobs_compare():
    jobs = request.form.get('jobs', '').split(' ')
    jobs_list = list(map(lambda x: "'" + x + "'", jobs))
    plot_url = Analysis().jobs_salary(jobs_list)
    return render_template('jobs_compare.html', plot_url=plot_url)


@app.route('/job/<job_category>')
def job(job_category):
    return job_category
