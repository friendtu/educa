from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(),name="student_registration"),
    path('course_list',views.StudentCourseListView.as_view(),name='student_course_list'),
]