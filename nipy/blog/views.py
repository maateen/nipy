from flask import Blueprint
from flask import abort
from flask import render_template
from nipy.blog.models import Categories
from nipy.blog.models import Pages
from nipy.blog.models import Posts
from nipy.blog.models import Users
from nipy.blog.utils import get_post_records
from nipy.blog.utils import get_single_post_data

blog = Blueprint('blog', __name__, template_folder='themes/',
                 static_folder='themes/default/static/', static_url_path='/themes/default/static')


@blog.route('/')
def home():
    return render_template('default/index.html', posts=get_post_records())


@blog.route('/<slug>/')
def single_content_without_channel(slug):
    return render_template('default/contact.html')


@blog.route('/<path:channel>/<slug>')
def single_content_with_channel(channel, slug):
    post = get_single_post_data(slug)
    if post is None:
        abort(404)
    else:
        return render_template('default/post.html', post=get_single_post_data(slug))
