from nipy import db
from nipy.admin.models import Categories as MyCategories
from nipy.admin.models import Pages as MyPages
from nipy.admin.models import Posts as MyPosts
from nipy.admin.models import Role as MyRoles
from nipy.admin.models import Settings as MySettings
from nipy.admin.models import User as MyUsers


class Categories(MyCategories):
    pass


class Pages(MyPages):
    pass


class Posts(MyPosts):
    pass


class Roles(MyRoles):
    pass


class Settings(MySettings):
    pass


class Users(MyUsers):
    pass
