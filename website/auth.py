from flask import Blueprint,request,flash, redirect, url_for, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,PasswordField,SubmitField,EmailField
from wtforms.validators import DataRequired
from .models import Users
from werkzeug.security import check_password_hash,generate_password_hash
from . import db
from flask_login import login_user,login_required,current_user,logout_user

auth = Blueprint('auth',__name__,static_folder='static',template_folder='templates')

class SignupPage(FlaskForm):
    Profilepic = FileField("Profile Picture")
    First_name = StringField("First Name",validators=[DataRequired()])
    Surname = StringField("Surname", validators=[DataRequired()])
    Username = StringField("Username", validators=[DataRequired()])
    Email = EmailField("Email", validators=[DataRequired()])
    Password = PasswordField("Password",validators=[DataRequired()])
    Retype_password= PasswordField("Retype-Password", validators=[DataRequired()])
    Submit= SubmitField("Submit")

class LoginPage(FlaskForm):
    Username = StringField("Username", validators=[DataRequired()])
    Password = PasswordField("Password",validators=[DataRequired()])

    Submit= SubmitField("Login")

class ForgotPass(FlaskForm):
    Email = EmailField("Email", validators=[DataRequired()])
    Password = PasswordField("New Password", validators=[DataRequired()])
    Password2 = PasswordField("Retype Password", validators=[DataRequired()])

    Submit= SubmitField("Submit")

@auth.route("/signup",methods=["POST","GET"])
def signup():
    form = SignupPage()
    if request.method == "POST":
        Profile_pic = form.Profilepic.data
        First_name = form.First_name.data
        Surname = form.Surname.data
        Username = form.Username.data
        Email = form.Email.data
        Password = form.Password.data
        Retype_pasword = form.Retype_password.data

        user = Users.query.filter_by(email= Email).first()
        if user:
            flash("User already exists", category="error")
        elif len(First_name)< 2:
            flash("First_name too short", category="error")
        elif len(Username) < 2:
            flash("Username is Too short", category="error")
        elif len(Surname) <2:
            flash("Surname is too short", category="error")
        elif Password != Retype_pasword:
            flash("Passwords do not match", category="error")
        elif len(Email) < 6:
            flash("The email given is Invalid", category="error")
        else:
            new_user = Users(firstname=First_name,surname=Surname,username=Username,email=Email,password = generate_password_hash(Password,method="sha256"),profpic=Profile_pic)

            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account Created Succesfully!!Now Log in", category="Success")

            return redirect(url_for("auth.login"))

    return render_template("signup.jinja2", form=form, user=current_user)

@auth.route("/",methods=["POST","GET"])
def login():

    form = LoginPage()
    if request.method == 'POST':
        username = form.Username.data
        password = form.Password.data

        user = Users.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login Successful", category="Success")
                login_user(user, remember=True)
                return redirect(url_for("views.bookpage"))
            else:
                flash("Incorrect Password! Try Again",category="error")
        else:
            flash("Username doesn't exist",category="error")
    return render_template("login.jinja2", form=form, user=current_user)

@auth.route("/reset", methods=["POST","GET"])
def reset():
    form = ForgotPass()
    if request.method == "POST":
        Email = form.Email.data
        Password = form.Password.data
        Password2 = form.Password2.data

        user = Users.query.filter_by(email=Email).first()
        if user :
            if Password == Password2:
                user.password = generate_password_hash(Password,method="sha256")
                flash("Password Reset Successfull", category="Success")
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                flash("Passwords Do Not Match!!Try Again",category="Error")

        else:
            flash("Email Does Not Exist!Try Again", category="Error")

    return render_template("forgot.jinja2", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
