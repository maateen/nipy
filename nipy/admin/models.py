from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from nipy import db

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey(
    'user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Categories(db.Model):

    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(60))
    slug = db.Column(db.String(64))
    parent = db.Column(db.BigInteger)
    description = db.Column(db.Text)

    def __init__(self, name, slug, parent, description=None):
        self.name = name
        self.slug = slug
        self.parent = parent
        self.description = description


class Posts(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.BigInteger, primary_key=True)
    author = db.Column(db.BigInteger)
    datetime = db.Column(db.DateTime)
    category = db.Column(db.BigInteger)
    title = db.Column(db.Text)
    slug = db.Column(db.String(100))
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    status = db.Column(db.SmallInteger)

    def __init__(self, author, datetime, category, title, slug, content, summary, status):
        self.author = author
        self.datetime = datetime
        self.category = category
        self.title = title
        self.slug = slug
        self.content = content
        self.summary = summary
        self.status = status


class Pages(db.Model):

    __tablename__ = 'pages'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Text)
    subtitle = db.Column(db.Text)
    slug = db.Column(db.String(100))
    parent = db.Column(db.BigInteger)
    content = db.Column(db.Text)
    status = db.Column(db.SmallInteger)

    def __init__(self, title, subtitle, slug, parent, content, status):
        self.title = title
        self.subtitle = subtitle
        self.slug = slug
        self.parent = parent
        self.content = content
        self.status = status


class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Settings(db.Model):

    __tablename__ = 'settings'
    id = db.Column(db.BigInteger, primary_key=True)
    blog_title = db.Column(db.Text)
    blog_subtitle = db.Column(db.Text)

    def __init__(self, blog_title, blog_subtitle):
        self.blog_title = blog_title
        self.blog_subtitle = blog_subtitle


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(50))
    display_name = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    bio = db.Column(db.Text)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.BigInteger)
    roles = db.relationship(
        'Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
