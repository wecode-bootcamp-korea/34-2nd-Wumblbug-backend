from django.urls import path

from users.views import KakaoSigninView

urlpatterns = [
    path('/signin/kakao', KakaoSigninView.as_view()), 
]