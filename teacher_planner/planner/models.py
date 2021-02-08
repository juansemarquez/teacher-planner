from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

#class Teacher(AbstractUser):
#    pass

class School(models.Model):
    '''Represents one of the schools where the teacher works'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name="schools")
    name = models.CharField(max_length=255,blank=False)
    level = models.CharField(max_length=255,blank=True)
    
class ClassGroup(models.Model):
    '''Represents one of the classes where the teacher works'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name="classgroups")
    school = models.ForeignKey("School", on_delete=models.CASCADE, 
                               related_name="classgroups")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=False)

class Lesson(models.Model):
    '''Represents a lesson in a class'''
    class_group = models.ForeignKey("ClassGroup", on_delete=models.CASCADE,
                                    related_name="lessons")
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                related_name="lessons")
    files = models.ManyToManyField("File", related_name="lessons")
    material = models.ManyToManyField("Material", related_name="lessons")
    similar_lessons = models.ManyToManyField("Lesson")
    goal = models.CharField(max_length=255,blank=False)
    activities = models.TextField(blank=False)
    #FIXME: Check timezones
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    afterthoughts = models.TextField(blank=True)

class File(models.Model):
    '''Represents a file the teacher needs for one or more lessons. Uploading 
    the actual file is not supported at the  moment. Just references.'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                related_name="files")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=True)
    url = models.URLField(blank=False)

class Material(models.Model):
    '''Represents an object (e.g.: a map or a basketball) that will be 
    necessary for one or more of the teacher's lessons'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                related_name="material")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=True)

