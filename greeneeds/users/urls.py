from django.urls import path

from users.views import LikeView

urlpatterns = [
    path('/like' , LikeView.as_view())        
]