from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from ..models import School, ClassGroup, Schedule
from ..forms import NewClassForm, NewScheduleForm

@login_required
def index(request):
    if request.method == "POST":
        form = NewClassForm(request.user, request.POST)
        if form.is_valid():
            cg = ClassGroup()
            cg.name = form.cleaned_data["name"]
            if request.POST["description"]:
                cg.description = form.cleaned_data["description"]
            if request.POST["number_of_students"]:
                cg.number_of_students = form.cleaned_data["number_of_students"]
            else:
                cg.number_of_students = 0
            cg.teacher = request.user
            cg.school = form.cleaned_data["school"]
            cg.save()
            return HttpResponseRedirect(reverse("one_class", 
                                                kwargs={'class_id':cg.id}))
        else:
            return create(request)
    elif request.method == "GET":
        return classes_index(request)

@login_required
def classes_index(request, message=None):
    class_list = request.user.classgroups.order_by('name')
    if message:
        return render(request, "planner/classes/index.html", 
                  {"classes": class_list,'message':message})
    else:
        return render(request, "planner/classes/index.html",
                      {"classes": class_list})


@login_required
def show(request, class_id):
    cg = ClassGroup.objects.get(id=class_id)
    if not cg or cg.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "POST":
        #Validate form and update
        form = NewClassForm(request.user, request.POST)
        if form.is_valid():
            cg.name = form.cleaned_data["name"]
            cg.description = form.cleaned_data["description"]
            cg.number_of_students = form.cleaned_data["number_of_students"]
            cg.school = form.cleaned_data["school"]
            cg.save()
            return HttpResponseRedirect(
                    reverse("one_class", kwargs={'class_id':cg.id}),
                    {'message': "Class data successfully updated"})
        else:
            return HttpResponseRedirect(
                    reverse("one_class", kwargs={'class_id':cg.id}),
                    {'message': "Error: Class data couldn't be updated"})

    elif request.method == "GET":
        schedule_forms = []
        for s in cg.schedules.all():
            schedule_forms.append( (s.id, NewScheduleForm(instance = s))  )
        empty_form = NewScheduleForm()
        return render(request, "planner/classes/show.html", 
            {"classgroup": cg, 'schedules': schedule_forms, 'empty_form': empty_form })


@login_required
def create(request):
    form = NewClassForm(request.user)
    return render(request, "planner/classes/create.html", 
                  {'form': form, 'schools' : request.user.schools})

@login_required
def edit(request,class_id):
    cg = ClassGroup.objects.get(id=class_id)
    if not cg or cg.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "GET":
        form = NewClassForm(request.user, cg)
        return render(request, "planner/classes/edit.html",
                {"classgroup": cg, "form":form})


@login_required
def create(request):
    form = NewClassForm(request.user)
    return render(request, "planner/classes/create.html", 
                  {'form': form, 'schools' : request.user.schools})

@login_required
def edit(request,class_id):
    cg = ClassGroup.objects.get(id=class_id)
    if not cg or cg.teacher != request.user:
        return HttpResponse('Permission denied')
    form = NewClassForm(request.user, instance=cg)

    return render(request, "planner/classes/edit.html", 
            {"form":form, "classgroup": cg})

@login_required
def delete(request, class_id):
    cg = ClassGroup.objects.get(id=class_id)
    if not cg or cg.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "POST":
        cg.delete()
        return HttpResponseRedirect(reverse("classes"), 
                {"message": "Class successfully deleted"})    

@login_required
def store_schedule(request, class_id):
    if request.method == "POST":
        cg = ClassGroup.objects.get(id=class_id)
        if not cg or cg.teacher != request.user:
            return HttpResponse('Permission denied')
        form = NewScheduleForm(request.POST)
        if form.is_valid():
            s = Schedule()
            s.classgroup = cg
            s.teacher = cg.teacher
            s.day_of_week = form.cleaned_data['day_of_week']
            s.starts = form.cleaned_data['starts']
            s.ends = form.cleaned_data['ends']
            if s.is_valid():
                s.save()
                message = "New schedule saved"
            else:
                message = "Schedule is not valid"
            return HttpResponseRedirect(reverse("one_class",
                    kwargs={'class_id':cg.id}),
                    {'message':message})
        else:
            return HttpResponseRedirect(reverse("one_class",
                kwargs={'class_id':cg.id}),
                {'message':"Form data is not valid"})

@login_required
def update_schedule(request, schedule_id):
    if request.method == "POST":
        s = Schedule.objects.select_related('classgroup').get(id=schedule_id)
        if not s or s.teacher != request.user:
            return HttpResponse('Permission denied')
        form = NewScheduleForm(request.POST)
        if form.is_valid():
            s.day_of_week = form.cleaned_data['day_of_week']
            s.starts = form.cleaned_data['starts']
            s.ends = form.cleaned_data['ends']
            if s.is_valid():
                s.save()
                message = "Schedule updated"
            else:
                message = "Schedule is not valid, not updated"
            return HttpResponseRedirect(reverse("one_class",
                    kwargs={'class_id':s.classgroup.id}),
                    {'message':message})
        else:
            return HttpResponseRedirect(reverse("one_class",
                kwargs={'class_id':s.classgroup}),
                {'message':"Form data is not valid"})

@login_required
def delete_schedule(request, schedule_id):
    if request.method == "POST":
        s = Schedule.objects.select_related('classgroup').get(id=schedule_id)
        if not s or s.teacher != request.user:
            return HttpResponse('Permission denied')
        s.delete()
        return HttpResponseRedirect(reverse("one_class",
            kwargs={'class_id':s.classgroup.id}),
            {'message':"Schedule has been deleted."})




