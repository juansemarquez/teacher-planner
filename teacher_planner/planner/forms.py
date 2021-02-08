from django import forms

class NewSchoolForm(forms.Form):
    name = forms.CharField(max_length=255)
    level = forms.CharField(max_length=255, required=False)
