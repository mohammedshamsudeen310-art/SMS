# attendance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("start-session/", views.start_attendance_session, name="start_attendance_session"),
    path("take-attendance/<int:session_id>/", views.take_attendance, name="take_attendance"),

    path("parent/", views.parent_attendance, name="parent_attendance"),
    path("parent/<int:child_id>/", views.parent_child_attendance_detail, name="parent_attendance_detail"),
]
