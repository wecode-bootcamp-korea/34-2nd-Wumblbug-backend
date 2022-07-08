from django.urls import path

from projects.views import ProjectDetailView, ProjectListView

urlpatterns = [
    path("/<int:project_id>", ProjectDetailView.as_view()),
    path("", ProjectListView.as_view()),
]