from flask import Blueprint,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
from .models import Books,Suggestions,Users
from . import db
from flask_login import login_required,current_user

views = Blueprint('views',__name__,static_folder='static', template_folder='templates')

class Bookpage(FlaskForm):
    Bookname = StringField("Name Of The Book", validators=[DataRequired()])
    Author = StringField("Author Of The Book", validators=[DataRequired()])
    Pic = FileField("Picture Of The Book")
    Submit = SubmitField("Add Book")

class Suggestionpage(FlaskForm):
    Name = StringField("Name Of The Book", validators=[DataRequired()])
    Author = StringField("Author Of The Book")
    Pic = FileField("Picture Of The Book")
    Submit = SubmitField("Add Book")

class UpdateUser(FlaskForm):
    Username = StringField("Username")
    Firstname = StringField("Firstname")
    Surname = StringField("Surname")
    Email = EmailField("Email")
    Submit = SubmitField("Update")


@views.route("/bookpage", methods=["GET", "POST"])
@login_required
def bookpage():
    form = Bookpage()
    if request.method == 'POST':
        name = form.Bookname.data
        author = form.Author.data
        pic = form.Pic.data
        book = Books.query.filter_by(name=name).first()
        if book:
            flash("Book is already added", category="Error")
        elif len(author) < 2:
            flash("Author Name is Too Short",category="Error")
        elif len(name) < 2:
            flash("Book Name is Too Short", category="Error")
        else:
            new_book = Books(name=name, author=author, pic=pic)
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully!You can now read", category="Success")
            return redirect(url_for('views.readbooks'))
    return render_template("bookpage.jinja2", form=form, user=current_user)

@views.route("/suggestions", methods=["GET", "POST"])
@login_required
def suggestions():
    form = Suggestionpage()
    if request.method == 'POST':
        name = form.Name.data
        author = form.Author.data
        pic = form.Pic.data
        book = Books.query.filter_by(name=name).first()
        suggested = Suggestions.query.filter_by(name=name).first()
        if book == suggested:
            flash("Book is already suggested or read", category="Error")
        elif len(author) < 2:
            flash("Author Name is Too Short",category="Error")
        elif len(name) < 2:
            flash("Book Name is Too Short", category="Error")
        else:
            new_book = Suggestions(name=name, author=author, pic=pic)
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully!You can now read", category="Success")
            return redirect(url_for('views.suggestedbooks'))
    return render_template("suggestionspage.jinja2", form=form, user=current_user)

@views.route("/dashboard", methods=["POST","GET"])
@login_required
def dashboard():
    form = UpdateUser()
    if request.method == "POST":
        username = form.Username.data
        firstname = form.Firstname.data
        surname = form.Surname.data
        email = form.Email.data

        user = Users.query.filter_by(email=email).first()
        if user:
            user.email = email
            user.surname = surname
            user.username = username
            user.firstname= firstname
            flash("Profile updated successfully",category="Success")
            db.commit()
            return render_template("dashboard.jinja2", user=current_user, form=form)
        else:
            flash("User is invalid", category="Error")
    return render_template("dashboard.jinja2", user=current_user, form=form)



