from flask import Blueprint
from flask import abort
from flask import flash
from flask import render_template
from flask import request
from nipy.admin.forms import CategoryForm
from nipy.admin.forms import PageForm
from nipy.admin.forms import PostForm
from nipy.admin.forms import RegisterForm
from nipy.admin.forms import UserForm
from nipy.admin.utils import add_category
from nipy.admin.utils import add_page
from nipy.admin.utils import add_post
from nipy.admin.utils import add_user
from nipy.admin.utils import delete_category
from nipy.admin.utils import delete_page
from nipy.admin.utils import delete_post
from nipy.admin.utils import delete_user
from nipy.admin.utils import get_category_name
from nipy.admin.utils import get_category_records
from nipy.admin.utils import get_local_datetime
from nipy.admin.utils import get_page_records
from nipy.admin.utils import get_post_records
from nipy.admin.utils import get_single_page_data
from nipy.admin.utils import get_single_user_data
from nipy.admin.utils import get_user_records
from nipy.admin.utils import update_category
from nipy.admin.utils import update_page
from nipy.admin.utils import update_post

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/',
                  static_folder='templates/static/', static_url_path='/templates/static')


@admin.route('/')
def index():
    return render_template('index.html')


@admin.route('/categories/')
def categories():
    return render_template('categories.html', category_records=get_category_records(), get_category_name=get_category_name, sequence=0)


@admin.route('/categories/<action>', methods=('GET', 'POST'))
def categories_action(action):
    form = CategoryForm()
    if action == 'add':
        if request.method == 'POST':
            if form.validate():
                response = add_category(request.form['name'], request.form[
                                        'slug'], request.form['parent'], request.form['description'])
                flash(response['message'], response['category'])
                return render_template('categories-action.html', form=form, add=True)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('categories-action.html', form=form, add=True)
        else:
            return render_template('categories-action.html', form=form, add=True)
    elif action == 'delete':
        if request.args.get('category_id'):
            category_id = request.args.get('category_id')
            response = delete_category(category_id)
            flash(response['message'], response['category'])
            return render_template('categories.html', category_records=get_category_records(), get_category_name=get_category_name, sequence=0)
        else:
            return render_template('categories.html', category_records=get_category_records(), get_category_name=get_category_name, sequence=0)
    elif action == 'edit':
        if request.args.get('category_id') and request.method == 'GET':
            category_id = request.args.get('category_id')
            return render_template('categories-action.html', form=form, category_records=get_category_records(category_id), edit=True)
        elif request.args.get('category_id') and request.method == 'POST':
            category_id = request.args.get('category_id')
            if form.validate():
                response = update_category(category_id, request.form['name'], request.form[
                                           'slug'], request.form['parent'], request.form['description'])
                flash(response['message'], response['category'])
                return render_template('categories.html', category_records=get_category_records(), get_category_name=get_category_name, sequence=0)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('categories-action.html', form=form, category_records=get_category_records(category_id), edit=True)
        else:
            return render_template('categories.html', category_records=get_category_records(), get_category_name=get_category_name, sequence=0)
    else:
        abort(404)


@admin.route('/pages/')
def pages():
    return render_template('pages.html', pages=get_page_records(), sequence=0)


@admin.route('/pages/<action>', methods=('GET', 'POST'))
def pages_action(action):
    form = PageForm()
    if action == 'add':
        if request.method == 'POST':
            if form.validate():
                try:
                    if request.form['draft']:
                        response = add_page(request.form['title'], request.form['slug'], request.form[
                                            'parent'], request.form['content'], status=0)
                        flash(response['message'], response['category'])
                        return render_template('pages-action.html', form=form, add=True)
                except:
                    if request.form['publish']:
                        response = add_page(request.form['title'], request.form['slug'], request.form[
                                            'parent'], request.form['content'], status=1)
                        flash(response['message'], response['category'])
                        return render_template('pages-action.html', form=form, add=True)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('pages-action.html', form=form, add=True)
        else:
            return render_template('pages-action.html', pages=get_page_records(), form=form, add=True)
    elif action == 'delete':
        if request.args.get('page_id'):
            page_id = request.args.get('page_id')
            response = delete_page(page_id)
            flash(response['message'], response['category'])
            return render_template('pages.html', pages=get_page_records(), sequence=0)
        else:
            return render_template('pages.html', pages=get_page_records(), sequence=0)
    elif action == 'edit':
        if request.args.get('page_id') and request.method == 'GET':
            page_id = request.args.get('page_id')
            return render_template('pages-action.html', form=form, page=get_single_page_data(page_id), edit=True)
        elif request.args.get('page_id') and request.method == 'POST':
            page_id = request.args.get('page_id')
            if form.validate():
                try:
                    if request.form['draft']:
                        response = update_page(page_id, request.form['title'], request.form[
                                               'slug'], request.form['parent'], request.form['content'], status=0)
                        flash(response['message'], response['category'])
                        return render_template('pages-action.html', form=form, edit=True, page=get_single_page_data(page_id))
                except:
                    if request.form['publish']:
                        response = update_page(page_id, request.form['title'], request.form[
                                               'slug'], request.form['parent'], request.form['content'], status=1)
                        flash(response['message'], response['category'])
                        return render_template('pages-action.html', form=form, edit=True, page=get_single_page_data(page_id))
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('pages-action.html', form=form, edit=True)
        else:
            return render_template('pages.html', posts=get_post_records(), sequence=0)
    else:
        abort(404)


