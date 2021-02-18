from django.forms import ModelForm, Form
import django.forms as forms
from .models import School, ClassGroup, Schedule, Lesson
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

class ScheduleSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None,
            attrs=None):
        option = super().create_option(name, value, label, selected, index, 
                subindex, attrs)
        if value:
            option['attrs']['data-classgroup'] = value.instance.classgroup.id
        else:
            option['attrs']['data-classgroup'] = 'No selection'
        return option


class NewLessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['class_group', 'schedule', 'goal', 
                  'activities', 'date', 'afterthoughts']
        widgets = { 'schedule': ScheduleSelect}

 
    def __init__(self, user_logged_in, *args, **kwargs):
        super(NewLessonForm, self).__init__(*args, **kwargs)
        self.fields['class_group'].queryset = ClassGroup.objects.filter(
                                                    teacher=user_logged_in)
        self.fields['schedule'].queryset = Schedule.objects.filter(
                                                    teacher=user_logged_in)


