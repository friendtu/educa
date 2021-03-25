from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Subject(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=['title']

class Course(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='courses_created')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='courses')
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)
    overview=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created']


    def __str__(self):
        return self.title

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=True)
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                    limit_choices_to={'model__in':['text','file','image','video']})
    object_id = models.PositiveIntegerField(default=0)
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title

class ItemBase(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related')
    title=models.CharField(max_length=250)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
class Text(ItemBase):
    content=models.TextField

class File(ItemBase):
    file=models.FileField(upload_to='files')

class Image(ItemBase):
    image=models.ImageField(upload_to='images')

class Video(ItemBase):
    video=models.URLField()


    

