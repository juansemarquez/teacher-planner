from django.test import Client, TestCase
from planner.models import School, ClassGroup, Lesson, File, Material, Schedule 
from planner.forms import NewScheduleForm
from django.contrib.auth.models import User

############## CLASSES AND SCHEDULES ############## 

class ClassGroupAndSchedulesTestCase(TestCase):
    def setUp(self):
        u1 = User.objects.create_user('john','lennon@thebeatles.com',
                                     'johnpassword')
        u2 = User.objects.create_user('paul','mccartney@thebeatles.com',
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


    def test_classgroup_count(self):
        u1 = User.objects.get(username="john")
        self.assertEqual(u1.classgroups.count(), 3)

        u2 = User.objects.get(username="paul")
        self.assertEqual(u2.classgroups.count(), 1)

    def test_classgroups_as_string(self):
        cg1 = ClassGroup.objects.get(name="Class 1")
        self.assertEqual(str(cg1), "Class 1 - School Number 1 (30 students)")

        cg2 = ClassGroup.objects.get(name="Class 2")
        self.assertEqual(str(cg2), "Class 2 - School Number 1 (35 students)")

        cg3 = ClassGroup.objects.get(name="Class 3")
        #Number of students is unknown:
        self.assertEqual(str(cg3), "Class 3 - School Number 2")
        self.assertEqual(0, cg3.number_of_students)
        
        cg4 = ClassGroup.objects.get(name="Class 4")
        self.assertEqual(str(cg4), "Class 4 - School Number 3 (34 students)")

    def test_schedule_as_string(self):
        cg1 = ClassGroup.objects.get(name="Class 1")
        sc1 = cg1.schedules.first()
        self.assertEqual("Monday (08:00:00-09:00:00)", str(sc1))

    def test_valid_schedule(self):
        cg1 = ClassGroup.objects.get(name="Class 1")
        sc1 = cg1.schedules.first()
        
        valid = Schedule()
        valid.classgroup = cg1
        valid.teacher = cg1.teacher
        valid.day_of_week = Schedule.DayOfWeek('TU')
        valid.starts = "8:30"
        valid.ends = "9:30"
        self.assertTrue(valid.is_valid())

    def test_valid_schedule(self):
        cg1 = ClassGroup.objects.get(name="Class 1")
        sc1 = cg1.schedules.first()
        
        s = Schedule()
        s.classgroup = cg1
        s.teacher = cg1.teacher
        s.day_of_week = Schedule.DayOfWeek('TU')
        s.starts = "8:30"
        s.ends = "9:30"

        #It's OK.
        self.assertTrue(s.is_valid())

        #Invalid, since it ends before starting:
        s.starts = "10:30"
        self.assertFalse(s.is_valid())

        #Invalid, since it overlaps with the one created on SetUp
        s.day_of_week = Schedule.DayOfWeek('MO')
        s.starts = "8:30" #It starts before the other one is over.
        self.assertFalse(s.is_valid())

        #Invalid, since it overlaps with the one created on SetUp
        s.day_of_week = Schedule.DayOfWeek('MO')
        s.starts = "7:30"
        s.ends = "8:30" #It ends after the other one has started.
        self.assertFalse(s.is_valid())
        
    def test_index(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        response = c.get("/classes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classes"].count(), 3)
    
    def test_show_class(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        cg = u1.classgroups.first()
        form = NewScheduleForm(instance = cg.schedules.first())
        schedules = [ (1,form) ]
        response = c.get("/classes/"+str(cg.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classgroup"].name, "Class 1")
        for t in response.context["schedules"]:
            self.assertEquals(t[0], 1)
            self.assertEquals(tuple(t[1].fields),('day_of_week','starts','ends'))

    def test_update_classgroup(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        s = u1.classgroups.first()
        school_id = s.school.id
        other_school = None
        for one_school in u1.schools.all():
            if one_school.id != school_id:
                other_school = one_school
                break
        if other_school is None:
            other_school = s.school

        #other_school = u1.schools.filter(id!=school_id).first()
        c.post("/classes/"+str(s.id), {'name':"Other name", 
                                       'description':"different",
                                       'school': other_school.id, 
                                       'number_of_students':'11'}
              )
        response = c.get("/classes/"+str(s.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classgroup"].name, "Other name")
        self.assertEqual(response.context["classgroup"].description, "different")
        self.assertEqual(response.context["classgroup"].school.name, other_school.name)
        self.assertEqual(response.context["classgroup"].number_of_students, 11)

    def test_delete_classgroup(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        response = c.get("/classes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classes"].count(), 3)
        c.post("/classes",
                          {'name':"New Class", 
                           'description':"New description",
                           'school':u1.schools.first().id,
                           'number_of_students': 20})
        cg = ClassGroup.objects.last()
        self.assertEqual(cg.name, "New Class")
        
        response = c.get("/classes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classes"].count(), 4)

        c.post("/classes/"+str(cg.id)+"/delete")
        response = c.get("/classes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["classes"].count(), 3)
