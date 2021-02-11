from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
#class Teacher(AbstractUser):
#    pass

class School(models.Model):
    '''Represents one of the schools where the teacher works'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name="schools")
    name = models.CharField(max_length=255,blank=False)
    level = models.CharField(max_length=255,blank=True)
    def __str__(self):
        if self.level:
            return self.name + ' ('+self.level+')'
        else:
            return self.name

class Schedule(models.Model):
    '''Represents a moment in the week when a classgroup meets the teacher
    One classgroup may have several schedules, i.e., the group meets the 
    teacher more than once a week'''
    class DayOfWeek(models.TextChoices):
        MONDAY = 'MO', 'Monday'
        TUESDAY = 'TU', 'Tuesday'
        WEDNESDAY = 'WE', 'Wednesday'
        THURSDAY = 'TH', 'Thursday'
        FRIDAY = 'FR', 'Friday'
        SATURDAY = 'SA', 'Saturday'
        SUNDAY = 'SU', 'Sunday'
    day_of_week = models.CharField(
        max_length=2,
        choices=DayOfWeek.choices,
    )
    starts = models.TimeField(auto_now=False, auto_now_add=False)
    ends = models.TimeField(auto_now=False, auto_now_add=False)
    classgroup = models.ForeignKey("ClassGroup", on_delete=models.CASCADE,
                                   related_name="schedules")
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name="schedules")
    def __repr__(self):
        dow = Schedule.DayOfWeek(self.day_of_week).label
        c = dow +' ('+str(self.starts)+'-'+str(self.ends)+')'
        return c
    def __str__(self):
        return self.__repr__()

    def is_valid(self):
        if isinstance(self.starts, str):
            self.starts=datetime.datetime.strptime(self.starts,'%H:%M').time()
        if isinstance(self.ends, str):
            self.ends=datetime.datetime.strptime(self.ends,'%H:%M').time()


        if self.ends <= self.starts:
            return False
        for s in self.teacher.schedules.all():
            if s.id == self.id:
                continue
            # - Both classes in the same day
            # - this class starts after the visited class has started
            # - this class starts before the visited class has ended
            if self.day_of_week == s.day_of_week \
                    and self.starts >= s.starts and self.starts < s.ends:
                return False
            # - Both classes in the same day
            # - this class ends after the visited class has started
            # - this class ends before the visited class has ended
            if self.day_of_week == s.day_of_week \
                    and self.ends >= s.starts and self.ends < s.ends:
                return False
        return True

    
class ClassGroup(models.Model):
    '''Represents one of the classes where the teacher works'''
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                related_name="classgroups")
    school = models.ForeignKey("School", on_delete=models.CASCADE, 
                               related_name="classgroups")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=False)
    number_of_students = models.PositiveSmallIntegerField(blank=True,default=0)

    def __repr__(self):
        if self.number_of_students:
            n = ' ('+str(self.number_of_students)+' students)'
        else:
            n = ''
        return self.name + " - " + self.school.name + n
    def __str__(self):
        return self.__repr__()

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

