from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)
app.secret_key = "password123lol"


@app.route("/")
def home():
    return "<h1>Welcome to SecurePortal</h1>"


@app.route("/info")
def about():
    return "<h2>About SecurePortal</h2><p>SecurePortal is being developed as part of CSC2031.</p>"


@app.route("/talk/<name>")
def contact(name):
    return "<h2>Contact Us</h2><p>Email: support@.com</p>"


@app.route("/status/")
def status():
    return "<h1>secure portal is running </h1> <p>on html except i have to write the html as a string which hurts  </p>"


@app.route("/hellox")
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


@app.route("/remember", methods=["GET", "POST"])
def remember():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect(url_for("whoami"))
    return render_template("rememberer.html")


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
