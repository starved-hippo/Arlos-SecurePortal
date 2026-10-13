from flask import Flask, request, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.get(username)
        if user and check_password_hash(user["password"], password):
            session["username"] = username
            session["role"] = user["role"]
        else:
            return f"""<h1>incorrect username or password</h1> <a href="/dashboard">Dashboard</a>"""

        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return """
    <h2>Logged out</h2>
    <p>The remembered username and password has been removed from the session.</p>
    <p><a href="/dashboard">Return to the dashboard</a></p>
    """


# protected routes
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


# database
users = {
    "amina": {"password": generate_password_hash("Cyber123"), "role": "Student"},
    "admin": {"password": generate_password_hash("Admin123"), "role": "Administrator"},
}


# depreciated pages
@app.route("/info")
def about():
    return "<h2>About SecurePortal</h2><p>SecurePortal is being developed as part of CSC2031.</p>"


@app.route("/talk/<name>")
def contact(name):
    return "<h2>Contact Us</h2><p>Email: support@.com</p>"


@app.route("/status/")
def status():
    return "<h1>secure portal is running </h1> <p>on html except i have to write the html as a string which hurts  </p>"


@app.route("/hello")
def greet():
    name = request.args.get("name", "")
    return f"""
    <h1>Welcome to SecurePortal</h1>
    <form>
        <label>what is Your name:</label>
        <input type="text" name="name">
        <input type="submit" value="Say Hello">
    </form>
    <p>Hello you are{name}!</p>
    """


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"search term: {query}"


@app.route("/welcome")
def welcome():

    name = request.args.get("q", "")
    if name == "student":
        return "<h2>Student view selected</h2>"
    return f"<h2>Welcome {name}</h2>"


@app.route("/events")
def events():

    category = request.args.get("c", "")

    view = request.args.get("v", "")

    return f"""
    <h2>Event Finder</h2>
    <p>Category: {category}</p>
    <p>View: {view}</p>
    """


@app.route("/whoami")
def whoami():
    username = session.get("username")

    if username:
        return f"""
        <h2>Current User</h2>
        <p>{username}</p>
        """

    return """
    <h2>Current User</h2>
    <p>No user remembered.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)
