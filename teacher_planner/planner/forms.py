from django.forms import ModelForm, Form
import django.forms as forms
from .models import School, ClassGroup, Schedule
from django.contrib.auth.models import User

class NewSchoolForm(ModelForm):
    class Meta:
        model = School
        fields = ['name', 'level']

class NewClassForm(ModelForm):    
    class Meta:
        model = ClassGroup
        fields = ('name', 'description', 'number_of_students', 'school')

    def __init__(self, user_logged_in, *args, **kwargs):
        super(NewClassForm, self).__init__(*args, **kwargs)
        self.fields['school'].queryset = School.objects.filter(
                                                    teacher=user_logged_in)


class NewScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['day_of_week', 'starts', 'ends']

