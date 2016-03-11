import random
import string

from datetime import datetime
from flask import url_for
from flask_babel import to_user_timezone
from flask_mail import Message
from nipy import app
from nipy import db
from nipy import mail
from nipy.admin.models import Categories
from nipy.admin.models import Pages
from nipy.admin.models import Posts
from nipy.admin.models import User as Users


def add_category(name, slug, parent=0, description=None):
    checker = Categories.query.filter_by(slug=slug, parent=parent).first()
    if checker is None:
        data = Categories(name, slug, parent, description)
        db.session.add(data)
        db.session.commit()
        return {'category': 'success', 'message': 'The category titled ' + name + ' has been added successfully.'}
    else:
        return {'category': 'danger', 'message': 'The slug of ' + name + ' matches with a previous record under the same parent category.'}


def add_page(title, subtitle, slug, parent, content, status):
    parent = int(parent)
    if status == 0:
        data = Pages(title, subtitle, slug, parent, content, status)
        db.session.add(data)
        db.session.commit()
        return {'category': 'success', 'message': 'The page titled \'' + title + '\' has been drafted successfully.'}
    elif status == 1:
        data = Pages(title, subtitle, slug, parent, content, status)
        db.session.add(data)
        db.session.commit()
        return {'category': 'success', 'message': 'The page titled \'' + title + '\' has been published successfully.'}
    else:
        return {'category': 'danger', 'message': 'Something went very wrong for \'' + title + '\'.'}


def add_post(title, slug, category, content, summary, author, status, date_time=False):
    if date_time is False:
        date_time = datetime.utcnow()
    category = int(category)
    if status == 0:
        data = Posts(author, date_time, category, title,
                     slug, content, summary, status)
        db.session.add(data)
        db.session.commit()
        return {'category': 'success', 'message': 'The post titled \'' + title + '\' has been drafted successfully.'}
    elif status == 1:
        data = Posts(author, date_time, category, title,
                     slug, content, summary, status)
        db.session.add(data)
        db.session.commit()
        return {'category': 'success', 'message': 'The post titled \'' + title + '\' has been published successfully.'}
    else:
        return {'category': 'danger', 'message': 'Something went very wrong for \'' + title + '\'.'}


def add_user(username, email, name, password, status):
    username_checker = Users.query.filter_by(username=username).first()
    if username_checker is None:
        email_checker = Users.query.filter_by(email=email).first()
        if email_checker is None:
            data = Users(username, password, name, email,
                         '', '', '', '', '', '', status)
            db.session.add(data)
            db.session.commit()
            return {'category': 'success', 'message': 'The user has been added successfully.'}
        else:
            return {'category': 'danger', 'message': 'The email address is already in database. Please try another.'}
    else:
        return {'category': 'danger', 'message': 'The username is already in database. Please try another.'}


def category_choice_list(parent=False):
    categories = Categories.query.all()
    if parent is True:
        choices = []
        choices = [('0', 'None')]
    else:
        choices = []
    for category in categories:
        temp = (str(category.id), category.name)
        choices.append(temp)
    return choices


def delete_category(category_id):
    checker1 = Categories.query.filter_by(id=category_id).first()
    if checker1:
        checker2 = Categories.query.filter_by(parent=category_id).first()
        if checker2 is None:
            db.session.delete(checker1)
            db.session.commit()
            return {'category': 'success', 'message': 'The category titled ' + checker1.name + ' has been deleted successfully.'}
        else:
            return {'category': 'danger', 'message': 'The requested category has child category. Please delete or move them to another parent category.'}
    else:
        return {'category': 'danger', 'message': 'The requested category was not found.'}


def delete_page(page_id):
    checker = Pages.query.filter_by(id=page_id).first()
    if checker:
        db.session.delete(checker)
        db.session.commit()
        return {'category': 'success', 'message': 'The page titled \'' + checker.title + '\' has been deleted successfully.'}
    else:
        return {'category': 'danger', 'message': 'The requested page was not found.'}


def delete_post(post_id):
    checker = Posts.query.filter_by(id=post_id).first()
    if checker:
        db.session.delete(checker)
        db.session.commit()
        return {'category': 'success', 'message': 'The post titled ' + checker.title + ' has been deleted successfully.'}
    else:
        return {'category': 'danger', 'message': 'The requested post was not found.'}


def delete_user(user_id):
    pass


def encrypt_password(password):
    encrypted_password = bcrypt.generate_password_hash(password)
    return encrypted_password


