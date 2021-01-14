

# ---3種類のユーザを作成する---
# パーミッションがないユーザーを作成
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, Group
User.objects.all().delete()
Group.objects.all().delete()

no_perisson_user_data = {'username': 'no_permisson_user',
                         'email': 'no_permisson_user@maill.com', 'password': 'pass1234'}
no_perisson_user = User.objects.create_user(
    username=no_perisson_user_data['username'], email=no_perisson_user_data['email'], password=no_perisson_user_data['password'])
# パーミッションがあるユーザーを作成
perisson_user_data = {'username': 'permisson_user',
                      'email': 'permisson_user@maill.com', 'password': 'pass1234'}
perisson_user = User.objects.create_user(
    username=perisson_user_data['username'], email=perisson_user_data['email'], password=perisson_user_data['password'])
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
blog_view_permission = Permission.objects.get(name="""Can view blog""")

# perisson_userにBlogの読み取りアクセス権を与える
perisson_user.user_permissions.set([blog_view_permission])

# 作成したGroupにPermissonオブジェクトを紐づける
blog_view_group.permissions.set([blog_view_permission])


# token = Token.objects.get(user__username='access_user')
# self.client = APIClient()
# self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

# response = self.client.patch(url)
# print(response.data)


# 準備完了 試してみる
class BlogViewTest(TestCase):
    def test_no_permisson_user_view(self):
        url = '/blogs/'
        # self.client = Client()
        # login_status = self.client.login(
        #     username=no_perisson_user_data['username'], password=no_perisson_user_data['password'])
        # self.assertTrue(login_status)
        # response = self.client.get(url)
        # print("パーミッションがないユーザーがアクセスした結果；", response.status_code)

    def test_permisson_user_view(self):
        # url = '/blogs/'
        # self.client = Client()
        # login_status = self.client.login(
        #     username=perisson_user_data['username'], password=perisson_user_data['password'])
        # self.assertTrue(login_status)
        # response = self.client.get(url)
        # print("パーミッションがあるユーザーがアクセスした結果；", response.status_code)
        user = User.objects.get(username=perisson_user_data['username'])
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        response = self.client.get("http://127.0.0.1:8000/blogs/")

    def test_group_user_view(self):
        url = '/blogs/'
        # self.client = Client()
        # login_status = self.client.login(
        #     username=group_user_data['username'], password=group_user_data['password'])
        # self.assertTrue(login_status)
        # response = self.client.get(url)
        # print("パーミッションがあるGroupに属するユーザーがアクセスした結果；", response.status_code)


bvt = BlogViewTest()
bvt.test_no_permisson_user_view()
bvt.test_permisson_user_view()
bvt.test_group_user_view()
