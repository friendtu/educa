from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView


# Create your views here.

class StudentRegistrationView(CreateView):
    form_class=UserCreationForm
    template_name="students/student/registration.html"
    success_url=reverse_lazy("student_course_list")

    def form_valid(self,form):
        result=super().form_valid(form)
        cd=form.cleaned_data
        user=authenticate(self.request,user=cd['username '],password=cd['password1'])
        login(self.request,user=user)
        return result

class StudentCourseListView(LoginRequiredMixin,ListView):
    model=Course
    template_name="students/course/list.html"
    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    form_class=CourseEnrollForm
    course=None
    
    def form_valid(self, form):
        self.course=form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',args=[self.course.id])
    
class StudentCourseDetail(DetailView):
    model=Course
    template_name="students/course/detail.html"

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(students__in=[self.request.user])


    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        
        course=self.get_object()
        if 'module_id' in self.kwargs:
            context['module']=course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module']=course.modules.all()[0]
        return context
    
