from django.urls import path

from projects.views import ProductUploadView, S3ImgUploader

urlpatterns = [
    path('/upload', ProductUploadView.as_view()),
    path('/test_upload', S3ImgUploader.as_view())
]