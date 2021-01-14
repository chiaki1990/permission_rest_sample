from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth.models import Permission
# Create your views here.


class BlogViewPermisson(BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        view_blog_p = Permission.objects.get(codename='view_blog')
        if view_blog_p in request.user.user_permissions.all():
            return True
        for g in request.user.groups.all():
            if view_blog_p in g.permissions.all():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class BlogListAPIView(APIView):
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated, BlogViewPermisson)

    def get(self, request, *args, **kwargs):
        self.check_permissions(request)
        # self.check_object_permissionもある
        return Response({'result': 'exit'})


"""
from blogs import executing
# 前提知識としてリクエストヘッダーに記述することがあるし
# 前提知識としてUnauthorizedは401で、認証されない時に表示される
# 前提条件としてForbiddenは403で、リソースに対して権限のないアクセスをすると表示されるもの

from django.contrib.auth.models import User
user1_data = {"username":"user1", "password":"user1"}
User.objects.create_user(username=user1_data["username"], password=user1_data["password"])

BasicAuthentication... HeaderをBasicして


import requests
res = requests.get("http://127.0.0.1:8000/blogs/")
print("Basic認証設定時にusernameとpasswordを渡してない場合", res.status_code)
print("内容", res.content)


res = requests.get("http://127.0.0.1:8000/blogs/", auth=(user1_data["username"], user1_data["password"]))
print("Basic認証設定時に認証内容が不適切な場合", res.status_code)
print("内容", res.content)

res = requests.get("http://127.0.0.1:8000/blogs/", auth=(user1_data["username"], 'hogehoge'))
print("Basic認証設定時に認証内容が適切な場合", res.status_code)
print("内容", res.content)


Token認証を入れてやる？？？


認証は、着信リクエストをリクエストを行ったユーザーに関連付けるために使用されることを学びましたが、
ユーザーがリクエストされたリソースへのアクセスを許可されているかどうかを知るには、これだけでは不十分です。
"""
