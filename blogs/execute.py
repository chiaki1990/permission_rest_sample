# 前提知識としてリクエストヘッダーに記述することがあるし
# 前提知識としてUnauthorizedは401で、認証されない時に表示される
# 前提条件としてForbiddenは403で、リソースに対して権限のないアクセスをすると表示されるもの

import requests
from django.contrib.auth.models import User
User.objects.all().delete()

user1_data = {"username": "user1", "password": "user1"}
User.objects.create_user(
    username=user1_data["username"], password=user1_data["password"])

# username, passwordが渡されていないとき
res = requests.get("http://127.0.0.1:8000/blogs/")
print("Basic認証設定時にusernameとpasswordを渡してない場合", res.status_code)
print("内容", res.content, "\n")

# 認証内容が不適切なとき
res = requests.get("http://127.0.0.1:8000/blogs/",
                   auth=(user1_data["username"], 'hogehoge'))
print("Basic認証設定時に認証内容が不適切な場合", res.status_code)
print("内容", res.content, "\n")

# 適切な認証内容が与えられたとき
res = requests.get("http://127.0.0.1:8000/blogs/",
                   auth=(user1_data["username"], user1_data["password"]))
print("Basic認証設定時に認証内容が適切な場合", res.status_code)
print("内容", res.content, "\n")
