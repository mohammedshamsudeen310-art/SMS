from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/", views.custom_login, name="custom_login"),
    path("logout/", views.custom_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher-dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("accountant-dashboard/", views.accountant_dashboard, name="accountant_dashboard"),
    path("parent-dashboard/", views.parent_dashboard, name="parent_dashboard"),


    path("profile/", views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path("admin/manage-students/", views.manage_students, name="manage_students"),
    path("students/edit/<int:pk>/", views.edit_student, name="edit_student"),
    path("students/add/", views.add_student, name="add_student"),
    path("admin/student/delete/<int:pk>/", views.delete_student, name="delete_student"),

    path("admin/manage-teachers/", views.manage_teachers, name="manage_teachers"),
    path('add/', views.add_teacher, name='add_teacher'),
    path("admin/teacher/edit/<int:pk>/", views.edit_teacher, name="edit_teacher"),
    path("admin/teacher/delete/<int:pk>/", views.delete_teacher, name="delete_teacher"),
    path('import/', views.import_teachers, name='import_teachers'),

  # accounts/urls.py
    path('manage-parents/', views.manage_parents, name='manage_parents'),
    path('add-parent/', views.add_parent, name='add_parent'),
    path('edit/<int:pk>/', views.edit_parent, name='edit_parent'),
    path('delete/<int:pk>/', views.delete_parent, name='delete_parent'),

    path('child-performance/', views.child_performance, name='child_performance'),
    path('child-result/<int:student_id>/', views.child_result, name='child_result'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)