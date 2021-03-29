from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import Course
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import ModuleFormSet
from django.shortcuts import get_object_or_404,redirect
from django.views.generic import from TemplateResponseMixin


# Create your views here.
class OwnerMixin(object):
    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin):
    model=Course
    fields=['subject','title','slug','overview']
    success_url=reverse_lazy('manage_course_list')

class OwnerEditMixin(object):
    def form_valid(self,form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class OwnerCourseEditMixin(OwnerEditMixin,OwnerCourseMixin):
    template_name='courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin,ListView):
    template_name='courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin,OwnerCourseEditMixin,CreateView):
    permission_required='course.add_course'

class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin,UpdateView):
    permission_required='course.change_course'

class CourseModuleUpdateView(TemplateResponseMixin,View)
    template_name='courses/manage/module/formset.html'
    couse=None


    def get(self,request):
        formset=ModuleFormSet(instance=self.course)
        return self.render_to_response({'formset':formset,
                                        'coure':self.coure
                                        })

    def post(self,request,*args, **kwargs):
        formset=ModuleFormSet(request.post)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course,
                                        'formset':formset})
            
 
    def dispatch(self,request,pk):
        self.course=get_object_or_404(Course,id=pk,Owner=request.user)
        return super(request,pk)

    
class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin,DeleteView):
    permission_required='course.delete_course'
    template_name="courses/manage/course/delete.html"
