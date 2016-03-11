from flask import Flask
from flask_babel import Babel
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
csrfprotect = CsrfProtect(app)
babel = Babel(app)
mail = Mail(app)


# Setup Flask-Security
from nipy.admin.forms import ExtendedRegisterForm
from nipy.admin.models import Role
from nipy.admin.models import User
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)

from nipy.admin.views import admin
from nipy.blog.views import blog
app.register_blueprint(admin)
app.register_blueprint(blog)