def get_author_name(user_id):
    author = Users.query.filter_by(id=user_id).first()
    return author.display_name


def get_author_status(role):
    if role == 0:
        return "Disabled"
    elif role == 1:
        return "Administrator"
    elif role == 2:
        return 'Editor'
    elif role == 3:
        return 'Author'
    elif role == 4:
        return 'Contributor'
    elif role == 5:
        return 'Subscriber'
    else:
        return "Unknown"


def get_category_id_by_name(slug):
    category = Categories.query.filter_by(slug=slug).first()
    return category.id


def get_category_name(category_id):
    category = Categories.query.filter_by(id=category_id).first()
    if category:
        return category.name
    else:
        return "None"


def get_category_records(category_id=None):
    if category_id:
        category_records = Categories.query.filter_by(id=category_id).first()
        return category_records
    else:
        category_records = Categories.query.all()
        return category_records


def get_date(date):
    date = str(date)
    date_format = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(date, date_format)
    date = to_user_timezone(date)
    return datetime.strftime(date, '%B %-d, %Y')


def get_local_datetime(date_time):
    babel = Babel(app)
    date_time = str(date_time)
    date_time_format = '%Y-%m-%d %H:%M:%S'
    try:
        date_time = datetime.strptime(date_time, date_time_format)
        date_time = to_user_timezone(date_time)
        return datetime.strftime(date_time, '%B %-d, %Y - %I:%M:%S %p')
    except:
        return 'None'


def get_number_of_post_of_author(author_id):
    author_id = int(author_id)
    number = Posts.query.filter_by(author=author_id).count()
    if number is None:
        return "None"
    else:
        return number


def get_page_records():
    pages_raw_data = Pages.query.all()
    if pages_raw_data:
        pages = []
        for page_raw_data in pages_raw_data:
            page = {}
            page['id'] = page_raw_data.id
            page['subtitle'] = page_raw_data.subtitle
            page['title'] = page_raw_data.title
            page['parent'] = get_parent_page_name(page_raw_data.parent)
            if page_raw_data.status == 0:
                page['status'] = 'Drafted'
            else:
                page['status'] = 'Published'
            pages.append(page)
        return pages
    else:
        return None


def get_parent_page_name(parent_id):
    if parent_id == 0:
        return "None"
    else:
        data = Pages.query.filter_by(id=parent_id).first()
        return data.title


def get_post_records():
    posts_raw_data = Posts.query.all()
    if posts_raw_data:
        posts = []
        for post_raw_data in posts_raw_data:
            if post_raw_data.status == 1:
                post = {}
                post['id'] = post_raw_data.id
                post['title'] = post_raw_data.title
                post['author'] = get_author_name(post_raw_data.author)
                post['category'] = get_category_name(post_raw_data.category)
                post['date'] = get_date(post_raw_data.datetime)
                if post_raw_data.status == 0:
                    post['status'] = 'Drafted'
                else:
                    post['status'] = 'Published'
                posts.append(post)
        return posts
    else:
        return None


def get_single_post_data(post_slug):
    post_raw_data = Posts.query.filter_by(slug=post_slug).first()
    if post_raw_data:
        if post_raw_data.status == 1:
            post = {}
            post['title'] = post_raw_data.title
            post['author'] = get_author_name(post_raw_data.author)
            post['category'] = get_category_name(post_raw_data.category)
            post['date'] = get_date(post_raw_data.datetime)
            post['slug'] = post_slug
            post['content'] = post_raw_data.content
            post['summary'] = post_raw_data.summary
            if post_raw_data.status == 0:
                post['status'] = 'Drafted'
            else:
                post['status'] = 'Published'
            return post
        else:
            return None
    else:
        return None


def get_single_page_data(post_id):
    page_raw_data = Pages.query.filter_by(id=post_id).first()
    page = {}
    page['id'] = page_raw_data.id
    page['title'] = page_raw_data.title
    page['subtitle'] = page_raw_data.subtitle
    page['slug'] = page_raw_data.slug
    page['parent'] = get_parent_page_name(page_raw_data.parent)
    page['content'] = page_raw_data.content
    if page_raw_data.status == 0:
        page['status'] = 'Drafted'
    else:
        page['status'] = 'Published'
    return page


