from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(),name="student_registration"),
    path('courses/',views.StudentCourseListView.as_view(),name='student_course_list'),
    path('enroll-course/',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
    path('course/<pk>/',views.StudentCourseDetail.as_view(),name='student_course_detail'),
    path('course/<pk>/<module_id>/',views.StudentCourseDetail.as_view(),name='student_course_detail_module'),
]