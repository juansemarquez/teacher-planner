from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from ..models import School
from ..forms import NewSchoolForm

@login_required
def schools(request):
    if request.method == "POST":
        form = NewSchoolForm(request.POST)
        if form.is_valid():
            school = School()
            school.name = form.cleaned_data["name"]
            if request.POST["level"]:
                school.level = form.cleaned_data["level"]
            school.teacher = request.user
            school.save()
            return schools_index(request, "School successfully created")
        else:
            return schools_create(request)

    elif request.method == "GET":
        return schools_index(request)

@login_required
def schools_index(request, message=None):
    school_list = request.user.schools.order_by('name')
    if message:
        return render(request, "planner/schools/index.html", 
                  {"schools": school_list,'message':message,"paginated":False})
    else:
        return render(request, "planner/schools/index.html",
                  {"schools": school_list, "paginated":False})


@login_required
def schools_show(request, school_id):
    school = School.objects.filter(id=school_id).get()
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "POST":
        #Validate form and update
        form = NewSchoolForm(request.POST)
        if form.is_valid():
            school.name = form.cleaned_data["name"]
            school.level = form.cleaned_data["level"]
            school.save()
            return render(request, "planner/schools/show.html",
                    {"school": school, 
                     "message": "School data has been updated"})
        else:
            return render(request, "planner/schools/show.html",
                    {"school": school, 
                     "message": "Error: School data couldn't be updated."})

    elif request.method == "GET":
        return render(request, "planner/schools/show.html",{"school": school})
    else:
        return HttpResponse('HTTP Method error')


@login_required
def schools_create(request):
    form = NewSchoolForm()
    return render(request, "planner/schools/edit.html", 
                  {"school": None, "form": form})

@login_required
def schools_edit(request,school_id):
    school = School.objects.filter(id=school_id).get()
    form = NewSchoolForm(instance=school)
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')
    return render(request, "planner/schools/edit.html", 
                  {"form":form, "school": school})

@login_required
def schools_delete(request, school_id):
    school = School.objects.filter(id=school_id).get()
    if not school or school.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "POST":
        school.delete()
        return schools_index(request, "School successfully deleted")
    

