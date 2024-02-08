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
        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In")
            return redirect(url_for("user"))
        return render_template("/login_page/login.html")

@app.route("/user", methods =["POST", "GET"])
def user():
    email = None

    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]


        return render_template("/user_page/user.html", email = email)
    flash("You are not logged in!")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():

    flash("You have been logged out" "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)