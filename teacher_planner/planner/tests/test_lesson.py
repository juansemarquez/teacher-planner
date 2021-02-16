from django.test import Client, TestCase
from planner.models import School, ClassGroup, Lesson, File, Material
from planner.models import Schedule, Tag, Teacher
from planner.forms import NewScheduleForm
from django.contrib.auth.models import User
import datetime

############## CLASSES AND SCHEDULES ############## 

class ClassGroupAndSchedulesTestCase(TestCase):
    def setUp(self):
        u1 = Teacher.objects.create_user('john','lennon@thebeatles.com',
                                     'johnpassword')
        u2 = Teacher.objects.create_user('paul','mccartney@thebeatles.com',
                                     'paulpassword')
        s1 = School()
        s1.teacher = u1
        s1.name = "School Number 1"
        s1.level = "High school"
        s1.save()

        s2 = School()
        s2.teacher = u1
        s2.name = "School Number 2"
        s2.save()
        
        s3 = School()
        s3.teacher = u2
        s3.name = "School Number 3"
        s3.level = "High school"
        s3.save()

        cg1 = ClassGroup()
        cg1.teacher = u1
        cg1.school = s1
        cg1.name = "Class 1"
        cg1.description = "This is the first class"
        cg1.number_of_students = 30
        cg1.save()

        cg2 = ClassGroup()
        cg2.teacher = u1
        cg2.school = s1
        cg2.name = "Class 2"
        cg2.description = "This is the second class"
        cg2.number_of_students = 35
        cg2.save()

        cg3 = ClassGroup()
        cg3.teacher = u1
        cg3.school = s2
        cg3.name = "Class 3"
        cg3.description = "This is the third class"
        #N_of_students intentionally missing.
        cg3.save()

        cg4 = ClassGroup()
        cg4.teacher = u2
        cg4.school = s3
        cg4.name = "Class 4"
        cg4.description = "This is the fourth class"
        cg4.number_of_students = 34
        cg4.save()

        sc1 = Schedule()
        sc1.teacher = u1
        sc1.classgroup = cg1
        sc1.day_of_week = Schedule.DayOfWeek('MO')
        sc1.starts = "08:00"
        sc1.ends = "09:00"
        sc1.save()

        t1 = Tag()
        t1.keyphrase = "example1"
        t1.teacher = u1
        t1.save()

        t2 = Tag()
        t2.keyphrase = "example2"
        t2.teacher = u1
        t2.save()

        t3 = Tag()
        t3.keyphrase = "example3"
        t3.teacher = u1
        t3.save()

        l1 = Lesson()
        l1.teacher = u1
        l1.class_group = cg1
        l1.goal = "Goal 1"
        l1.activities = "Activities 1"
        l1.schedule = sc1
        l1.date = datetime.date.today()
        l1.save()
        l1.tags.add(t1)
        l1.save()

        l2 = Lesson()
        l2.teacher = u1
        l2.class_group = cg1
        l2.goal = "Goal 2"
        l2.activities = "Activities 2"
        l2.schedule = sc1
        l2.date = datetime.date.today()
        l2.save()
        l2.tags.add(t1, t2)
        l2.save()

        l3 = Lesson()
        l3.teacher = u1
        l3.class_group = cg1
        l3.goal = "Goal 3"
        l3.activities = "Activities 3"
        l3.schedule = sc1
        l3.date = datetime.date.today()
        l3.save()
        l3.tags.add(t3)
        l3.save()

    def test_find_lessons(self):
        u1 = Teacher.objects.get(username="john")
        tag_list = "example1,example2"
        lessons = u1.get_lessons_by_taglist(tag_list)
        self.assertEqual(lessons.count() , 2)

        self.assertEqual(lessons[0].goal, "Goal 2")
        self.assertEqual(lessons[1].goal, "Goal 1")


