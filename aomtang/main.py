from flask import Flask, redirect, url_for, render_template, request , session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "password"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def hello_world():
    return render_template("/home_page/index.html")

@app.route("/login", methods = ["POST", "GET"])
def login(): 
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("/login_page/login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out, {user}", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)