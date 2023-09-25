from django.urls import path, include
from user.views import UserInfo

urlpatterns = [
    path('token', UserInfo.as_view()),
]