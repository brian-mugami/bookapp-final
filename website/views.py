import uuid
import os
from .forms import Bookpage,Search,UpdateUser,UpdateBook
from flask import Blueprint,render_template,flash,request,redirect,url_for
from .models import Books,Users
from . import db
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'website/static/images/'

views = Blueprint('views',__name__,static_folder='static', template_folder='templates')

@views.route("/bookpage", methods=["GET", "POST"])
@login_required
def bookpage():
    form = Bookpage()
    if request.method == 'POST':
        name = form.Bookname.data
        author = form.Author.data
        about = form.About.data

        book = Books.query.filter_by(name=name).first()
        if book:
            flash("Book is already added", category="Error")
        elif len(author) < 2:
            flash("Author Name is Too Short",category="Error")
        elif len(name) < 2:
            flash("Book Name is Too Short", category="Error")
        else:
            new_book = Books(name=name, author=author, about=about, user_id=current_user.id)
            db.session.add(new_book)
            db.session.commit()

            flash("Book added successfully!You can now read", category="Success")
            return redirect(url_for('views.allbooks'))
    return render_template("bookpage.jinja2", form=form, user=current_user)

@views.route("/dashboard/<int:id>", methods=["POST","GET"])
@login_required
def dashboard(id):
    form = UpdateUser()
    user = Users.query.get(id)
    if request.method == "POST":
        user.username = form.Username.data
        user.firstname = form.Firstname.data
        user.surname = form.Surname.data
        user.email = form.Email.data
        user.profpic = form.Profile_pic.data

        #grab pic
        pic = secure_filename(user.profpic.filename)
        #set uuid
        pic_name = str(uuid.uuid4()) + "_" + pic

        #change to string
        user.profpic = pic_name
        # save image
        saver = form.Profile_pic.data
        try:
            flash("Profile updated successfully", category="Success")
            db.session.commit()
            saver.save(os.path.join(UPLOAD_FOLDER, pic_name))
            return render_template("dashboard.jinja2", user=current_user, form=form)
        except:
            flash("Invalid user",category="Error")
    else:
        return render_template("dashboard.jinja2", user=current_user, form=form)
    return render_template("dashboard.jinja2", user=current_user, form=form)

@views.context_processor
def search():
    form = Search()
    return dict(form=form)

@views.route("/search", methods=["POST"])
def search():
    form = Search()
    if request.method == "POST":
         searched = form.Search.data
         books = Books.query.filter(Books.name.like('%'+searched+'%'))
         return render_template('search.jinja2', form=form, books=books,user=current_user)

@views.route("/books")
@login_required
def allbooks():
    all_books = Books.query.order_by(Books.date_added)
    return render_template('books.jinja2', user = current_user,books=all_books)

@views.route("/delete_user")
@login_required
def users():
    users = Users.query.order_by(Users.date_added)
    return render_template('delete_users.jinja2', user=current_user,users=users)

@views.route("/delete_user/<int:id>")
@login_required
def delete_users(id):
    delete_user = Users.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    flash("User Deleted Successfully", category="Success")
    return render_template('delete_users.jinja2', user=current_user, delete_user=delete_user)

@views.route("/update_book/<int:id>",methods=["POST","GET"])
@login_required
def update_book(id):
    book_to_update = Books.query.get(id)
    form = UpdateBook()
    if request.method == "POST":
        book_to_update.name = form.Bookname.data
        book_to_update.author = form.Author.data
        book_to_update.read = form.Read.data
        book_to_update.about = form.About.data
        book_to_update.book_pic = form.Pic.data
        try:
            bookpicName= secure_filename(book_to_update.book_pic.filename)
            bookName = bookpicName+'_'+str(uuid.uuid4())

            book_to_update.book_pic = bookName
            saver = form.Pic.data

            try:
                flash("Book details updated successfully", category="Success")
                db.session.commit()
                saver.save(os.path.join(UPLOAD_FOLDER, bookName))
                return render_template("update_books.jinja2", user=current_user, form=form, book=book_to_update)
            except:
                flash("Invalid user",category="Error")
        except:
            flash("Please update even the picture", category="Error")
            return render_template("update_books.jinja2", user=current_user, form=form,book=book_to_update)
    return render_template("update_books.jinja2", user=current_user, form=form, book=book_to_update)

@views.route("/delete/<int:id>")
@login_required
def delete_book(id):
    book_to_delete = Books.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    all_books = Books.query.order_by(Books.date_added)
    flash("Book has been deleted",category="Success")
    return render_template('books.jinja2', user = current_user,books=all_books)



