from django.forms import ModelForm
from .models import School

class NewSchoolForm(ModelForm):
    class Meta:
        model = School
        fields = ['name', 'level']

    #name = forms.CharField(max_length=255)
    #level = forms.CharField(max_length=255, required=False)
    #def __init__(name=None, level=None):
        #if name:
            #self.name = name
        #if level:
            #self.level = level
