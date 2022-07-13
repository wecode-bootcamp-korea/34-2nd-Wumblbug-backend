from django.urls import path

from users.views import KakaoSigninView, UserView, LikeView

urlpatterns = [
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('/like' , LikeView.as_view()),
    path('' , UserView.as_view()),
]