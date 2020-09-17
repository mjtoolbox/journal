from flask import Flask, render_template, request, redirect
import sqlite3
import sys
from db import dbconnection

app = Flask(__name__)


@app.route("/")
def home():
    testSelect()
    return render_template("welcome.html")

@app.route("/journals")
def journals():
    
    return render_template("journals.html")

@app.route("/new")
def newJournal():
    return render_template("newJournal.html")

@app.route("/view")
def viewJournal():
    return render_template("viewJournal.html")

# This function is to test db connection
def testSelect():
    cur = dbconnection().cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    for row in rows:
        print(row)

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