def get_single_user_data(user_id):
    user_raw_data = Users.query.filter_by(id=user_id).first()
    user = {}
    user['id'] = user_raw_data.id
    user['username'] = user_raw_data.username
    user['name'] = user_raw_data.name
    user['email'] = user_raw_data.email
    user['display_name'] = user_raw_data.display_name
    user['bio'] = user_raw_data.bio
    user['status'] = get_author_status(user_raw_data.status)
    user['total_posts'] = get_number_of_post_of_author(user_raw_data.id)
    user['last_login'] = get_local_datetime(user_raw_data.last_login)
    return user


def get_user_records():
    users_raw_data = Users.query.all()
    if users_raw_data:
        users = []
        for user_raw_data in users_raw_data:
            user = {}
            user['id'] = user_raw_data.id
            user['username'] = user_raw_data.username
            user['name'] = user_raw_data.name
            user['email'] = user_raw_data.email
            user['display_name'] = user_raw_data.display_name
            user['bio'] = user_raw_data.bio
            user['status'] = get_author_status(user_raw_data.status)
            user['total_posts'] = get_number_of_post_of_author(
                user_raw_data.id)
            user['last_login'] = get_local_datetime(user_raw_data.last_login)
            users.append(user)
        return users
    else:
        return None


def page_choice_list(parent=False):
    pages = Pages.query.all()
    if parent is True:
        choices = []
        choices = [('0', 'None')]
    else:
        choices = []
    for page in pages:
        temp = (str(page.id), page.title)
        choices.append(temp)
    return choices


def update_category(category_id, name, slug, parent, description):
    category = Categories.query.filter_by(id=category_id).first()
    if category.slug == slug and category.parent == int(parent):
        category.name = name
        category.description = description
        db.session.commit()
        return {'category': 'success', 'message': 'The category titled ' + name + ' has been updated successfully.'}
    else:
        checker = Categories.query.filter_by(slug=slug, parent=parent).first()
        if checker is None:
            category.name = name
            category.slug = slug
            category.parent = parent
            category.description = description
            db.session.commit()
            return {'category': 'success', 'message': 'The category titled ' + name + ' has been updated successfully.'}
        else:
            return {'category': 'danger', 'message': 'The slug of ' + name + ' matches with a previous record under the same parent category.'}


def update_page(page_id, title, subtitle, slug, parent, content, status):
    page = Pages.query.filter_by(id=page_id).first()
    page.title = title
    page.subtitle = subtitle
    page.slug = slug
    page.parent = int(parent)
    page.content = content
    page.status = status
    db.session.commit()
    if status == 0:
        return {'category': 'success', 'message': 'The page titled \'' + title + '\' has been updated & drafted successfully.'}
    elif status == 1:
        return {'category': 'success', 'message': 'The page titled \'' + title + '\' has been updated & published successfully.'}
    else:
        return {'category': 'danger', 'message': 'Something went very wrong for \'' + title + '\'.'}


def update_post(post_id, title, slug, category, content, summary, status):
    category = int(category)
    post = Posts.query.filter_by(id=post_id).first()
    post.title = title
    post.slug = slug
    post.category = category
    post.content = content
    post.summary = summary
    post.status = status
    db.session.commit()
    if status == 0:
        return {'category': 'success', 'message': 'The post titled \'' + title + '\' has been updated & drafted successfully.'}
    elif status == 1:
        return {'category': 'success', 'message': 'The post titled \'' + title + '\' has been updated & published successfully.'}
    else:
        return {'category': 'danger', 'message': 'Something went very wrong for \'' + title + '\'.'}


def update_user(user_id, username, name, email, display_name, bio, status, newpassword):
    user = Users.query.filter_by(id=user_id).first()
    if user.username != username:
        username_checker = Users.query.filter_by(username=username).first()
        if username_checker is None:
            user.username = username
        else:
            return {'category': 'danger', 'message': 'The username is already in database. Please try another.'}
    if user.email != email:
        email_checker = Users.query.filter_by(email=email).first()
        if email_checker is None:
            user.email = email
        else:
            return {'category': 'danger', 'message': 'The email address is already in database. Please try another.'}
    if user.name != name:
        user.name = name
    if user.email != email:
        user.email = email
    if user.display_name != display_name:
        user.display_name = display_name
    if user.bio != bio:
        user.bio = bio
    if user.status != status:
        user.status = status
    db.session.commit()
    return {'category': 'success', 'message': 'The user has been updated successfully.'}


def verify_password(username, password):
    data = Users.query.filter_by(username=username).first()
    encrypted_password = data.password
    response = bcrypt.check_password_hash(encrypted_password, password)
    return response