@admin.route('/posts/')
def posts():
    return render_template('posts.html', posts=get_post_records(), sequence=0)


@admin.route('/posts/<action>', methods=('GET', 'POST'))
def posts_action(action):
    form = PostForm()
    if action == 'add':
        if request.method == 'POST':
            if form.validate():
                author = 1
                try:
                    if request.form['draft']:
                        response = add_post(request.form['title'], request.form['slug'], request.form[
                                            'category'], request.form['content'], request.form['summary'], author, status=0)
                        flash(response['message'], response['category'])
                        return render_template('posts-action.html', form=form, add=True)
                except:
                    if request.form['publish']:
                        response = add_post(request.form['title'], request.form['slug'], request.form[
                                            'category'], request.form['content'], request.form['summary'], author, status=1)
                        flash(response['message'], response['category'])
                        return render_template('posts-action.html', form=form, add=True)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('posts-action.html', form=form, add=True)
        else:
            return render_template('posts-action.html', posts=get_post_records(), form=form, add=True)
    elif action == 'delete':
        if request.args.get('post_id'):
            post_id = request.args.get('post_id')
            response = delete_post(post_id)
            flash(response['message'], response['category'])
            return render_template('posts.html', posts=get_post_records(), get_local_datetime=get_local_datetime, sequence=0)
        else:
            return render_template('posts.html', posts=get_post_records(), get_local_datetime=get_local_datetime, sequence=0)
    elif action == 'edit':
        if request.args.get('post_id') and request.method == 'GET':
            post_id = request.args.get('post_id')
            return render_template('posts-action.html', form=form, post_records=get_post_records(post_id), edit=True)
        elif request.args.get('post_id') and request.method == 'POST':
            post_id = request.args.get('post_id')
            if form.validate():
                try:
                    if request.form['draft']:
                        response = update_post(post_id, request.form['title'], request.form['slug'], request.form[
                                               'category'], request.form['content'], request.form['summary'], status=0)
                        flash(response['message'], response['category'])
                        return render_template('posts-action.html', form=form, edit=True, post_records=get_post_records(post_id))
                except:
                    if request.form['publish']:
                        response = update_post(post_id, request.form['title'], request.form['slug'], request.form[
                                               'category'], request.form['content'], request.form['summary'], status=1)
                        flash(response['message'], response['category'])
                        return render_template('posts-action.html', form=form, edit=True, post_records=get_post_records(post_id))
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('posts-action.html', form=form, edit=True)
        else:
            return render_template('posts.html', posts=get_post_records(), sequence=0)
    else:
        abort(404)


@admin.route('/users/')
def users():
    return render_template('users.html', users=get_user_records(), sequence=0)


@admin.route('/users/<action>', methods=('GET', 'POST'))
def users_action(action):
    form = UserForm()
    if action == 'add':
        if request.method == 'POST':
            if form.validate():
                response = add_user(request.form['username'], request.form['email'], request.form[
                                    'name'], request.form['password'], request.form['status'])
                flash(response['message'], response['category'])
                return render_template('users-action.html', form=form, add=True)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('users-action.html', form=form, add=True)
        else:
            return render_template('users-action.html', form=form, add=True)
    elif action == 'delete':
        if request.args.get('user_id'):
            user_id = request.args.get('user_id')
            response = delete_user(user_id)
            flash(response['message'], response['category'])
            return render_template('users.html', category_records=get_category_records(), sequence=0)
        else:
            return render_template('users.html', category_records=get_category_records(), sequence=0)
    elif action == 'edit':
        if request.args.get('user_id') and request.method == 'GET':
            user_id = request.args.get('user_id')
            return render_template('users-action.html', form=form, user=get_single_user_data(user_id), edit=True)
        elif request.args.get('user_id') and request.method == 'POST':
            user_id = request.args.get('user_id')
            if form.validate():
                response = update_user(user_id, request.form['name'], request.form[
                                       'slug'], request.form['parent'], request.form['description'])
                flash(response['message'], response['category'])
                return render_template('users.html', users=get_user_records(), sequence=0)
            else:
                flash(
                    "Form validation failed. Please fill up the form correctly.", "danger")
                return render_template('users-action.html', form=form, user=get_single_user_data(user_id), edit=True)
        else:
            return render_template('users.html', users=get_user_records(), sequence=0)
    else:
        abort(404)
