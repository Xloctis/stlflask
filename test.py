from flask import Flask
import requests
import json
from types import SimpleNamespace
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return 'username / repository name / type of data request'


allowedTypes = {
    'details': 5,
    'pulls': 4,
    'forks': 3,
    'pullsnew': 2,
    'issues': 1
}


@app.route('/<user_name>/<repo_name>/<requesttype>')
def repo(user_name, repo_name, requesttype):
    if not requesttype in allowedTypes:
        return '400 bad request'
    gitURL = f"https://api.github.com/repos/{user_name}/{repo_name}/"

    if requesttype != 'details':
        gitURL += requesttype
    else:
        gitURL = gitURL[:-1]
    if requesttype == 'pullsnew':
        gitURL = gitURL[:-3]
    gitPull = requests.get(gitURL).json()

    if allowedTypes[requesttype] == 2:
        today = datetime.datetime.today()
        newpullscontainer = []
        for pullItem in gitPull:
            creationDate = pullItem['created_at']
            creationDate = creationDate[:-10]
            cmp = datetime.datetime.strptime(creationDate, "%Y-%m-%d")
            delta = today - cmp
            if delta.days < 14:
                newpullscontainer.append(pullItem)
        dataparse = newpullscontainer
    else:
        dataparse = gitPull

    return dataparse


if __name__ == '__main__':
    app.run()
