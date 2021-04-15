from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login
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

class StudentCourseListView(View):
    pass
