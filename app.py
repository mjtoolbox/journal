from flask import Flask, render_template, request, redirect
from flask_simplelogin import SimpleLogin
from flask_simplelogin import login_required
# import sqlite3
# from sqlite3 import Error
import psycopg2
import sys
from postgresdb import dbconnection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route("/journals")
def journals():
    con = dbconnection()
    # con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    return render_template("journals.html", journals=rows)


@login_required
@app.route("/new")
def newJournal():
    return render_template("newJournal.html")


@app.route("/addJournal", methods=['POST'])
def addJournal():
    msg = ""
    try:
        # Insert to DB
        title = request.form['title']
        date = request.form['date']
        author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']

        con = dbconnection()
        cur = con.cursor()
        cur.execute("INSERT INTO Journal (title, date, author, tag, emotion, content) VALUES (%s,%s,%s,%s,%s,%s); ",
                    (title, date, author, tag, emotion, content))

        con.commit()
        msg = "Journal successfully saved"
        return redirect("/journals")
    except Exception as e:
        print("Hey there is an error: " + e)
        msg = e
    finally:
        cur.close()
        con.close()
        # return render_template("result.html", msg=msg)


@app.route("/edit/<int:id>")
def editJournal(id):
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("select * from Journal where id = %s", (str(id),))
        row = cur.fetchone()
        print("Edit")
        print(row)
        if row:
            return render_template("editJournal.html", aJournal=row)
        else:
            msg = "Cannot find the journal with this id"
    except Exception as e:
        print("There is an error", e)
        msg = e
    finally:
        cur.close()
        con.close()


@ app.route("/update", methods=["POST"])
def updateJournal():
    msg = ""
    try:
        _id = request.form['id']
        title = request.form['title']
        date = request.form['date']
        # author = request.form['author']
        tag = request.form['tag']
        emotion = request.form['emotion']
        content = request.form['content']

        con = dbconnection()
        cur = con.cursor()
        cur.execute("UPDATE Journal SET title = %s, date = %s, content = %s, emotion = %s, tag = %s WHERE id = %s",
                    (title, date, content, emotion, tag, _id))
        con.commit()
        msg = "Journal successfully updated!"
        return redirect("/journals")
    except Exception as e:
        print("Error " + e)
        con.rollback()
        msg = "There is an error, rollback the change."
    finally:
        cur.close()
        con.close()


@app.route("/delete/<int:id>")
def deleteJournal(id):
    msg = ""
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("delete from Journal where id = %s", (str(id),))
        con.commit()
        msg = "Journal deleted successfully!"
        # return render_template("result.html", msg=msg)
        return redirect("/journals")
    except Exception as e:
        print("Error " + e)
        con.rollback()
        msg = "There is an error while deleting."
    finally:
        cur.close()
        con.close()

# def editJournal():
#     msg = ""
#     try:
#         con = dbconnection()
#         cur = con.cursor()
#         cur.execute("SELECT * FROM Journal WHERE id = ?", str(1))
#         row = cur.fetchone()
#         if row:
#             return render_template("editJournal.html", aJournal=row)
#         else:
#             msg = "Cannot find the journal with this id"
#     except Error as e:
#         print("There is an error " + e)
#         msg = e
#     finally:
#         cur.close()
#         con.close()


@ app.route("/view")
def viewJournal():
    return render_template("viewJournal.html")

# This function is to retrieve all Journals


def findAllJournals():
    con = dbconnection()
    # con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
