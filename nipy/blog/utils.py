from datetime import datetime
from flask import Markup
from flask import url_for
from flask_babel import Babel
from flask_babel import to_user_timezone
from nipy import app
from nipy.blog.models import Categories
from nipy.blog.models import Pages
from nipy.blog.models import Posts
from nipy.blog.models import Users


def get_author_name(user_id):
    author = User.query.filter_by(id=user_id).first()
    return author.display_name


def get_category_channel(category_id):
    category = Categories.query.filter_by(id=category_id).first()
    if category:
        if category.parent != 0:
            category_slug = ''
            while category.parent != 0:
                category_slug = category.slug
                category = Categories.query.filter_by(
                    id=category.parent).first()
                if category:
                    category_slug = category.slug + '/' + category_slug
        else:
            category_slug = category.slug
    else:
        category_slug = ''
    return category_slug


def get_category_name(category_id):
    category = Categories.query.filter_by(id=category_id).first()
    try:
        return category.name
    except:
        return 'Unknown'


def get_date(date):
    babel = Babel(app)
    date = str(date)
    date_format = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(date, date_format)
    date = to_user_timezone(date)
    return datetime.strftime(date, '%B %-d, %Y')

"""def get_post_url(post_id):
	post = Posts.query.filter_by(id = post_id).first()
	post_slug = post.slug
	category_channel = get_category_channel(post.category)
	return url_for('blog.single_post', category_channel = category_channel, post_slug = post_slug)"""


def get_post_records():
    posts_raw_data = Posts.query.all()
    if posts_raw_data:
        posts = []
        for post_raw_data in posts_raw_data:
            if post_raw_data.status == 1:
                post = {}
                post['author'] = get_author_name(post_raw_data.author)
                post['date'] = get_date(post_raw_data.datetime)
                post['category'] = get_category_name(post_raw_data.category)
                post['title'] = post_raw_data.title
                post['slug'] = post_raw_data.slug
                category_channel = get_category_channel(post_raw_data.category)
                post['url'] = url_for(
                    'blog.single_content_with_channel', channel=category_channel, slug=post['slug'])
                post['content'] = Markup(post_raw_data.content)
                post['summary'] = Markup(post_raw_data.summary)
                posts.append(post)
        return posts
    else:
        return None


def get_single_post_data(post_slug):
    post_raw_data = Posts.query.filter_by(slug=post_slug).first()
    if post_raw_data:
        if post_raw_data.status == 1:
            post = {}
            post['author'] = get_author_name(post_raw_data.author)
            post['date'] = get_date(post_raw_data.datetime)
            post['category'] = get_category_name(post_raw_data.category)
            post['title'] = post_raw_data.title
            post['slug'] = post_slug
            post['content'] = Markup(post_raw_data.content)
            post['summary'] = Markup(post_raw_data.summary)
            return post
        else:
            return None
    else:
        return None
