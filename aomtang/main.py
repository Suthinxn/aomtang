from flask import Flask, redirect, url_for, render_template, request , session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "password"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

@app.route("/")
def welcome():
    return render_template("/welcome_page/welcome.html")

@app.route("/home")
def home():
    return render_template("/home_page/home.html")

@app.route("/view")
def view():
    return render_template("/views_page/views.html", values=users.query.all())

@app.route("/login", methods = ["POST", "GET"])
def login(): 
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

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
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was save!")
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

@app.route("/register")
def register():
    return render_template("/register_page/register.html")

@app.route("/login_or_register")
def login_or_register():
    return render_template("/login_or_register_page/login_or_register.html")\
    

@app.route("/news")
def news():
    return render_template("/news_page/news.html")

@app.route("/income_and_expense")
def income_expense():
    return render_template("/income_expense_page/income_expense.html")

@app.route("/saving")
def saving():
    return render_template("/saving_page/saving.html")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)