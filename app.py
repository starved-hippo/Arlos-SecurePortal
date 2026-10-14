from flask import Flask, request, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "password123lol"


# pages
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    role = session.get("role")

    if username:
        return render_template("dashboard/dashboard.html", username=username, role=role)
    else:
        return render_template("dashboard/dashboard guest.html")


@app.route("/resources")
def resources():
    username = session.get("username")
    role = session.get("role")
    if username not in session:
        return url_for("login")

    if role == "Student":
        return render_template("resources/student.html")
    elif role == "Teacher":
        return render_template("resources/teacher.html")
    elif role == "Admin":
        return render_template("resources/admin.html")
    else:
        return "<h1>no role</h1>"


@app.route("/user_management")
def user_managment():
    role = session.get("role")
    if role == "Admin":
        return """
        <h1>User Management</h1>
        <p>Welcome, Administrator.</p>
        <p>You can manage user accounts and assign roles.</p>"""
    else:
        return """
        <h1>Access Denied</h1>
        <p>You do not have permission to view this page.</p>
        """


@app.route("/search", methods=["GET", "POST"])
def search():
    results = None
    searched = False

    if request.method == "POST":
        searched = True
        username = request.form["username"]

        connection = sqlite3.connect("secureportal.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?",(username,))

        results = cursor.fetchall()
        connection.close()
        
        print("form submitted, results: ", results, "searched: ", searched)
        
    return render_template("resources/search.html", results=results, searched=searched)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = sqlite3.connect("secureportal.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT username, password_hash, role
            FROM users
            WHERE username = ?""",
            (username,),
        )
        # why comma?? pls ask

        user = cursor.fetchone()
        connection.close()

        if user and check_password_hash(user[1], password):
            session["username"] = user[0]
            session["role"] = user[2]
            return redirect(url_for("dashboard"))

        return f"""<p>incorrect username or password, <a href="/login">retry?</a></p>"""
    return render_template("users/login.html")


@app.route("/logout")
def logout():
    session.clear()
    return """
    <h2>Logged out</h2>
    <p>The remembered username and password has been removed from the session.</p>
    <p><a href="/dashboard">Return to the dashboard</a></p>
    """


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = generate_password_hash(request.form["password"])

        connection = sqlite3.connect("secureportal.db")
        cursor = connection.cursor()

        cursor.execute(
            """
        INSERT INTO users (username, password_hash, role) 
        VALUES (?, ?, ?)""",
            (username, password_hash, "Student"),
        )

        connection.commit()
        connection.close()
        return redirect(url_for("dashboard"))

    return render_template("users/register.html")


if __name__ == "__main__":
    app.run(debug=True)
