import wxr_parser

from nipy import db
from nipy import user_datastore
from nipy.admin.models import Categories
from nipy.admin.models import Pages
from nipy.admin.models import Posts
from nipy.admin.models import Role
from nipy.admin.models import Settings
from nipy.admin.models import User
from nipy.admin.utils import add_category
from nipy.admin.utils import add_post
from nipy.admin.utils import get_category_id_by_name
from sys import argv

if argv[1] == 'syncdb':
    # db.drop_all()
    db.create_all()
    checker = Role.query.count()
    if checker == 0:
        print("ok")
        roles = ['Administrator', 'Editor',
                 'Author', 'Contributor', 'Subscriber']
        for role in roles:
            response = user_datastore.create_role(name='test')
            print(response)

elif argv[1] == 'import_wordpress':
    if '.xml' in argv[2]:
        parsed_data = wxr_parser.parse(argv[2])
        categories = parsed_data['categories']
        category_keys = sorted(categories.keys())
        print("By default, these categories won't have any parent.")
        for category_key in category_keys:
            response = add_category(categories[category_key][
                                    'title'], categories[category_key]['slug'])
            print(response['message'])
        print("Now, we will import all posts.")
        users = Users.query.all()
        for user in users:
            print(str(user.id) + '. ' + user.username)
        print("To whom you wanna assign these posts.")
        author = int(input())
        print("Do you wanna publish or draft all posts?\n0. Draft\n1. Publish")
        status = int(input())
        posts = reversed(parsed_data['posts'])
        for post in posts:
            response = add_post(post['title'], post['slug'], get_category_id_by_name(post['categories'][
                                0]), post['content'], post['content'][:300], author, status, post['pub_date'])
            print(response['message'])
    else:
        print("Expecting a xml file path after 'import_wordpress' command.")

else:
    print("Error in Command!")
