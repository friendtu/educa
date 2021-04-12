from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views.generic.list import ListView
from .models import Course
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import ModuleFormSet
from django.shortcuts import get_object_or_404,redirect
from django.views.generic.base import TemplateResponseMixin,View
from django.apps import apps
from .models import Module,Content
from django.forms.models import modelform_factory


# Create your views here.
class OwnerMixin(object):
    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin):
    model=Course
    
class OwnerEditMixin(object):
    def form_valid(self,form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class OwnerCourseEditMixin(OwnerEditMixin,OwnerCourseMixin):
    fields=['subject','title','slug','overview']
    template_name='courses/manage/course/form.html'
    success_url=reverse_lazy('manage_course_list')

class ManageCourseListView(OwnerCourseMixin,ListView):
    template_name='courses/manage/course/list.html'

class CourseCreateView(PermissionRequiredMixin,OwnerCourseEditMixin,CreateView):
    permission_required='course.add_course'

class CourseUpdateView(PermissionRequiredMixin,OwnerCourseEditMixin,UpdateView):
    permission_required='course.change_course'

class CourseDeleteView(PermissionRequiredMixin,OwnerCourseMixin,DeleteView):
    permission_required='course.delete_course'
    template_name="courses/manage/course/delete.html"
    success_url=reverse_lazy('manage_course_list')

class CourseModuleUpdateView(TemplateResponseMixin,View):
    template_name='courses/manage/module/formset.html'
    course=None

    def get(self,request,*args,**kwargs):
        formset=ModuleFormSet(instance=self.course)
        return self.render_to_response({'formset':formset,
                                        'course':self.course
                                        })

    def post(self,request,*args, **kwargs):
        formset=ModuleFormSet(instance=self.course,data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course,
                                        'formset':formset}) 
 
    def dispatch(self,request,pk):
        self.course=get_object_or_404(Course,id=pk,owner=request.user)
        return super().dispatch(request,pk)



#show all modules under the course that hosts the module 
#show all contents under the module
#show buttons to add new contents under the module
class ModuleContentListView(TemplateResponseMixin,View):
    template_name="courses/manage/module/content_list.html"
    def get(self,request,module_id):
        module=get_object_or_404(Module,id=module_id,course__owner=request.user)
        return self.render_to_response({'module':module})

class ContentCreateUpdateView(TemplateResponseMixin,View):
    module=None
    obj=None
    template_name='courses/manage/content/form.html'

    def get_model(self,model_name):
        if model_name in ('text','image','video','file'):
            return apps.get_model(app_label='courses',model_name=model_name)
        return None

    def get_form(self,model,*args,**kwargs):
        Form=modelform_factory(model,exclude=('owner','created','updated'))
        return Form(*args,**kwargs)

    def dispatch(self,request,module_id,model_name,id=None):
        self.model=self.get_model(model_name)
        self.module=get_object_or_404(Module,course__owner=request.user,id=module_id)
        if id:
            self.obj=get_object_or_404(self.model,owner=request.user, id=id)
        return super().dispatch(request,module_id,model_name,id)

    def get(self,request,module_id, model_name,id=None):
        form=self.get_form(self.model,instance=self.obj)
        return self.render_to_response({'form':form,
                                        'object':self.obj})

    def post(self,request,module_id,model_name,id=None):
        form=self.get_form(self.model,data=request.POST,files=request.FILES)

        if form.is_valid():
            obj=form.save(commit=False)
            obj.owner=request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,item=obj)
            return redirect('module_content_list',self.module.id)
        return self.render_to_response({'form':form,
                                        'object':self.obj})


class ContentDeleteView(View):
    def post(self,request,content_id):
        content=get_object_or_404(Content,id=content_id,module__course__owner=request.user)
        module=content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list',module.id)



