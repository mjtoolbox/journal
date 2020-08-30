from flask import Flask, render_template, request
import sqlite3
import sys

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/journals")
def journals():
    return render_template("Journals.html")

@app.route("/new")
def newJournal():
    return render_template("NewJournal.html")

if __name__ == "__main__":
    app.run()