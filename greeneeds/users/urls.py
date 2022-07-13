from django.urls import path

from users.views import KakaoSigninView, UserView

urlpatterns = [
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('' , UserView.as_view()),
]