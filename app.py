from flask import Flask, request

app = Flask(__name__)

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

@app.route('/greet')
def method_name():
    name = request.args.get("name", "")
    return f"""
    <h1>Welcome to SecurePortal</h1>
    <form>
        <label>Your name:</label>
        <input type="text" name="name">
        <input type="submit" value="Say Hello">
    </form>
    <p>Hello {name}!</p>
    """
    pass

if __name__ == "__main__":
    app.run(debug=True)