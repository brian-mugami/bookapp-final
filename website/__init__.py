import secrets
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
DBNAME = 'books'
def create_app():

    app = Flask(__name__)
    secret = secrets.token_urlsafe(23)
    app.secret_key = secret

    #sqlitedb
    #app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite///" + os.path.join(basedir, 'booksappdb')
    #myslq
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:Mugaaguva20@localhost:5432/{DBNAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    migrate.init_app(app, db)



    from website.views import views
    from website.auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.jinja2'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.jinja2'), 500

    from .models import Users,Books,Suggestions

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))


    return app


