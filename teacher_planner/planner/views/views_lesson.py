from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime

from ..models import School, ClassGroup, Schedule, Teacher, Lesson, Tag
from ..forms import NewClassForm, NewScheduleForm, NewLessonForm

@login_required
def index(request):
    if request.method == "POST":
        form = NewLessonForm(request.user, request.POST)
        if form.is_valid():
            lesson = Lesson()
            lesson.teacher = request.user
            lesson.class_group = form.cleaned_data["class_group"]
            lesson.goal = form.cleaned_data["goal"]
            lesson.activities = form.cleaned_data["activities"]
            if request.POST["schedule"]:
                lesson.schedule = form.cleaned_data["schedule"]
            if request.POST['afterthoughts']:
                lesson.afterthoughts = form.cleaned_data['afterthoughts']
            lesson.save()
            if request.POST["tags"]:
                tag_list = [ tag.strip() \
                        for tag in request.POST['tags'].split(',') ]
                exist=request.user.tags.filter(keyphrase__iexact__in=tag_list)

                # Adding existing tags:
                for tag in exist:
                    lesson.tags.add(tag)
                    tag_list.remove(tag.keyphrase)
                
                # Adding new tags
                for tag in tag_list:
                    new_tag = Tag()
                    tag.keyphrase = tag
                    new_tag.save()
                    lesson.tags.add(tag)

            # TODO: Files and material

            return HttpResponseRedirect(reverse("lesson", 
                                               kwargs={'lesson_id':lesson.id}))
        else:
            return create(request)
    elif request.method == "GET":
        return lesson_index(request)

@login_required
def lesson_index(request, message=None):
    today_lessons_list = request.user.lessons\
            .filter(date=datetime.date.today()).order_by('schedule__starts')
    future_lessons_list = request.user.lessons\
            .filter(date__gt=datetime.date.today())\
            .order_by('date','schedule__starts')
    past_lessons_list = request.user.lessons\
            .filter(date__lt=datetime.date.today())\
            .order_by('-date', '-schedule__starts')
    attributes = {"past_lessons_list": past_lessons_list,
                  "future_lessons_list": future_lessons_list,
                  "today_lessons_list": today_lessons_list,
                  "message": message,
                  "future_paginated": False,
                  "past_paginated": False,
                 }
    if len(future_lessons_list) > 10:
        future_paginator = Paginator(future_lessons_list, 10)
        page_number_future = request.GET.get('page_number_future')
        attributes['future_lessons_list'] = \
                future_paginator.get_page(page_number_future)
        attributes['future_paginated'] = True

    if len(past_lessons_list) > 10:
        past_paginator = Paginator(past_lessons_list, 10)
        page_number_past = request.GET.get('page_number_past')
        attributes['past_lessons_list'] = \
            past_paginator.get_page(page_number_past)
        attributes['past_paginated'] = True


    return render(request, "planner/lessons/index.html", attributes)

@login_required
def show(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if not lesson or lesson.teacher != request.user:
        return HttpResponse('Permission denied')
    if request.method == "POST":
        #Validate form and update
        form = NewLessonForm(request.user, request.POST)
        if form.is_valid():
            lesson.goal = form.cleaned_data["goal"]
            lesson.activities = form.cleaned_data["activities"]
            lesson.date = form.cleaned_data["date"]
            lesson.class_group = form.cleaned_data["class_group"]
            if request.POST['schedule']:
                lesson.schedule = form.cleaned_data["schedule"]
            if request.POST['afterthoughts']:
                lesson.afterthoughts = form.cleaned_data['afterthoughts']
            lesson.save()
            # TODO: Files and material
            return HttpResponseRedirect(
                    reverse("lesson_show", kwargs={'lesson_id': lesson.id}),
                    {'message': "Lesson data successfully updated"})
        else:
            return HttpResponseRedirect(
                    reverse("lesson_show", kwargs={'lesson_id': lesson.id}),
                    {'message': "Error: Lesson data couldn't be updated"})

    elif request.method == "GET":
        #TODO: Files and material
        # schedule_forms = []
        # for s in cg.schedules.all():
            # schedule_forms.append( (s.id, NewScheduleForm(instance = s))  )
        # empty_form = NewScheduleForm()
        return render(request, "planner/lessons/show.html", {"lesson": lesson, 
              #'schedules': schedule_forms, 'empty_form': empty_form 
             })


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




