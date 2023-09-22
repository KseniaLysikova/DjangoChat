from django.urls import path, include
from user.views import UserToken

urlpatterns = [
    path('token', UserToken.as_view()),
]