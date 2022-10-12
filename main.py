from flask import Flask, render_template, request
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.saramin import extract_saramin_jobs

app = Flask("JobScrapper")

@app.route("/")
def home():
    return render_template("index.html", name="nico")

@app.route("/search")
def hello():
    keyword = request.args.get("keyword")
    indeed = extract_indeed_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    saramin = extract_saramin_jobs(keyword)
    jobs =  indeed + wwr + saramin
    return render_template("search.html", keyword = keyword, jobs = jobs)
    
app.run("127.0.0.1")
