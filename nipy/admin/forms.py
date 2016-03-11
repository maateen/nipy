from flask_security.forms import RegisterForm
from flask_wtf import Form
from nipy.admin.utils import category_choice_list
from nipy.admin.utils import page_choice_list
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Optional


class CategoryForm(Form):

    name = StringField(validators=[DataRequired(), Length(min=4, max=60)])
    slug = StringField(validators=[DataRequired(), Length(min=4, max=64)])
    parent = SelectField(
        validators=[Optional()], choices=category_choice_list(parent=True))
    description = TextAreaField(validators=[Optional()])
    submit = SubmitField()


class PageForm(Form):

    title = StringField(validators=[DataRequired()])
    subtitle = StringField(validators=[Optional()])
    slug = StringField(validators=[DataRequired(), Length(min=4, max=100)])
    parent = SelectField(
        validators=[Optional()], choices=page_choice_list(parent=True))
    content = TextAreaField(validators=[DataRequired()])
    draft = SubmitField()
    publish = SubmitField()


class PostForm(Form):

    title = StringField(validators=[DataRequired()])
    slug = StringField(validators=[DataRequired(), Length(min=4, max=100)])
    category = SelectField(
        validators=[Optional()], choices=category_choice_list(parent=True))
    content = TextAreaField(validators=[DataRequired()])
    summary = TextAreaField(validators=[DataRequired()])
    draft = SubmitField()
    publish = SubmitField()


class ExtendedRegisterForm(RegisterForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=60)])


class UserForm(Form):

    username = StringField(validators=[DataRequired(), Length(min=4, max=60)])
    password = PasswordField(validators=[DataRequired(), Length(
        min=8, max=64), EqualTo('confirm', message='Passwords must match')])
    newpassword = PasswordField(validators=[Optional(), Length(
        min=8, max=64), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(validators=[DataRequired(), Length(min=8, max=64)])
    name = StringField(validators=[Optional(), Length(max=50)])
    email = EmailField(
        validators=[DataRequired(), Length(min=4, max=50), Email()])
    newemail = EmailField(
        validators=[Optional(), Length(min=4, max=50), Email()])
    display_name = StringField(validators=[Optional(), Length(max=50)])
    bio = TextAreaField(validators=[Optional()])
    status = SelectField(validators=[Optional()], choices=[('5', 'Subscriber'), (
        '4', 'Contributor'), ('3', 'Author'), ('2', 'Editor'), ('1', 'Administrator')])
    submit = SubmitField()
