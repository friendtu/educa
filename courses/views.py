from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Course
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
class OwnerMixin(object):
    def get_queryset():
        qs=super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerCourseMixin(OwnerMixin):
    model=Course

class OwnerEditMixin(object):
    def form_valid(self,form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class OwnerCourseEditMixin(LoginRequiredMixin,OwnerEditMixin,OwnerCourseMixin):
    fields=['subject','title','slug','overview']
    success_url=reverse_lazy('manage_course_list')
    template_name='courses/manage/course/edit.html'

class ManageCourseListView(OwnerCourseMixin,ListView):
    template_name='courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin,OwnerCourseMixin,CreateView):
    permission_required='course.add_course'

class CourseUpdateView(PermissionRequiredMixin,OwnerCourseMixin,UpdateView):
    permission_required='course.change_course'
    
class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin,DeleteView):
    permission_required='course.delete_course'
    template_name="courses/manage/course/delete.html"
    success_url=reverse_lazy('manage_course_list')
