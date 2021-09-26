from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_manager, login_user, login_required, logout_user, current_user, LoginManager
# import sqlite3
# from sqlite3 import Error
import psycopg2
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from postgresdb import dbconnection
from user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mypass'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def findUserByEmail(email):
    try:
        con = dbconnection()
        cur = con.cursor()
        cur.execute("select * from users where email = %s", (email,))
        row = cur.fetchone()
        if row is None:
            return None
        else:
            user = User(row[0], row[1], row[2], row[3], row[4])
            return user
    except Exception as e:
        print("error" + e)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = findUserByEmail(user_id)
        return user
    except Exception as e:
        print("error" + e)


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route("/login")
def loginview():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = findUserByEmail(email)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('login'))

    print("login print user")
    print(user)
    login_user(user, remember=remember)
    return redirect(url_for('profile'))


@app.route("/signup")
def signupview():
    return render_template('signup.html')


@app.route("/signup", methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = 'user'

    print("signup: " + name + " " + email + " " + password)

    user = findUserByEmail(email)

    if user:
        flash("Email address already exists")
        return redirect(url_for('signup'))

    con = dbconnection()
    cur = con.cursor()
    cur.execute("INSERT INTO users (email, password, name, role) VALUES (%s,%s,%s,%s); ",
                (email, generate_password_hash(password, method='sha256'), name, role))

    con.commit()
    return redirect(url_for('login'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile')
@login_required
def profile():
    print("current user " + current_user.name)
    return render_template('profile.html', name=current_user.name)


@app.route("/journals")
@login_required
def journals():
    con = dbconnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM Journal")
    rows = cur.fetchall()
    return render_template("journals.html", journals=rows)


@app.route("/new")
@login_required
def newJournal():
    return render_template("newJournal.html")


@app.route("/addJournal", methods=['POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
