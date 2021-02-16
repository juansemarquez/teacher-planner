from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import datetime
class Teacher(User):
    class Meta:
        proxy = True

    def get_lessons_by_taglist(self, tag_list):
        ''' Receives a list of keyphrases, and returns a list of lessons, that
        has at least one of the tags in the received list, ordered from the one
        with most tags in common in first place, to the one with less tags 
        in common at the end'''
        if type(tag_list) is str:
            tag_list = tag_list.strip()
            tag_list = [ tag.strip() for tag in tag_list.split(',') ]
        if len(tag_list) == 0:
            return []
        return self.lessons.filter(tags__keyphrase__in=tag_list).annotate(tag_times=models.Count('id')).order_by('-tag_times')

class School(models.Model):
    '''Represents one of the schools where the teacher works'''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, 
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, 
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, 
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name="lessons")
    files = models.ManyToManyField("File", related_name="lessons")
    material = models.ManyToManyField("Material", related_name="lessons")
    
    goal = models.CharField(max_length=255,blank=False)
    activities = models.TextField(blank=False)
    schedule = models.ForeignKey("Schedule", on_delete=models.SET_NULL,
                                 blank=True, null=True)
    #FIXME: Check timezones
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    afterthoughts = models.TextField(blank=True)
    def similar_lessons(self):
        ''' Returns a list of lessons (different than this one), in which each
        lesson shares at least one tag with this one, ordered from the one
        with most tags in common in first place, to the one with less tags 
        in common at the end'''
        tags = self.tags.all()
        result = Lesson.objects.filter(teacher=self.teacher,
                                    tag_id__in=tags).exclude(id=self.id).get()
        return result

    def similarity(self, other):
        '''Compares this lesson with another one, and counts how many tags they
        share. Returns int'''
        # Creates sets from tags keyphrases
        tag_list = self.tag_set()
        other_tag_list = other.tag_set()
        # How many elements do the sets have in common?
        return len(tag_list.intersection(other_tag_list))

    def tag_set(self):
        ''' Returns a set from tags keyphrases (may be empty set)'''
        return { tag.keyphrase for tag in self.tags }

class File(models.Model):
    '''Represents a file the teacher needs for one or more lessons. Uploading 
    the actual file is not supported at the  moment. Just references.'''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name="files")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=True)
    url = models.URLField(blank=False)

class Material(models.Model):
    '''Represents an object (e.g.: a map or a basketball) that will be 
    necessary for one or more of the teacher's lessons'''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name="material")
    name = models.CharField(max_length=255,blank=False)
    description = models.CharField(max_length=500,blank=True)

class Tag(models.Model):
    '''Represents a tag or keyphrase a teacher describes a lesson with. Any
    lesson can have zero or more tags, and any tag can belong to one or more
    lessons. Tags are used to find similar lessons: two lessons are similar to
    each other if they share the same tags. In the context of this system, for
    example:
    - if lesson "x" and lesson "y" share one tag,
    - and lesson "x" and lesson "z" share three tags,
    - and lesson "x" and lesson "w" share no tags,
    it is said that:
    - lesson "x" isn't similar to lesson "w" (since they share no tags).
    - lesson "x" is similar to lesson "y" and to lesson "z" (tags shared)
    - lesson "x" is 'more similar' to lesson "z" (three tags shared) than to 
        lesson "y" (only one tag shared).'''
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name="tags")
    lessons = models.ManyToManyField("Lesson", related_name="tags")
    keyphrase = models.CharField(max_length=100,blank=False, unique=True)
    def __repr__(self):
        return keyphrase
    def __str__(self):
        return keyphrase



