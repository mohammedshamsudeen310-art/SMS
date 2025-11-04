from django.urls import path
from . import views

urlpatterns = [
    path("mark-results/", views.mark_results, name="mark_results"),
    path("my-results/", views.view_my_results, name="view_my_results"),
    path("upload-results/", views.upload_results, name="upload_results"),
    path("download-template/", views.download_results_template, name="download_results_template"),

    path('download_result/', views.download_result, name='download_result'),


]
