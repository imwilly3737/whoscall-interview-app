from flask import Flask

from tasks.tasks import Tasks

app = Flask(__name__)


@app.route("/health_check")
def health_check():
    return "Ok"


@app.route("/tasks")
def get_tasks():
    return "task"
