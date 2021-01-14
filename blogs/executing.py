###########################################################
# 使い方 projectルートディレクトリに移動後、、、
# python manage.py makemigrations
# python manage.py migrate
# python manage.py shell
# import blogs.executing
###########################################################


# ---3種類のユーザを作成する---
# パーミッションがないユーザーを作成
import requests
from django.contrib.auth.models import User, Permission, Group
User.objects.all().delete()
Group.objects.all().delete()

no_permission_user_data = {'username': 'no_permisson_user',
                           'email': 'no_permisson_user@maill.com', 'password': 'pass1234'}
no_permission_user = User.objects.create_user(
    username=no_permission_user_data['username'], email=no_permission_user_data['email'], password=no_permission_user_data['password'])
# パーミッションがあるユーザーを作成
permission_user_data = {'username': 'permisson_user',
                        'email': 'permisson_user@maill.com', 'password': 'pass1234'}
permission_user = User.objects.create_user(
    username=permission_user_data['username'], email=permission_user_data['email'], password=permission_user_data['password'])
# パーミッションを有するグループに属するユーザーを作成
group_user_data = {'username': 'group_user',
                   'email': 'group_user@maill.com', 'password': 'pass1234'}
group_user = User.objects.create_user(
    username=group_user_data['username'], email=group_user_data['email'], password=group_user_data['password'])


# Groupオブジェクトを作成
blog_view_group = Group.objects.create(name='blog_view_group')
# GroupオブジェクトにUserオブジェクトを紐づける
group_user.groups.set([blog_view_group])

# ---パーミッションをセットする---
# Permissonオブジェクトを作成(migrate時に自動作成されていのでパス-> getで取得)
# #blog_view_permission = Permission.objects.get(name="""Can view blog""")
view_blog_p = Permission.objects.get(codename='view_blog')

# perisson_userにBlogの読み取りアクセス権を与える
permission_user.user_permissions.set([view_blog_p])

# 作成したGroupにPermissonオブジェクトを紐づける
blog_view_group.permissions.set([view_blog_p])


# 準備完了 試してみる
class BlogViewCheck:

    def no_permisson_user_view(self):
        res = requests.get("http://127.0.0.1:8000/blogs/", auth=(
            no_permission_user_data['username'], no_permission_user_data['password']))
        print("パーミッションがないユーザーがアクセスした結果；", res.status_code)
        print(res.content, "\n")

    def permisson_user_view(self):
        res = requests.get("http://127.0.0.1:8000/blogs/", auth=(
            permission_user_data['username'], permission_user_data['password']))
        print("パーミッションがあるユーザーがアクセスした結果；", res.status_code)
        print(res.content, "\n")

    def group_user_view(self):
        res = requests.get("http://127.0.0.1:8000/blogs/", auth=(
            group_user_data['username'], group_user_data['password']))
        print("パーミッションがあるGroupに属するユーザーがアクセスした結果；", res.status_code)
        print(res.content, "\n")


bv = BlogViewCheck()
bv.no_permisson_user_view()
bv.permisson_user_view()
bv.group_user_view()
