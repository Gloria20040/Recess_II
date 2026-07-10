from flask import Flask, render_template, request

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "1234"

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        return render_template("success.html", username=username)

    return "Invalid Username or Password"


if __name__ == "__main__":
    app.run(debug=True)