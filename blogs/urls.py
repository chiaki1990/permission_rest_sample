from django.urls import path
from .views import BlogListAPIView

urlpatterns = [
    path('', BlogListAPIView.as_view())
]
