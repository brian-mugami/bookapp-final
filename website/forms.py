from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,EmailField,SearchField,BooleanField
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired,InputRequired,AnyOf
from wtforms.widgets import FileInput,CheckboxInput

class Bookpage(FlaskForm):
    Bookname = StringField("Name Of The Book", validators=[DataRequired()])
    Author = StringField("Author Of The Book", validators=[DataRequired()])
    Pic = FileField("Picture Of The Book")
    About =CKEditorField("About The Book")
    Read = CheckboxInput(input_type= None)
    Submit = SubmitField("Add Book")

class Suggestionpage(FlaskForm):
    Name = StringField("Name Of The Book", validators=[DataRequired()])
    Author = StringField("Author Of The Book")
    Pic = FileField("Picture Of The Book")
    About = CKEditorField("About The Book")
    Submit = SubmitField("Add Book")

class UpdateUser(FlaskForm):
    Username = StringField("Username")
    Firstname = StringField("Firstname")
    Surname = StringField("Surname")
    Email = EmailField("Email")
    Profile_pic = FileField("Profile Pic")
    Submit = SubmitField("Update")

class Search(FlaskForm):
    Search = SearchField("search", validators=[DataRequired()])
    Submit = SubmitField("Search")

class UpdateBook(FlaskForm):
    Bookname = StringField("Name Of The Book", validators=[DataRequired()])
    Author = StringField("Author Of The Book", validators=[DataRequired()])
    Pic = FileField("Picture Of The Book")
    About = CKEditorField("About The Book")
    Read = BooleanField("Is the book Read" , default=False, validators=[AnyOf([True,False])])
    Submit = SubmitField("Update")