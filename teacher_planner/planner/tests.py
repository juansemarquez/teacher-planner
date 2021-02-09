from django.test import Client, TestCase

# Create your tests here.
from .models import School, ClassGroup, Lesson, File, Material 
from django.contrib.auth.models import User

class SchoolTestCase(TestCase):
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

    def test_school_count(self):
        u1 = User.objects.get(username="john")
        self.assertEqual(u1.schools.count(), 2)

        u2 = User.objects.get(username="paul")
        self.assertEqual(u2.schools.count(), 1)

    def test_schools_as_string(self):
        s1 = School.objects.get(name="School Number 1")
        self.assertEqual(str(s1), "School Number 1 (High school)")

        s2 = School.objects.get(name="School Number 2")
        self.assertEqual(str(s2), "School Number 2")

    def test_index(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        response = c.get("/schools")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 2)

    def test_show_school(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        s = u1.schools.first()
        response = c.get("/schools/"+str(s.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["school"].name, "School Number 1")

    def test_create_school(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        response = c.get("/schools")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 2)
        response = c.post("/schools",
                          {'name':"New School", 'level':"New level"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 3)
        s = School.objects.last()
        self.assertEqual(s.name, "New School")
        self.assertEqual(s.level, "New level")

    def test_update_school(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        s = u1.schools.first()
        response = c.post("/schools/"+str(s.id),
                          {'name':"Other name", 'level':"Other level"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["school"].name, "Other name")


    def test_delete_school(self):
        u1 = User.objects.get(username="john")
        c = Client()
        c.force_login(u1)
        response = c.get("/schools")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 2)
        response = c.post("/schools",
                          {'name':"New School", 'level':"New level"})
        s = School.objects.last()
        self.assertEqual(s.name, "New School")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 3)
        response = c.post("/schools/"+str(s.id)+"/delete")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["schools"].count(), 2)











