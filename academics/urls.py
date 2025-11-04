# academics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("manage-promotions/", views.manage_promotions, name="manage_promotions"),

    path("students/import/", views.import_students, name="import_students"),
    path("students/download-template/", views.download_student_template, name="download_student_template"),

    # ============================================================
    # 🔹 SUBJECTS
    path("subjects/", views.subject_list, name="subject_list"),
    path("subjects/add/", views.add_subject, name="add_subject"),
    path("subjects/<int:pk>/edit/", views.edit_subject, name="edit_subject"),
    path("subjects/<int:pk>/delete/", views.delete_subject, name="delete_subject"),

    # ============================================================
    # 🔹 SESSIONS
    path("sessions/", views.manage_sessions, name="manage_sessions"),
    path("sessions/add/", views.add_session, name="add_session"),
    path("sessions/edit/<int:pk>/", views.edit_session, name="edit_session"),
    path("sessions/delete/<int:pk>/", views.delete_session, name="delete_session"),

]
